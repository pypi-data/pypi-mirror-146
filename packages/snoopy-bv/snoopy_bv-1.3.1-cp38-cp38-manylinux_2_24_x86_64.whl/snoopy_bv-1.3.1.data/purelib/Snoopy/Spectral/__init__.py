import sys
try:
    mod = sys.modules[__name__]
except:
    import Spectral
    mod = sys.modules[__name__]

from _Spectral import *
from .seastate import SeaState, SeaState2D, compareSeaStatePlot, SeaState2D_Fourier
from .seaStateList import SeaStatesDF
from .wif import Wif
from .wifm import Wifm
from .rao import Rao, getUnitRao
from .spectralStats import  RsFromM0, AsFromM0, RtzFromM0M2, SpectralStats, msi , msi_from_motion
from .qtf import Qtf
from .mqtf import MQtf
from .responseSpectrum import ResponseSpectrum
from .responseSpectrum import ResponseSpectrum2nd
from .dampingLinearization import StochasticDamping, LinearizeAndMatch
from .wib import Wib
from .edw import rcwCalc, constrainedWave, Edw_Rao, NewWave
from .dispersion import w2k, k2w, w2we, k2Cp, w2l, w2Cg, l2t, T2Te, t2l, we2w, cp2t, cp2k, t2k, l2w, w2Cp
from . import spectrum
from .spectrum import SpectrumType, Spectrum , specMaker
from .misc import modesIntsToNames, modesIntToMode, modesTypeComponentToIntDict, modesIntToTypeComponentDict, modesDf
from .spectralStats import ampFromRperiod, ampFromRisk_py
from .headingConvention import plotHeadingConfiguration


for name in spectrum.availableSpectra :
    setattr( mod , name , getattr( spectrum , name ) )

from .spreading import Cosn, Wnormal, Cos2s
ParametricSpectrum = spectrum.ParametricSpectrum
import os
TEST_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Tests", "test_data")
