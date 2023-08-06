#!/usr/bin/env python3
from Snoopy.Mechanics import HydroCoefABC
from Snoopy import logger
import numpy as np
import xarray as xa

class McnCoef(HydroCoefABC):
    data_vars_requirement = ['hydrostatic','excitation','added_mass',
                             'wave_damping','cog_point','motion','mass_matrix']
    data_vars_optional    = ['base_flow_stiffness','cob_point',
                             'ref_point','ref_wave']
    coords_requirement    = ['heading','frequency']
    coords_optional       = ['body','body_i','body_j',
                             'mode','mode_i','mode_j','xyz','xy']
    attrs_requirement     = ['speed']
    attrs_optional        = ['version','software','nb_body',
                             'nb_mode','depth','g','rho',
                             'input_file_hash','input_file',
                             'executable_hash','executable']
    matrans_list          = ['hydrostatic',
                             'base_flow_stiffness','excitation',
                             'added_mass','wave_damping']
    @classmethod
    def Build(cls,  nb_body             = 1,
                    nb_mode             = 6,
                    cob_point           = None,
                    cog_point           = None,
                    ref_point           = None,
                    ref_wave            = None,
                    hydrostatic         = None,
                    base_flow_stiffness = None,
                    excitation          = None,
                    added_mass          = None,
                    added_mass_inf      = None,
                    mass_matrix         = None,
                    motion              = None,
                    wave_damping        = None,
                    heading             = None,
                    frequency           = None,
                    mode                = None,
                    mode_i              = None,
                    mode_j              = None,
                    body                = None,
                    body_i              = None,
                    body_j              = None,
                    speed               = None,
                    depth               = 0,
                    version             = 0,
                    g                   = 9.81,
                    rho                 = 1025.,
                    software            = "Unknown",
                    return_object       = True,
                    xyz                 = ["x","y","z"],
                    xy                  = ["x","y"],
                    solver_version      = "unknown",
                    solver_commit       = "unknown",
                    executable          = "unknown",
                    executable_hash     = "unknown",
                    input_file          = "unknown",
                    input_file_hash     = "unknown",
                    file_type           = "unknown",
                    unexpected_keywords = "raise",
                    **kwargs):
        """Constructor, with explicit signature

        Parameters
        ----------
        nb_body : int
            number of body, optional, default = 1

        nb_mode : int
            numbrer of mode, optional, default = 6

        cog_point : numpy.array or list or xarray.DataArray
            Center of gravity, dimension : [nbBody,3]

        ref_point : numpy.array or list or xarray.DataArray
            Reference point, dimension : [nbBody,3]
            Optional, default value: cog_point

        ref_wave : numpy.array or list or xarray.DataArray
            Origin of wave phase in surface, dimension : [2,],
            Optional, default = [0,(ref_point[0],ref_point[1])]

        heading    : numpy.array or list or xarray.DataArray
            ship heading, in radian, dimension [nb_head,]

        frequency  : numpy.array or list or xarray.DataArray
            frequency of problem, dimension [nb_freq,]


        mode   : numpy.array or list or xarray.DataArray
            name of mode, dimension [nb_mode,]
            Optional, default : np.arange(1,nb_mode+1,dtype='int')

        mode_i   : numpy.array or list or xarray.DataArray
            name of influencing mode, dimension [nb_mode_i,]
            Optional, default : np.arange(1,nb_mode+1,dtype='int')

        mode_j   : numpy.array or list or xarray.DataArray
            name of influenced mode, dimension [nb_mode_j,]
            Optional, default : np.arange(1,nb_mode+1,dtype='int')

        body     : numpy.array or list or xarray.DataArray
            name of body, dimension [nb_body,]
            Optional, default : np.arange(1,nb_body+1,dtype='int')

        body_i   : numpy.array or list or xarray.DataArray
            name of influencing body, dimension [nb_body_i,]
            Optional, default : np.arange(1,nb_body+1,dtype='int')

        body_j   : numpy.array or list or xarray.DataArray
            name of influenced mode, dimension [nb_body_j,]
            Optional, default : np.arange(1,nb_body+1,dtype='int')

        speed   : float
            advancing speed [m/s]

        depth : float
            depth [m].
            Optional, default = 0.
            Attention, Depth = 0. mean Depth = infitity

        hydrostatic : numpy.array or list or xarray.DataArray
            hydrostatic stiffness total, dimension ["body","mode_i","mode_j"]
            hydrostatic = hydrostatic_hull + hydrostatic_grav

        base_flow_stiffness : numpy.array or list or xarray.DataArray
            stiffness caused by steady flow, dimension ["body","mode_i","mode_j"]
            Optional, default: numpy.zeros((nb_body,nb_mode,nb_mode))

        excitation : numpy.array or list or xarray.DataArray
            excitation force, dimension
            ["body","mode","heading","frequency"]

        added_mass : numpy.array or list or xarray.DataArray
            added mass in radiation problem, dimension
            ["body_i","body_j","mode_i","mode_j","heading","frequency"]

        wave_damping : numpy.array or list or xarray.DataArray
            wave damping in radiation problem, dimension
            ["body_i","body_j","mode_i","mode_j","heading","frequency"]

        xyz : list of numpy.array
            label for coordinate
            Optional, default = ['x','y','z']

        xy : list of numpy.array
            label for coordinate for point on free surface
            Optional, default = ['x','y']


        ReturnObject: bool
            True    : return constructed object
            False   : return only xarray

        unexpected_keywords : str
            Decide what to do when encounter unexpected keywords
            - "ignore": do nothing
            - "warning": print a warning
            - "raise": raise a TypeError exception
        Returns
        -------
            output : RdfCoef or xarray
                if ReturnObject == True: return RdfCoef
                if ReturnObject == False: return xarray
        """
        # Requirements
        assert cog_point is not None             , 'cog_point must be given'
        assert heading is not None               , 'heading must be given'
        assert frequency is not None             , 'frequency must be given'
        assert excitation is not None            , 'excitation must be given'
        assert added_mass is not None            , 'addedMass must be given'
        assert wave_damping is not None          , 'wave_damping must be given'
        assert hydrostatic is not None           , 'hydrostatic must be given'
        assert mass_matrix is not None           , 'mass_matrix must be given'

        # Optional:
        body   = cls.default_labeling(body,nb_body)
        body_i = cls.default_labeling(body_i,nb_body)
        body_j = cls.default_labeling(body_j,nb_body)
        mode   = cls.default_labeling(mode,nb_mode)
        mode_i = cls.default_labeling(mode_i,nb_mode)
        mode_j = cls.default_labeling(mode_j,nb_mode)

        if base_flow_stiffness is None:
            base_flow_stiffness = np.zeros((nb_body,nb_mode,nb_mode),dtype='float64')

        if ref_point is None:
            ref_point = np.array(cog_point)

        if ref_wave is None:
            ref_wave = np.array(ref_point[0,:2])

        this_version = cls.version
        data_vars = {
            'hydrostatic'          : (cls.static_6x6DoF_dims, hydrostatic),
            'base_flow_stiffness'  : (cls.static_6x6DoF_dims, base_flow_stiffness),
            'excitation'           : (cls.dynamic_uncoupled_dims, excitation),
            'motion'               : (cls.dynamic_uncoupled_dims, motion),
            'added_mass'           : (cls.dynamic_coupled_dims, added_mass) ,
            'wave_damping'         : (cls.dynamic_coupled_dims, wave_damping),
            'ref_point'            : (cls.notable_point_dims,ref_point),
            'cog_point'            : (cls.notable_point_dims,cog_point),
            'ref_wave'             : (['xy'],ref_wave),
            'mass_matrix'          : (cls.static_6x6DoF_dims, mass_matrix)}
            #'encounter_frequency'  : (cls.dynamic_only_dims, encounter_frequency)}
            #'wave_length'           : (["Frequency"], wave_length)}


        coords = {  'body'      : body,
                    'body_i'    : body_i,
                    'body_j'    : body_j,
                    'mode'      : mode,
                    'mode_i'    : mode_i,
                    'mode_j'    : mode_j,
                    'heading'   : heading,
                    'frequency' : frequency,
                    'xyz'       : xyz,
                    'xy'        : xy}

        attrs  = {'speed'       : speed,
                  'depth'       : depth,
                  'rho'         : rho,
                  'g'           : g,
                  'nb_mode'     : nb_mode,
                  'nb_body'     : nb_body,
                  'version'     : version,
                  'software'    : software,
                  'solver_version'  : solver_version,
                  'solver_commit'   : solver_commit,
                  'executable'      : executable,
                  'executable_hash' : executable_hash,
                  'input_file'      : input_file,
                  'input_file_hash' : input_file_hash,
                  'file_type'       : file_type}

        xarrayOutput = xa.Dataset(data_vars = data_vars,coords=coords,attrs=attrs)
        if len(kwargs)>0:
            if unexpected_keywords == "warning":
                logger.info(f"Ignore unexpected keywords: {kwargs.keys()}")
            elif unexpected_keywords == "raise":
                raise TypeError(f"Unexpected keywords: {kwargs.keys()}")
        if return_object:
            return cls(xarrayOutput)
        else:
            return xarrayOutput
