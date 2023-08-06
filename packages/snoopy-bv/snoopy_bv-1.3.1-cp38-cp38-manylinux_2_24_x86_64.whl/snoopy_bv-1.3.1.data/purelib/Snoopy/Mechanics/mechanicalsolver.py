# -*- coding: utf-8 -*-


import enum
import numpy as np
from Snoopy.Mechanics import McnInput,RdfCoef,McnCoef
from .rdfcoef import RdfCoef
from Snoopy import logger
from Snoopy import Spectral as sp
import os.path
from scipy.linalg import eigh
from scipy import interpolate, optimize


EPS = 1e-6


def unset_zeros_matrix(matrix):
    """Return None if input matrix is zeros
    Return the input as is otherwise
    Parameters
    ----------
    matrix : arraylike or None
        Input matrix

    Returns
    -------
    _type_
        _description_

    """
    if matrix is not None:
        if np.all(np.abs(matrix)<1e-15):
            return None
    return matrix
class MechanicalSolver :

    def __init__(self, mcn_input_obj, rdf_coef_obj):
        """Initialize object MechanicalSolver from 
        mcn_input_obj and rdf_coef_obj
        Parameters
        ----------
        mcn_input_obj : McnInput
            Contain input formation for mechanical solver
        rdf_coef_obj : RdfCoef
            Contain hydrodynamic coefficients
        """
        self.mcn_input_obj = mcn_input_obj
        self.rdf_coef_obj  = rdf_coef_obj




    def solve(self,output="motion"):
        '''
        Solves the mechanical equation
        Parameters
        ----------
        output : str
            What to return?
            "motion"   : return a array of motion in cog
            "mcn_coef" : return a McnCoef object 
        Returns
        -------
        mcn_coef_obj : McnCoef
            Contain hydrodynamic coefficients and resolved 
            mechanic property 

        '''

        logger.info('> Solve motion equation')
        mcn_input_obj = self.mcn_input_obj
        rdf_coef_obj  = self.rdf_coef_obj
        amplitude  = mcn_input_obj.amplitude
        motion = rdf_coef_obj.new_vars("motion","dynamic_uncoupled",dtype="complex64")
        stiffness_matrix =  rdf_coef_obj.new_vars("hydrostatic","static_6x6DoF")  
        mass     = mcn_input_obj.mass 
        #gyration_radius = mcn_input_obj.gyration_radius  # not needed?

        rho = rdf_coef_obj.rho
        g   = rdf_coef_obj.g
        speed   = rdf_coef_obj.speed
        depth   = rdf_coef_obj.depth
        head    = rdf_coef_obj.heading.data
        wrps    = rdf_coef_obj.frequency.data
        we      = rdf_coef_obj.encounter_frequency.data
        nb_body = rdf_coef_obj.nb_body
        if nb_body >1:
            raise NotImplementedError("This MechanicalSolver can't handle multibody calculation yet")

        # Set ref_point de rdf_coef_obj to cog_point
        rdf_coef_obj.ref_point = mcn_input_obj.cog_point

        # Attention, hardcoding nb_body = 1
        rdf_coef_obj_sel  = rdf_coef_obj.sel(body=1,body_i=1,body_j=1)
        mcn_input_obj_sel = mcn_input_obj.sel(body=1,body_i=1,body_j=1)

        cog_point   = mcn_input_obj_sel.cog_point.data
        cob_point   = rdf_coef_obj_sel.cob_point.data
        mass_matrix = mcn_input_obj_sel.mass_matrix.data

        # Stiffness
        # add gravity stiffness
        gravity_stiffness = np.zeros((6,6), dtype='float64')
        gravity_stiffness[3,3] = gravity_stiffness[4,4] = (+cog_point[2] - cob_point[2])
        gravity_stiffness[3,5] = -cog_point[0] + cob_point[0]
        gravity_stiffness[4,5] = -cog_point[1] + cob_point[1]
        gravity_stiffness = gravity_stiffness* mass * g

        # Total stiffness
        
        hydrostatic_hull    = rdf_coef_obj_sel.hydrostatic_hull.data 
        base_flow_stiffness = rdf_coef_obj_sel.base_flow_stiffness.data        
        excitation     = rdf_coef_obj_sel.excitation.data
        added_mass     = rdf_coef_obj_sel.added_mass.data
        wave_damping   = rdf_coef_obj_sel.wave_damping.data


        K = hydrostatic_hull + base_flow_stiffness - gravity_stiffness
        if hasattr(mcn_input_obj_sel,'user_stiffness_matrix'):
            K += mcn_input_obj_sel.user_stiffness_matrix.data



        # Quadratic damping
        user_quadratic_damping  = unset_zeros_matrix(getattr(mcn_input_obj_sel,'user_quadratic_damping',None))

        user_damping_matrix_rel = unset_zeros_matrix(getattr(mcn_input_obj_sel,'user_damping_matrix_rel',None))
        
        user_damping_matrix_abs = getattr(mcn_input_obj_sel,'user_damping_matrix_abs',np.zeros((6,6),dtype='float'))


        r1st = np.zeros( (len(head), len(wrps), 6), dtype = 'complex' )

        tol = 1e-3
        itmax = 100
        linParam = 8./(3.*np.pi) * amplitude

        stiffness_matrix.loc[{"body":1}] = K
        M = np.zeros((6,6),dtype='float')
        B = np.zeros((6,6),dtype='float')
        

        for i_head,headval in enumerate(head):

            for i_freq,freqval in enumerate(wrps):
                logger.info(f'freq = {freqval:6.3f} (rad/s) \t speed = {speed:5.2f} (m/s) \t head = {headval:4.2f} (degree)')

                xtmp  = np.zeros(6,dtype = 'complex')
                error = 1.0
                it = 0

                while ( error > tol and it <= itmax ) :

                    it +=1

                    f      = we[i_head,i_freq]
                    M[:,:] = added_mass[i_head, i_freq, : ,:]+ mass_matrix 
                    B[:,:] = wave_damping[i_head, i_freq, :, :] + user_damping_matrix_abs 

                    if user_damping_matrix_rel is not None:
                        bcr = 2.0 * np.sqrt( np.abs( M * K ) )
                        B += 0.01 * user_damping_matrix_rel * bcr



                    Bq = np.zeros((6,6))
                    if user_quadratic_damping is not None:
                        for k in range(6):
                                Bq[k,:] =  linParam * f * user_quadratic_damping[k,:] * np.abs( xtmp[k] )
                    lhs = (- f**2 * M + 1j * f * ( B + Bq ) + K)
                    rhs = excitation[i_head, i_freq,:]


                    r1st[i_head, i_freq, :] = X = np.linalg.solve(lhs,rhs)
                    motion.loc[{"body":1,"frequency":freqval,"heading":headval}] = X
                    if user_damping_matrix_rel is not None:
                        error   =  np.abs(r1st[i_head, i_freq, :] - xtmp).max()
                        xtmp[:] = 0.9 * r1st[i_head, i_freq, :] + 0.1*xtmp[:]
                    else: # no quadtratic loop : exit iteration
                        break
        if output == "mcn_coef":
            # Get all info from rdf_coef_obj
            datadict = rdf_coef_obj.explicit_dict
            # Add mass info and motion result
            datadict["motion"]      = motion.data
            datadict["hydrostatic"] = stiffness_matrix.data
            datadict["cog_point"]   = mcn_input_obj.cog_point.data
            datadict["mass_matrix"] = mcn_input_obj.mass_matrix.data
            datadict["mass_matrix"] = mcn_input_obj.mass_matrix.data
            datadict["unexpected_keywords"] = "ignore"
            output = McnCoef.FromDict(datadict)
            return output
        elif output == "motion":
            return motion.data
        else:
            raise RuntimeError(f"Unexpected output request: {output}!")

    def getWetModes(self):

        '''
        Computes body wet frequencies and modes

        Returns
        -------
        None.

        '''

        wr   = np.zeros( (len(self.head), len(self.wrps), 6))
        vect = np.zeros( (len(self.head), len(self.wrps), 6, 6))

        k = self.stiffness_matrix
        # solve eigenvalue problem for all frequencies and heading
        for i_head in range(len(self.head)):

            for i_freq in range(len(self.wrps)):

                M = self.added_mass[i_head, i_freq, : ,:] + self.massMatrix

                #Minv = np.linalg.inv(M)
                #matA = np.matmul( Minv , K + 0.01 * (EPS**2) * np.diag(M) )
                #w2, v = np.linalg.eig( matA )

                w2, v = eigh (a = K + 0.01 * (EPS**2) * np.diag(M) , b = M )


                wr[i_head, i_freq, :] = np.sqrt( np.abs(w2) )
                vect[ i_head , i_freq , : , :] = v.real


        wetFreq  = np.zeros(6)
        wetModes = np.zeros((6,6))

        # sort unique encounter frequencies
        x  = self.we[:,:].reshape(-1)
        xu, idu = np.unique( x , return_index = True )
        ids = np.argsort( xu )
        xs  = xu[ids]

        # compute wet frequencies and and wet modes
        for imod in range(6):

            # get eigenvalues
            yu   = wr[:,:,imod].reshape(-1)[idu]
            ys   = yu[ids]

            funcFreq = lambda w : interpolate.interp1d(xs, ys, bounds_error = False , fill_value = (ys[0], ys[-1] ) )(w) - w

            wetFreq[imod] = optimize.fsolve(func=funcFreq, x0 = xs[0])

            # get eigenvectors
            v  = vect[ : , : , : , imod].reshape(-1, vect.shape[-2]).T
            vu = v[:,idu]
            vs = vu[:,ids]

            funcVect = interpolate.interp1d( xs , vs , bounds_error = False , fill_value = (vs[:,0], vs[:,-1] ) )

            wetModes[:,imod] = funcVect( wetFreq[imod] )
            wetModes[:,imod] = wetModes[:,imod] / np.linalg.norm( wetModes[:,imod]  )


        # sort
        idmod    = np.argsort( wetFreq )
        wetFreq  = wetFreq[idmod]
        wetModes = wetModes[:,idmod]

        logger.info('\n')
        logger.info('----------------------------------------------------')
        logger.info('WET FREQUENCIES AND MODES')
        logger.info('----------------------------------------------------')
        for imod in range(6):
            logger.info(f' > Wet mode : {imod+1}')
            logger.info(f'Frequency : {wetFreq[imod]:.3f} (rad/s)')
            logger.info('Decomposition:')
            logger.info(f"{ np.array2string(wetModes[:,imod], formatter={'float_kind':'{0:.3f}'.format}) }")
            logger.info('----------------------------------------------------')




        return wetFreq, wetModes


    def writeRaos(self, rao_path):
        '''
        write motions and hydrdoynamic forces RAOs (after solving
        the mechanical equation)

        Parameters
        ----------
        path : string
            Raos output path

        Returns
        -------
        None.

        '''
        def write_rao(cvalue):
            rao =  sp.Rao(b = np.deg2rad(self.head) ,
                          w = self.wrps,
                          cvalue = cvalue,
                          refPoint = self.cog_point,
                          waveRefPoint = np.array([0.,0.]), # to check in hydrostar-v
                          depth = self.depth,
                          forwardSpeed = self.speed,
                          modes = np.array([irao]),
                          rho = self.rho,
                          grav = self.grav )

            rao.write( rao_path + f'/{fname}' + '.rao' )

        if not os.path.exists(rao_path):
            os.mkdir(rao_path)

        data = {'fext': self.excitation,
                'motion': self.r1st,
                'cm': self.added_mass,
                'ca':self.wave_damping}

        for name, value in data.items():
            for imod in range(6):
                offset = 0
                if name in ['fext','motion']: # motion or excitation forces
                    cvalue = value[:,:,imod:imod+1]
                    if (name == 'motion' and imod > 2): # convert rotations to degree
                        cvalue = cvalue * np.rad2deg(1.)
                    if name == 'fext':
                        offset = 6
                    irao = imod + 1 + offset
                    fname = sp.modesIntToMode(irao).name.lower()
                    cvalue = -1j * np.conj(cvalue)
                    write_rao(cvalue)
                else: # hydrodynamic coefficients
                    for jmod in range(6):
                        cvalue = value[:,:,imod:imod+1,jmod]
                        irao = 0
                        fname = f'{name}_{imod+1}{jmod+1}'
                        write_rao(cvalue)




