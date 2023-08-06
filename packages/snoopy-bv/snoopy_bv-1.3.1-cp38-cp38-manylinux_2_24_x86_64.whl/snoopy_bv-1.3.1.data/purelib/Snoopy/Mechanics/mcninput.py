#!/usr/bin/env python3
from Snoopy.Mechanics import HydroCoefABC
from Snoopy import logger
import os
import numpy as np
from Snoopy.Reader.input_mcn_parser import parse_input_mcn
import xarray as xa
import json

class McnInput(HydroCoefABC):
    """
    """
    data_vars_requirement = ['cog_point']
    data_vars_optional    = ['mass_matrix','user_damping_matrix_rel',
                             'user_damping_matrix_abs','user_quadratic_damping',
                             'user_stiffness_matrix']
    coords_requirement    = []
    coords_optional       = ['body','body_i','body_j',
                             'mode','mode_i','mode_j','xyz']
    attrs_requirement     = []
    attrs_optional        = ['mass','gyration_radius','nb_body',
                             'nb_mode','amplitude','file_type']
    @classmethod
    def Read(cls,inputFile):
        """ Parser/constructor
        Read a input mcn file and produce a McnInput object.
        This method override the Read method of HydroCoefABC
        This is intentional since the only way to read this
        object is to parse the input.mcn file
        If a json file is given (format HydrostarV), the routine 
        will try to find path of input mcn file and read it
        Parameters
        ----------
            inputFile : str
                path to input.mcn file or jsonfile
        Returns
        -------
            output : McnInput object
        """
        if inputFile.endswith(".mcn"):
            return cls.Build(version=cls.version,**parse_input_mcn(inputFile))
        elif inputFile.endswith(".json"):
            return cls.Read_JSON(inputFile)

    @classmethod
    def Read_JSON(cls, inputdata):
        """Extract informations that needed to create mcn_input 
        from HydroStarV format. For now, we expect to obtain a 
        path to input.mcn file and parse the data from input.mcn 
        file
        Parameters
        ----------
        inputdata : str or dict
            path to json file or dictionary of already parsed json file
        Returns
        -------
        -------
            output : McnInput object
        """
        if isinstance(inputdata,str):
            with open(inputdata,"r") as fid:
                data = json.load( fid )
            cwd = os.path.dirname(os.path.abspath(inputdata))
        elif isinstance(inputdata,dict):
            data = inputdata
            cwd  = data.get("folderPath","./")
        else:
            raise TypeError(f"Invalid input type for Read_JSON: {type(inputdata)}")
        assert "mechanicalInput" in data, "Can't find mechanical input information in json file"
        mcnfile = os.path.join(cwd,data["mechanicalInput"].get("input_mcn","input.mcn"))
        return cls.Build(version=cls.version,**parse_input_mcn(mcnfile))

    @classmethod
    def Build(cls,  nb_body             = 1,
                    nb_mode             = 6,
                    cog_point           = None,
                    mass                = None,
                    mass_matrix         = None,
                    gyration_radius     = None,
                    quadratic_damping   = None,
                    viscous_damping     = None,
                    amplitude           = 1,
                    return_object       = True,
                    mode                = None,
                    mode_i              = None,
                    mode_j              = None,
                    body                = None,
                    body_i              = None,
                    body_j              = None,
                    xyz                 = ["x","y","z"],
                    version             = None,
                    user_damping_matrix_abs = None,
                    user_damping_matrix_rel = None,
                    user_stiffness_matrix   = None,
                    user_quadratic_damping  = None,
                    unexpected_keywords     = "raise",
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

        xyz : list of numpy.array
            label for coordinate
            Optional, default = ['x','y','z']

        unexpected_keywords : str
            Decide what to do when encounter unexpected keywords
            - "ignore": do nothing
            - "warning": print a warning
            - "raise": raise a TypeError exception

        ReturnObject: bool
            True    : return constructed object
            False   : return only xarray

        Returns
        -------
            output : McnInput object or xarray.Dataset object
                if ReturnObject == True: return McnInput
                if ReturnObject == False: return xarray.Dataset
        """
        assert cog_point is not None, 'cog_point must be given'

        if mass_matrix is None:
            assert mass is not None , \
                'If mass_matrix is not present, mass must be given'
            assert gyration_radius is not None ,\
                'If mass_matrix is not present, mass must be given'
            assert nb_mode == 6, "We can't assemble non standard mass matrix"
            mass_matrix = np.zeros((nb_body,6,6),dtype='float64')
            for ibody in range(nb_body):
                gyration_radius = np.asarray(gyration_radius)
                mass_matrix[ibody,:3,:3] = mass[ibody] * np.eye(3)
                mass_matrix[ibody,3:,3:] = mass[ibody] * np.diag(gyration_radius[ibody,:3]**2)
                mass_matrix[ibody,3,4:]  = mass[ibody] * gyration_radius[ibody,3:5] \
                                            * np.abs(gyration_radius[ibody,3:5])
                mass_matrix[ibody,4,5]   = mass[ibody] * gyration_radius[ibody,5]  \
                                            * np.abs(gyration_radius[ibody,5])
                # symmetrise
                mass_matrix[ibody,4:,3]  = mass_matrix[ibody,3,4:]
                mass_matrix[ibody,5,4]   = mass_matrix[ibody,4,5]
        else:
            mass = np.zeros((nb_body,),dtype='float64')
            gyration_radius = np.zeros((nb_body,6),dtype='float64')
            for ibody in range(nb_body):
                mass[ibody] = mass_matrix[0,0]
                gyration_radius[ibody,:3]  = np.sqrt(np.diag(mass_matrix[ibody,3:,3:]) / mass[ibody])
                gyration_radius[ibody,3:5] = np.sign(mass_matrix[ibody,3,4:])* np.sqrt(np.abs(mass_matrix[ibody,3,4:]) / mass[ibody])
                gyration_radius[ibody,5]   = np.sign(mass_matrix[ibody,5,4]) * np.sqrt(np.abs(mass_matrix[ibody,5,4]) / mass[ibody])

        # Optional variable:
        body   = cls.default_labeling(body,nb_body)
        body_i = cls.default_labeling(body_i,nb_body)
        body_j = cls.default_labeling(body_j,nb_body)
        mode   = cls.default_labeling(mode,nb_mode)
        mode_i = cls.default_labeling(mode_i,nb_mode)
        mode_j = cls.default_labeling(mode_j,nb_mode)

        data_vars = {'mass_matrix' : (cls.static_6x6DoF_dims, mass_matrix),
                     'cog_point'   : (cls.notable_point_dims,cog_point)}

        if user_damping_matrix_rel is not None:
            data_vars['user_damping_matrix_rel'] = (cls.static_coupled_dims, user_damping_matrix_rel)

        if user_damping_matrix_abs is not None:
            data_vars['user_damping_matrix_abs'] = (cls.static_coupled_dims, user_damping_matrix_abs)

        if user_stiffness_matrix is not None:
            data_vars['user_stiffness_matrix'] = (cls.static_coupled_dims, user_stiffness_matrix)

        if user_quadratic_damping is not None:
            data_vars['user_quadratic_damping'] = (cls.static_coupled_dims, user_quadratic_damping)

        coords = {  'body'      : body,
                    'body_i'    : body_i,
                    'body_j'    : body_j,
                    'mode'      : mode,
                    'mode_i'    : mode_i,
                    'mode_j'    : mode_j,
                    'xyz'       : xyz}

        if version is None:
            version = cls.version

        attrs  = {'mass'            : mass,
                  'gyration_radius' : gyration_radius,
                  'amplitude'       : amplitude,
                  'nb_mode'         : nb_mode,
                  'nb_body'         : nb_body,
                  'version'         : version}

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
