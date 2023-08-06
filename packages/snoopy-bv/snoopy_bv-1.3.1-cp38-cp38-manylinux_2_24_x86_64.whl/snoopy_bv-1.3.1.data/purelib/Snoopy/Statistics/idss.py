"""
Routines related to increased design sea-states
"""

import numpy as np

def iHsRatio(  m0 , targetAmp, probIDSS ):
    """Return Increased Hs / Hs ratio
    
    Parameters
    ----------
    m0 : float
        Zero order moment on the original sea-state
    targetAmp : float
        Target value
    probIDSS : float
        Probability of targetAmp on increased design sea-state

    Returns
    -------
    Hs ratio : float
        Ratio iHs / hs, required to have P(targetAmp) = probIDSS on increased design sea-state

    """
    
    return np.sqrt(- (targetAmp)**2 / ( 2 * m0 * np.log(probIDSS)) )