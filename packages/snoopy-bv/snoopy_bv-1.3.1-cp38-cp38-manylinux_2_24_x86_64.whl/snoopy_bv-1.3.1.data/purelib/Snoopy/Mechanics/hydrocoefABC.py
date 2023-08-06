#!/usr/bin/env python3
import xarray as xa
import numpy as np
import os
import json
from numbers import Number
from .matrans import matrans3,vectran3
from Snoopy.Reader import read_hydrostarV_database
import Snoopy.Mechanics as mcn
from Snoopy.Spectral import w2we,w2l
from Snoopy import logger
class HydroCoefABC:
    """ Base class that wrap around an hdf5/xarray dataset
    """
    version = 100
    # dependant: label of dimension, ordered
    dynamic_coupled_dims   = ['body_i','body_j','heading','frequency',
                              'mode_i','mode_j']
    dynamic_uncoupled_dims = ['body','heading','frequency','mode']
    static_6x6DoF_dims     = ['body','mode_i','mode_j']
    static_coupled_dims    = ['body_i','body_j','mode_i','mode_j']
    dynamic_only_dims      = ['heading','frequency']
    notable_point_dims     = ['body','xyz']
    freesurface_point_dims = ['xy']
    all_dims = {"dynamic_coupled"   : dynamic_coupled_dims,
                "dynamic_uncoupled" : dynamic_uncoupled_dims,
                "static_coupled"    : static_coupled_dims,
                "static_6x6DoF"     : static_6x6DoF_dims,
                "dynamic_only"      : dynamic_only_dims,
                "notable_point"     : notable_point_dims,
                'freesurface_point' : freesurface_point_dims}
    all_coords = {'body','body_i','body_j','heading','frequency','mode','mode_i','mode_j','xyz','xy'}
    # type of dependant: all variable is grouped depending on its dimension
    variable_dynamic_coupled    = ['added_mass','wave_damping']
    variable_dynamic_uncoupled  = ['excitation','motion','incident']
    variable_static_6x6DoF      = ['base_flow_stiffness','mass_matrix',
                                   'hydrostatic_hull','hydrostatic']
    variable_static_coupled     = ['user_damping_matrix_rel',
                                   'user_damping_matrix_abs',
                                   'user_quadratic_damping',
                                   'user_stiffness_matrix']
    variable_dynamic_only       = ['encounter_frequency']
    notable_point               = ['cob_point','cog_point','ref_point']
    freesurface_point           = ['ref_wave']
    all_vars = {"dynamic_coupled"   : variable_dynamic_coupled,
                "dynamic_uncoupled" : variable_dynamic_uncoupled,
                "static_6x6DoF"     : variable_static_6x6DoF,
                "static_coupled"    : variable_static_coupled,
                "dynamic_only"      : variable_dynamic_only,
                "notable_point"     : notable_point,
                "freesurface_point" : freesurface_point}

    # list of complex variable need to be combined
    combine_complex       = ['excitation','incident','motion']

    # list of variable need to be translate when ref_point is changed
    matrans_list = []
    # list of variable need to be phase shift when ref_wave is changed
    phase_shift_list = []

    def __init__(self,inputXarray,deepcopy=True):
        """
        Based on xarray.dataset.

        Parameters
        ----------
        inputXarray : xarray or RdfCoef
            contain all the informations

        deepcopy : boolean, optional
            do the deepcopy or not

        """
        self._add_data = {}
        if deepcopy:
            self.data = inputXarray.copy(deep=True)
        else:
            self.data = inputXarray


    #-------------------------------------------#
    # constructors / convertors / readers       #
    #-------------------------------------------#
    @classmethod
    def convertXarray(cls,inputXarray):
        """ Convert any older version of inputXarray to current version
            Parameters
            ----------
            inputXarray : xarray.Dataset
                dataset to be converted

            Returns
            -------
            outputXarray : xarray.Dataset
                dataset converted
        """

        kwargs = {}
        all_info    =(   cls.attrs_requirement
                      + cls.coords_requirement
                      + cls.data_vars_requirement
                      + cls.attrs_optional
                      + cls.coords_optional
                      + cls.data_vars_optional )
        if "version" in all_info:  all_info.remove("version")
        version = getattr(inputXarray,"version",0)
        assert version > 0, 'This reader can only read data base version later than 0'

        for key in all_info:
            val = getattr(inputXarray,key,None) # The usual way
            # Handle exception in preprocessing routine
            val = cls._preprocessing(key,val,inputXarray)
            # Postprocessing and add (key,val) to kwargs
            cls._postprocessing(kwargs,key,val)
        # Impose the version.
        kwargs["version"] = cls.version
        return cls.Build(return_object=False,**kwargs)

    @classmethod
    def _preprocessing(cls,key,val,inputXarray):
        """ Add exceptions!
        """
        if val is not None:  # Data did found in usual way, but need preprocessing
            if key == "user_damping":
                # Exception : because of historical reason,
                # the cross terms in user_damping can't be ouputed
                # The shape in hdf5 is (heading, frequency, body, mode_j, mode_i)
                # while it should be
                # (heading, frequency, body_j, body_i, mode_j, mode_i)
                if not set(val.dims) == set(cls.dynamic_coupled):
                    assert set(val.dims) == {"heading", "frequency", "body", "mode_j", "mode_i"},\
                        f'Unexpected dimensions of user_damping: {val.dims}'
                    if inputXarray.nb_body == 1:
                        # For single body, we can still fix it
                        val = val.rename({'body':'body_i'}).expand_dims("body_j")
                    else:
                        # For multibody, we have to read inputs again to get this
                        raise AttributeError('This version of database do '\
                                            +'not correctly store user_damping')
            elif key == "hydrostatic_hull":
                # Exception: the scaling of hydrostatic is not done in both 
                # hydrostar and hydrostar-V
                if inputXarray.version == 1.:
                    logger.info('Warning! Add scaling to hydrostatic hull')
                    val *= inputXarray.rho * inputXarray.g

        elif val is None: # Data not found in usual way, look for exception
            if key in cls.combine_complex:
                # Exception : since fortran can't output complex data
                # excitation is splitted to real and imaginary part
                # We recombine them here
                real_part = getattr(inputXarray,key+"_re",None)
                img_part  = getattr(inputXarray,key+"_im",None)
                if (real_part is None) or (img_part is None):
                    requirement = (   cls.attrs_requirement 
                                    + cls.coords_requirement
                                    + cls.data_vars_requirement)
                    if key in requirement   : # Only raise error if key is required
                        raise KeyError(f"Missing {key}_re or {key}_im in database")
                else:
                    val = real_part + 1j* img_part
            else:
                # Look for other exceptions, normally, we have none for now!
                pass
        return val

    @classmethod
    def _postprocessing(cls,kwargs,key,val):
        """ Pivot dataset to the imposed dimension order
        of the class, and add non None variable to kwargs.
        usefull when convert fortran output to python
        """
        if isinstance(val,xa.core.dataarray.DataArray):
            found = False
            for type_vars,all_vars in cls.all_vars.items():
                if key in all_vars:
                    kwargs[key] = val.transpose(*cls.all_dims[type_vars]).data
                    found = True
                    break
            if not found:
                if key not in cls.all_coords:
                    logger.info(f"Warning: unrecognized DataArray {key}")
                kwargs[key] = val.data
        elif val is not None:
            kwargs[key] = val
        else:
            if (   (key in cls.attrs_requirement)
                or (key in cls.coords_requirement)
                or (key in cls.data_vars_requirement)):
                raise KeyError(f"Can't find information related to {key} "
                               +"in xarray dataset" )

    @classmethod
    def Initialize(cls,*args,**kwargs):
        """The most generic constructor, wrap around all other constructors
        Take input as:
        - Object of class HydroCoefABC : return as is.
        - Object of class xarray.Dataset : construct with __init__
        - A string : construct with Read
        - A dict   : construct with FromDict
        - Keywords : construct with Build
        - None object: will return None        
        """
        if len(args) == 0:
            return cls.Build(**kwargs)
        elif len(args) == 1:
            input = args[0]
            if input is None:
                return None
            elif isinstance(input,HydroCoefABC):
                return input
            elif isinstance(input,xa.Dataset):
                return cls(input)
            elif isinstance(input,str):
                return cls.Read(input)
            elif isinstance(input,dict):
                return cls.FromDict(input)
            else:
                raise TypeError(f'Unexpect class {type(input)} in constructor.')
        else:
            raise ValueError(f'Unexpected number of argument: {len(args)}')

    



    @classmethod
    def FromDict(cls,dictIn):
        """Constructor direct

        Parameters
        ----------
        dictIn : dict
            Dictionair that contain information to build object

        Returns
        -------
        RdfCoef
            output RdfCoef object
        """
        return cls.Build(**dictIn)



    @classmethod
    def Read_HDF(cls,inputPath):
        """Lecteur and constructor for hydrostar format (hdf5)
        Hydrostar-V might have this ouput format in the future

        Parameters
        ----------
        inputPath : str
            path to hdf5 file

        Returns
        -------
        output : RdfCoef
            output RdfCoef object
        """
        assert os.path.isfile(inputPath), f'File {inputPath} not found!'
        xarraydata = xa.open_dataset(inputPath)
        file_type = getattr(xarraydata,"file_type",None)
        if file_type == "hsrdf output":
            return mcn.RdfCoef(xarraydata,deepcopy=False)
        elif file_type == 'hsmcn output':
            return mcn.McnCoef(xarraydata,deepcopy=False)
        else:
            return cls(xarraydata,deepcopy=False)


    @classmethod
    def Read(cls,inputPath,inputFormat=None):
        """General lecteur and constructor, will guess format

        (if inputFomat= None) or chose the lecteur base on inputFomat

        Parameters
        ----------
        inputPath : str
            path to input.json file

        Returns
        -------
        output : RdfCoef
            output RdfCoef object
        """
        if inputFormat is None:
            inputFormat = cls.guessFormat(inputPath)

        if inputFormat == "JSON":
            return cls.Read_JSON(inputPath)
        elif inputFormat == "HDF":
            return cls.Read_HDF(inputPath)
        else:
            raise RuntimeError(f"Unknown input format : {inputFormat}")



    @classmethod
    def Read_JSON(cls,inputPath):
        """Lecteur and constructor for hydrostar-v format (json)
        This format is only for hydrostar-v
        Parameters
        ----------
        inputPath : str or dict
            path to input.json file or already parsed dict 

        Returns
        -------
        output : RdfCoef or list of RdfCoef
            output RdfCoef object if there are 1 speed
            outout list of RdfCoef if there are many speeds

        """
        outputList = read_hydrostarV_database(inputPath)
        for item in outputList:
            item["version"]   = cls.version
        if len(outputList)== 1:
            return cls.Build(**outputList[0])
        else:
            return [cls.Build(**item) for item in outputList]

    #-------------------------------------------#
    # Data management                           #
    #-------------------------------------------#

    def new_vars(self,var_name,var_type,data=None,dtype="float64",register=True):
        """Create object DataArray from a given data (optional), check of dimensions 
        are correct. If data is not given, a table of zeros with appropriate size 
        will be generated.
        If register == True, add variable to database.
        Parameters
        ----------
        var_name : str
            Name of DataArray
        var_type : str
            One of the following:
                "dynamic_coupled", "dynamic_uncoupled",
                "static_6x6DoF", "static_coupled"    
                "dynamic_only", "notable_point"   
        data    : array-like, optional
            Value of new vars, default None
        register : bool, optional
            Register variable in database, by default True
        """
        assert var_type in self.all_dims.keys(), f'Unrecognized data type :{var_type}'
        var_dim = self.all_dims[var_type]
        db = self._data
        shape = [db.sizes[item] for item in var_dim]
        if data is None:
            data = np.zeros(shape,dtype=dtype)

        else:
            assert np.allclose(data.shape,shape), \
                "Given data shape ({data.shape}) is not consistance with type {var_type}"
        
        newdb = db.assign(**{var_name:(var_dim,data)})
        if register:
            self._data = newdb
        return newdb[var_name]
        


    #-------------------------------------------#
    # Properties                                #
    #-------------------------------------------#
    @property
    def data(self):
        """Coefficient as xarray dataset
        """
        return self._data

    @data.setter
    def data(self,inputXarray):
        if isinstance(inputXarray,xa.Dataset):
            dbVersion = getattr(inputXarray,"version",0)
            if  dbVersion == self.version:
                self._data = inputXarray
            else:
                self._data = self.convertXarray(inputXarray)

                
        elif isinstance(inputXarray,mcn.RdfCoef):
            self.data = inputXarray.data
        else:
            raise RuntimeError(f"Attempt to initialize RdfCoef object "\
                            +f"with invalid object type: {type(inputXarray)}")

    @property
    def nb_body(self):
        return self._data.nb_body
    @property
    def wave_length(self):
        if hasattr(self._data,"wave_length"):
            return self._data.wave_length
        elif "wave_length" in self._add_data:
            return self._add_data["wave_length"]
        else:
            self._add_data["wave_length"] = np.array(
                [w2l( freq, depth = self.depth ) for freq in self._data.frequency])
            return self._add_data["wave_length"]

    @property
    def encounter_frequency(self):
        if "encounter_frequency" not in self._data.keys():
            self.add_encounter_frequency_to_database()
        return self._data.encounter_frequency

    def add_encounter_frequency_to_database(self):
        """Encounter frequency is a derived input that 
        can be computed thank to dispersion relation, 
        it doesn't necessary present in the database. 
        We can add it in the database at any moment. 
        """
        data = self._data
        if "encounter_frequency" not in data.keys():
            frequency = data.frequency
            heading   = data.heading
            speed     = data.speed
            depth     = data.depth
            nb_head   = len(heading)
            nb_freq   = len(frequency)
            encounter_frequency = np.zeros((nb_head,nb_freq),dtype='float64')
            for i_freq,freq in enumerate(frequency):
                for i_head,head in enumerate(heading):
                    encounter_frequency[i_head,i_freq] = \
                            w2we( freq , head*np.pi/180, speed, depth = depth )
            self.new_vars("encounter_frequency","dynamic_only",data=encounter_frequency)

    @property
    def essential_info(self):
        outputDict = {}
        data = self._data
        for item in self.data_vars_requirement:
            outputDict[item] = data.__getitem__(item).data
        for item in self.coords_requirement:
            outputDict[item] = data.__getitem__(item).data
        for item in self.attrs_requirement:
            outputDict[item] = data.attrs[item]
        return outputDict

    @property
    def explicit_dict(self):
        outputDict = {}
        data = self._data
        for item in self.data_vars_requirement + self.data_vars_optional:
            outputDict[item] = data.__getitem__(item).data
        for item in self.coords_requirement + self.coords_optional:
            outputDict[item] = data.__getitem__(item).data
        for item in self.attrs_requirement + self.attrs_optional:
            outputDict[item] = data.attrs[item]
        return outputDict

    @property
    def ref_point(self):
        return self._data.ref_point

    @ref_point.setter
    def ref_point(self,new_ref_point):
        """Move the coefficicents to a new reference point. In place.
        Apply transformation to all attributes whose name are
        in the list cls.matrans_list
        Parameters
        ----------
        new_ref_point : np.ndarray (nb_body,3)
            New reference point
        """
        old_ref_point = np.array(self.ref_point)
        if not np.allclose(old_ref_point,new_ref_point):
            data = self._data
            for item in self.matrans_list:
                data[item] = self._matrans(data[item], old_ref_point,new_ref_point)
            data.ref_point.data = new_ref_point

    @property
    def ref_wave(self):
        return self._data.ref_wave

    @ref_wave.setter
    def ref_wave(self,newvalue):
        # TODO: implement phase shift when set to new wave reference point.
        raise AttributeError(f"Setting a new value for ref_wave is not yet implemented!")



    #-------------------------------------------#
    # Wrapper functions                         #
    #-------------------------------------------#
    def sel(self,*args,**kwargs):
        """ Wrap around dataset function to get
        correct traceback log
        """
        return self._data.sel(*args,**kwargs)

    def isel(self,*args,**kwargs):
        """ Wrap around dataset function to get
        correct traceback log
        """
        return self._data.isel(*args,**kwargs)

    def write(self,filename):
        """Write the content to hdf format

        Parameters
        ----------
        filename : str
            Filename to write
        """
        #self._data.to_netcdf(path=filename)
        data = self._data
        attrs = data.attrs
        attrs["version"] = self.version - 1 
        coords = data.coords
        data_vars = {}
        for key in data.data_vars.keys():
            if key in self.combine_complex:
                complex_data = data.data_vars[key]
                data_vars[key+"_re"] = complex_data.real
                data_vars[key+"_im"] = complex_data.imag
            else:
                data_vars[key] = data.data_vars[key]
        data_out = xa.Dataset(coords = coords, attrs = attrs, data_vars = data_vars)                
        data_out.to_netcdf(path=filename)
    #-------------------------------------------#
    # Dunder functions                          #
    #-------------------------------------------#
    def __getitem__(self,itemname):
        return self._data[itemname]

    def __getattr__(self,attrname):
        return self._data.__getattr__(attrname)

    def __setitem__(self, key, newvalue):
        self._data.__setitem__(key,newvalue)


    def __setstate__(self,data): # Pickle support
        self.data = data

    def __getstate__(self): # Pickle support
        return self.data

    def __copy__(self): # Support for copy function
        return self.__class__(self._data.copy())

    def __deepcopy__(self): # Support for copy function
        return self.__class__(self._data.copy(deep=True))

    def copy(self,deep=False):
        return self.__class__(self._data.copy(deep=deep))

    def _compare(self,another):
        class_name = self.__class__.__name__
        if isinstance(another,HydroCoefABC):
            thisDict = self.essential_info
            thatDict = another.essential_info
            if not set(thisDict.keys())==set(thatDict.keys()):
                return False, "2 object don't share the same list of keys"
            for item in thisDict.keys():
                if isinstance(thisDict[item],str):
                    if not thisDict[item]==thatDict[item]:
                        return False, f"Different in {item}"
                elif isinstance(thisDict[item],np.ndarray) or isinstance(thisDict[item],xa.core.dataarray.DataArray):
                    if not np.allclose(thisDict[item],thatDict[item]):
                        return False, f"Different in {item}"
                elif isinstance(thisDict[item],Number):
                    if not thisDict[item] == thatDict[item]:
                        return False, f"Different in {item}"
                else:
                    logger.info(f'Warning, not comparing {item} of type {type(thisDict[item])}')
            return True,""

        if isinstance(another,dict):
            try:
                anotherObj = HydroCoefABC.FromDict(another)
            except Exception as e:
                return False, f"Faild to convert dictionary to {class_name} object, error: {e}"
        if isinstance(another,xa.Dataset)  :
            try:
                anotherObj = HydroCoefABC(another)
            except Exception as e:
                return False, f"Faild to convert xarray to {class_name} object, error: {e}"

        else:
            raise RuntimeError(f"Object type {type(another)} is not comparable with object type {class_name}")
        return self._compare(anotherObj)



    def __eq__(self,another):
        return self._compare(another)[0]


    #-------------------------------------------#
    # Attached utility functions                #
    #-------------------------------------------#
    @staticmethod
    def default_labeling(coords,nb):
        """ If coords is None, automatically fill
        coords with label from 1 to nb.
            Otherwise, check if len(coords)==nb,
        and return as is.
        """
        if coords is None:
            coords = np.arange(1,nb+1,dtype='int')
        else:
            assert len(coords) == nb , f'Size of input is not {nb}'
        return coords

    @staticmethod
    def guessFormat(inputPath):
        """
            Utility function that guess in put format
            Parameters
            ----------
                inputPath : str
            Returns
            -------
                output: str
                    data format
        """
        if inputPath.endswith("h5"):
            return "HDF"
        elif inputPath.endswith("json"):
            return "JSON"


    @staticmethod
    def _matrans(xarrayIn,old_ref_point,new_ref_point):
        dataArray = xarrayIn.data
        dataArrayTrans = np.zeros_like(dataArray)
        shapeArray = dataArray.shape

        if (len(shapeArray)==3):
            nbBody,nModeI,nModeJ = shapeArray
            for ibody in range(nbBody):
                dataArrayTrans[ibody,:,:] = matrans3(
                                dataArray[ibody,:,:],
                                old_ref_point[ibody],
                                new_ref_point[ibody])

        elif len(shapeArray)== 4:
            nbBody,nbHead,nbFreq,nModeI = shapeArray
            for ibody in range(nbBody):
                for ihead in range(nbHead):
                    for ifreq in range(nbFreq):
                        dataArrayTrans[ibody,ihead,ifreq,:] = vectran3(
                                    dataArray[ibody,ihead,ifreq,:],
                                    old_ref_point[ibody],
                                    new_ref_point[ibody])
        elif len(shapeArray)== 6:
            nbBodyI,nbBodyJ,nbHead,nbFreq,nModeI,nModeJ = shapeArray
            if (nbBodyI > 1) or (nbBodyJ > 1):
                raise NotImplementedError("Translation for multibody case is not yet implemented")
            for ibody in range(nbBodyI):
                for jbody in range(nbBodyJ):
                    for ihead in range(nbHead):
                        for ifreq in range(nbFreq):
                            dataArrayTrans[ibody,jbody,ihead,ifreq,:,:] = \
                                matrans3(dataArray[ibody,jbody,ihead,ifreq,:,:],\
                                         old_ref_point[ibody],\
                                         new_ref_point[ibody])
        else:
            raise RuntimeError("Unexpected shape of matrix: {dataA}")
        xarrayIn.data = dataArrayTrans
        return xarrayIn
