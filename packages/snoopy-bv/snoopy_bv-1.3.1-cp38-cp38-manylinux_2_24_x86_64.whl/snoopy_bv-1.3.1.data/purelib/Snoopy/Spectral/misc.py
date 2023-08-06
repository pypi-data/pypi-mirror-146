import pandas as pd
import _Spectral

"""
Handle RAO names and enum

This looks too messy to be the correct way to handle things. Ideas are welcomed...
"""


modesNameToModeDict = _Spectral.Modes.__members__

modeNameToSymDict  = {
    'NONE':   (0,  "UNKNOWN", 0, "N/A" , None) ,
    'SURGE':  (+1, "MOTION", 1 , "m/m" , 1) ,
    'SWAY':   (-1, "MOTION", 2 , "m/m", 1) ,
    'HEAVE':  (+1, "MOTION", 3 , "m/m", 1) ,
    'ROLL':   (-1, "MOTION", 4 , "deg/m", 0) ,
    'PITCH':  (+1, "MOTION", 5 , "deg/m", 0 ) ,
    'YAW':    (-1, "MOTION", 6 , "deg/m", 0) ,
    'FX':     (+1, "LOAD", 1 , "N/m", 3) ,
    'FY':     (-1, "LOAD", 2 , "N/m", 3) ,
    'FZ':     (+1, "LOAD", 3 , "N/m", 3) ,
    'MX':     (-1, "LOAD", 4 , "N.m/m", 4) ,
    'MY':     (+1, "LOAD", 5 , "N.m/m", 4) ,
    'MZ':     (-1, "LOAD", 6 , "N.m/m", 4) ,
    'WAVE':   ( 0, "WAVE" , 0 , "m/m", 1) ,
    'RWE':    ( 0, "PRESSURE" , 0 , "m/m", 1) ,
    'SECTFX': (+1, "INTERNALLOAD", 1 , "N/m", 3) ,
    'SECTFY': (-1, "INTERNALLOAD", 2 , "N/m", 3) ,
    'SECTFZ': (+1, "INTERNALLOAD", 3 , "N/m", 3) ,
    'SECTMX': (-1, "INTERNALLOAD", 4 , "N.m/m", 4) ,
    'SECTMY': (+1, "INTERNALLOAD", 5 , "N.m/m", 4) ,
    'SECTMZ': (-1, "INTERNALLOAD", 6 , "N.m/m", 4) ,
    'WATERVELOCITY_X': (0, "WATERVELOCITY", 1, "m/s/m", 0.5),
    'WATERVELOCITY_Y': (0, "WATERVELOCITY", 2, "m/s/m", 0.5),
    'WATERVELOCITY_Z': (0, "WATERVELOCITY", 3, "m/s/m", 0.5),
    'PRESSURE' : (0,  "PRESSURE" , 1, "m/m", 1),
}


modesDf = pd.DataFrame(  data = modeNameToSymDict , index = pd.Index(["SYM", "TYPE", "COMPONENT", "HSTAR_UNIT" , "FROUDE_SCALE"]) ).transpose()
modesDf.index.name = "NAME"
modesDf.loc[ : , "MODE"] = [ _Spectral.Modes.__members__[k] for k in modesDf.index ]
modesDf.loc[ : , "INT_CODE"] = [ _Spectral.Modes.__int__( a ) for a in modesDf.MODE ]



def modesIntToMode( int_ ) :
    if int_ in modesIntToNameDict.keys() :
        return _Spectral.Modes(int_)
    else :
        _Spectral.Modes.NONE


"""
   For conversion to HydroStar RAO files
"""
def modesNameToType( name ) :
    return modesDf.loc[name, "TYPE"]


def modesNameToComponent( name ) :
    return modesDf.loc[name, "COMPONENT"]


modesIntToTypeComponentDict =  modesDf.set_index("INT_CODE").loc[ : , ["TYPE", "COMPONENT"] ].transpose().to_dict("list")
modesTypeComponentToIntDict = { tuple(v) : k for k, v in modesIntToTypeComponentDict.items() }

def modesIntsToNames( modesInts ) :
    """Convert modes integer code to name (strings)
    """
    # return [ modesIntToNameDict[i] for i in modesInts ]
    return modesDf.reset_index().set_index("INT_CODE").loc[ modesInts , "NAME" ].values


"""
Following lines are for compatibility with older code, might be removed
"""
modesIntToNameDict = { i : _Spectral.Modes(i).__str__().split(".") [1] for i in range( len(modesNameToModeDict)   ) }


