"""
   Snoopy is an namespace package.
   => Subpackage (like Spectral, Meshing...) can be imported/distributed individually
"""

import sys
import os
import importlib
import logging
from os.path import join
import pkgutil
from .System import LogTimerFormatter
from .version import snoopy_tag

__version__ = snoopy_tag

def getDevPath(sharedCodeDir) :
    pyd_package_names = ["_Geometry", "_Math", "_Mechanics", "_Meshing", "_Spectral", "_Statistics", "_TimeDomain"]
    pyd_path = os.getenv("SNOOPY_PYD", "Release")
    if "SNOOPY_PYD" in os.environ.keys() :
        #If envvar specified path exists, use it!
        if os.path.exists( join(sharedCodeDir, pyd_path) ) :
            return pyd_path
        else :
            raise(Exception("SNOOPY_PYD Path {:} does not exists".format(join(sharedCodeDir, pyd_path) )))

    else :  # pyd has to be in PYTHONPATH, check it
        atLeastOne = False
        for package_name in pyd_package_names:
            if(pkgutil.get_loader(package_name) is not None):
                atLeastOne = True
            else:
                print ( package_name , "not found")
        # return empty list because pyd are already in sys.path
        if atLeastOne :
            return None
        else:
            # nothing has been found, raise
            print ("PYTHONPATH\n" + "\n".join( os.getenv("PYTHONPATH", "").split(";") ))
            raise(Exception(f"Path for Snoopy pyd not found in specified path ({join(sharedCodeDir, pyd_path):}) nor in PYTHONPATH"))


# Create logger for Snoopy
class DualLogger(logging.Logger): # To set level in python and various cpp modules at the same time
    def setLevel(self, level, cpp = []):
        logging.Logger.setLevel(self, level)
        if isinstance(cpp, str ) :
            if cpp == "all":
                cpp = ["Spectral" , "WaveKinematic", "TimeDomain" , "Statistics", "Tools", "Meshing"]
        for c in cpp :
            importlib.import_module(f"Snoopy.{c:}" ).set_logger_level( level )


logger = logging.getLogger(__name__)
logger.__class__ = DualLogger # Promote to "DualLogger", so that setLevel handles cpp spdlog level as well.
if len(logger.handlers) == 0 :  # Avoid re-adding handlers (When script is re-run with spyder for instance)
    c_handler = logging.StreamHandler()
    c_handler.setFormatter(LogTimerFormatter())
    logger.addHandler(c_handler)


logger.setLevel(logging.INFO)

snoopyDir = os.path.abspath(join(os.path.dirname(__file__)))

#Handle path to pyd :
if "base_library.zip" in snoopyDir:  # Freezed case with pyInstaller. TODO : Check that this is still necessary, now that binaries are always copied in 'DLLs'
    pass
elif(pkgutil.get_loader("_Spectral") is not None):  # If found
    pass
elif os.path.exists( os.path.join(snoopyDir, "DLLs") ) : # Case where Snoopy has been installed (in site package)
    #Better option would be to have the setup.py copying the binaries in correct folders. Would avoid messing with sys.path
    sys.path.insert(0, join(snoopyDir, "DLLs"))
else :
    subfolder = getDevPath(snoopyDir)
    logger.debug("dev path : {}".format(subfolder))
    if subfolder is not None:
        sys.path.insert(0, join(snoopyDir, subfolder))

    #Print binary path in case of debug mode
    if subfolder is not None:
        if "debug" in subfolder.lower() :
            logger.setLevel(logging.DEBUG)
            logger.debug("Using debug PYD")
    else:
        logger.debug("Using SNOOPY from PYTHONPATH")

# Make Snoopy a namespage package
__path__ = __import__('pkgutil').extend_path(__path__, __name__)
