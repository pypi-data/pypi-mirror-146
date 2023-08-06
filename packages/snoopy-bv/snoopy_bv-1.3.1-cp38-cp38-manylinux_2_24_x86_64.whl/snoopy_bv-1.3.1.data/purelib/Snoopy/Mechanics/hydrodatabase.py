#!/usr/bin/env python3
import xarray as xa
import numpy as np
import json
from Snoopy.Mechanics import RdfCoef,McnCoef,McnInput,MechanicalSolver
from os.path import abspath,dirname,isfile
class HydroDatabase:
    """Database for all hydrodynamic object.
    Currently can hold 3 attributes corresponding to 3 class of objects 
    (could be extended for more)    
    rdf_coef : RdfCoef object 
        hold all the hydrodynamics results, mass is not know
    mcn_input: McnInput object
        hold all the user input of mass property
    mcn_coef : McnCoef object 
        hold all the hydrodynamics, mass property and resolved motion. 
    
    If mcn_coef is present (not being None), that mean the mechanincal 
    equation is already resolved, and we have access to the motion.

    If mcn_coef is not present (being None), it can be created if rdf_coef 
    and mcn_input is present and then the motion can be obtained through 
    solving the mechanical equation. If rdf_coef or mcn_input is not present, 
    an error will be raised. Otherwise, mcn_coef object will be automatically 
    created. 
    """
    _RdfCoef = RdfCoef
    _McnCoef = McnCoef
    _McnInput = McnInput
    def __init__(self,  rdf_coef     = None,
                        mcn_coef     = None,
                        mcn_input    = None,
                        solver       = "HydroStar"):
        """Initialization: register rdf_coef, mcn_coef mcn_input
        and solver name as properties in object.
        The properties can be None.
        Parameters
        ----------
        rdf_coef : RdfCoef 
            hold all the hydrodynamics results, mass is not know
        mcn_input: McnInput 
            hold all the user input of mass property
        mcn_coef : McnCoef 
            hold all the hydrodynamics, mass property and resolved motion. 
        solver   : str
            distinguish between HydroStar and HydroStarV
        """        
        self.rdf_coef    = rdf_coef
        self.mcn_coef    = mcn_coef
        self.mcn_input   = mcn_input
        self.solver      = solver
    @classmethod
    def InitHydrostarV(cls,jsonInput):
        """Special initialization for HydroStarV
        Parameters
        ----------
        jsonInput : str
            path to json input file

        Returns
        -------
        HydroDatabase
            HydroDatabase object 
        """
        with open(jsonInput) as fID:
            metadata = json.load(fID)
            metadata["inputPath"] = jsonInput
            metadata["folderPath"] = dirname(abspath(jsonInput))

        out = cls(  rdf_coef  = RdfCoef.Read_JSON(metadata),
                    mcn_input = McnInput.Read_JSON(metadata),
                    solver    = "HydroStarV")
        out.metadata = metadata
        mcnoutputfile = metadata["mechanicalInput"].get("output_mcn","hvmcn.h5")
        if isfile(mcnoutputfile):
            # If output file is present, that mean hvmcn is already ran, 
            # we just import the data
            try:
                out.mcn_coef = mcnoutputfile
            except KeyError:
                print(f'Attempt to read McnCoef from file {mcnoutputfile} failed! ')
                out.mcn_coef = None
            
        return out        
    #---------------------------------------------------#
    # Properties                                        #
    #---------------------------------------------------#
    @property
    def database(self):
        """Shortcut point to either mcn_object or rdf_object.
        If mcn_object present, it will be returned
        Otherwise, if rdf_object is present, it will be returned
        An error will be raise if neither is present.

        Returns
        -------
        McnCoef or RdfCoef
            _description_
        """
        if self.has_mcn:
            return self.mcn_coef
        elif self.has_rdf:
            return self.rdf_coef
        else:
            raise AttributeError("No data found in object")
    @property
    def mechanical_solver(self):
        """Build an mechanical solver

        Returns
        -------
        MechanicalSolver
            Solve motion equation
        """
        if not hasattr(self, "_mechanical_solver"):
            self._mechanical_solver = \
                MechanicalSolver(mcn_input_obj = self.mcn_input,
                                 rdf_coef_obj  = self.rdf_coef )
        return self._mechanical_solver
    @property
    def motion(self):
        """Motion
        If mcn_coef object is present, motion should be present in 
        this database, so this function simply extract motion from
        mcn_coef object
        Otherwise, rdf_coef and mcn_input must present, this method
        will call the method compute_motion, which will build an 
        mechanical solver and solve the mechanical equation.
        Returns
        -------
        array_like
            Motion on cog_point

        """
        if hasattr(self,"_motion"):
            return self._motion
        elif self.has_mcn:
            return self.mcn_coef.motion
        elif self.has_rdf and self.has_mcn_input:
            self._motion = self.compute_motion()
            return self._motion
        else:
            raise AttributeError("Not enough information to produce motion output")
    def compute_motion(self):
        """Forcefully compute the motion 
        Ignore data in mcn_coef, need rdf_coef and mcn_input
        Returns
        -------
        array_like
            Motion on cog_point
        """
        return self.mechanical_solver.solve(output="motion")
    #---------------------------------------------------#
    # RdfCoef object                                    #
    #---------------------------------------------------#
    @property
    def has_rdf(self):
        """Check if rdf_coef is present

        Returns
        -------
        bool
            True if rdf_coef is present
        """
        return getattr(self,"_rdf_coef",None) is not None

    def _get_rdf_coef(self):
        """Build a RdfCoef object
        This class is not able to build a RdfCoef, so an error
        will be directly raised. This behavior could be overrided 
        by the child classes
        Raises
        ------
        AttributeError
            Will always raise error
        """
        raise AttributeError("Rdf data not found")

    @property
    def rdf_coef(self):
        """Return _rdf_coef if present
        Otherwise return the output of method _get_rdf_coef

        Returns
        -------
        RdfCoef
            Rdf results
        """
        if not hasattr(self,"_rdf_coef"):
            self._rdf_coef = self._get_rdf_coef()
        return self._rdf_coef

    @rdf_coef.setter
    def rdf_coef(self,data):
        """Set the rdf_coef
        Mainly do the data conform check and conversion of 
        older database version or Fortran->Python data conversion
        Parameters
        ----------
        data : any
            str: expect a path to hdf file, will perform Read method
            xarray: do the checking and all conversions
            RdfCoef : do the conversion from older format if needed
        """
        self._rdf_coef = RdfCoef.Initialize(data)

    #---------------------------------------------------#
    # McnCoef object                                    #
    #---------------------------------------------------#
    @property
    def has_mcn(self):
        """Check if mcn_coef is present
        Returns
        -------
        bool
            True if mcn_coef is present
        """
        return getattr(self,"_mcn_coef",None) is not None

    def _get_mcn_coef(self):
        """Build McnCoef object
        Check if mcn_input and rdf_coef is present
        If yes, process to solve the mechanical equation 
        and store everything in McnCoef format
        Returns
        -------
        McnCoef
            Hydrodynamic and mechanic results

        """
        if self.has_mcn_input and self.has_rdf:
            ms = MechanicalSolver(self.mcn_input,self.rdf_coef)
            self._mcn_coef = ms.solve(output="mcn_coef")
            return self._mcn_coef
        else:
            raise AttributeError('Mcn data not found')

    @property
    def mcn_coef(self):
        """Return stored _mcn_coef
        If not present, call the function _get_mcn_coef and
        return it output

        Returns
        -------
        McnCoef
            Hydrodynamic and mechanic results
        """
        if getattr(self,"_mcn_coef",None) is None:
            self._mcn_coef = self._get_mcn_coef()
        return self._mcn_coef


    @mcn_coef.setter
    def mcn_coef(self,data):
        """Set the mcn_coef object
        Mainly do the data conform check and conversion of 
        older database version or Fortran->Python data conversion
        Parameters
        ----------
        data : any
            str: expect a path to hdf file, will perform Read method
            xarray: do the checking and all conversions
            McnCoef : do the conversion from older format if needed
        Parameters
        -------
        McnCoef
            Hydrodynamic and mechanic results
        """
        self._mcn_coef = McnCoef.Initialize(data)

    #---------------------------------------------------#
    # McnCoef object                                    #
    #---------------------------------------------------#
    @property
    def has_mcn_input(self):
        """Check if mcn_input is present
        Returns
        -------
        bool
            True if mcn_input is present
        """
        return getattr(self,"_mcn_input",None) is not None

    def _get_mcn_input(self):
        """Build a RdfCoef object
        This class is not able to build a McnInput, so an error
        will be directly raised. This behavior could be overrided 
        by the child classes
        Raises
        ------
        AttributeError
            Will always raise error
        """
        raise AttributeError("Mcn input not found")

    @property
    def mcn_input(self):
        """Return stored _mcn_input
        If not present, call the function _get_mcn_input and
        return it output

        Returns
        -------
        McnInput
            Mechanic input
        """        
        if not hasattr(self,"_mcn_input"):
            self._mcn_input = self._get_mcn_input()
        return self._mcn_input

    @mcn_input.setter
    def mcn_input(self,data):
        """Set the mcn_input 
        Mainly do the data conform check and conversion of 
        older database version or Fortran->Python data conversion
        Parameters
        ----------
        data : any
            str: expect a path to hdf file, will perform Read method
            xarray: do the checking and all conversions
            McnInput : do the conversion from older format if needed
        """
        self._mcn_input = McnInput.Initialize(data)