class HydroStarVMechanics(MechanicalSolver):

    def __init__(self, inputJSON) :
        """Initialization with HydroStarV input

        Parameters
        ----------
        inputJSON : str
            path to input of hydrostarV
        """
        rdf_coef_obj = RdfCoef.Read(inputJSON)
        mcn_input_obj = McnInput.Read(inputJSON)
        super().__init__(mcn_input_obj  = mcn_input_obj,
                         rdf_coef_obj   = rdf_coef_obj)



class HydroStarMechanics(MechanicalSolver):

    def __init__(self, hdf_file,input_mcn_file):
        """Initialization with HydroStar hdf fileoutput
        Parameters
        ----------
        hdf_file : str
            path to hdf output file of hsrdf
        input_mcn_file : str
            path to .mcn input file of hsmcn
        """

        rdf_coef_obj = RdfCoef.Read(hdf_file)
        mcn_input_obj = McnInput.Read(input_mcn_file)
        super().__init__(mcn_input_obj  = mcn_input_obj,
                         rdf_coef_obj   = rdf_coef_obj)



if __name__ == '__main__':

    test = False

    if test:

        # test both options to define body inertia

        hstat_db_path = r"D:\hstar_v\cases_dev\S60_hydrostatic_export\RESULT"
        hydroCoeff_db_path = r"D:\hstar_v\cases\S60\S60_Fn02_Refined\RESULT\HarmonicFlow_DB"


        ms = HydroStarVMechanics(hstat_db_path = hstat_db_path,
                                 hydroCoeff_db_path = hydroCoeff_db_path,
                                 mass = 1.94199E+08,
                                 cog_point = np.array([148.601, 0.000, -4.343]),
                                 gyration_radius = np.array([15.750, 69.148, 70.889, 0.000, 3.524, 0.000]))

        # ms2 = MechanicalSolver(hstat_db_path = hstat_db_path,
        #                       hydroCoeff_db_path = hydroCoeff_db_path,
        #                       cog_point = np.array([148.601, 0.000, -4.343]), mass_matrix = ms.mass_matrix )


        #ms.solve()
