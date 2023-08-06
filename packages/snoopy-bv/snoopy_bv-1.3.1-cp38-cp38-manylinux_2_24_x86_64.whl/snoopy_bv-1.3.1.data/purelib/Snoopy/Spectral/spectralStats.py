import numpy as np
from Snoopy import Spectral as sp
from Snoopy import Statistics as st

"""
Spectral statistics ( Rayleigh distribution based )
"""

class SpectralStats(object) :
    """All kind of statistics for seakeeping, assuming Rayleigh distribution.
    """


    def __str__(self ):

        s = f"""Significant amplitude : {self.getAs():.3g}
Up-crossing period : {self.Rtz:.3g}
3 hours values : {self.ampFromRperiod(10800):.3g}
"""
        return s

    def __imul__(self , scalar) :
        self.m0 = self.m0 * scalar**2
        self.m2 = self.m2 * scalar**2
        self._basic()
        return self

    def __mul__(self , scalar) :
        return SpectralStats( self.m0 * scalar**2, self.m2 * scalar**2 )

    __rmul__ = __mul__


    def __init__(self, m0 , m2) :
        """
        Parameters
        ----------
        m0 : float or np.ndarray
            Spectral moment of order zero.
        m2 : float or np.ndarray
            Spectral moment of order two.

        Attributes
        ----------
        Rtz : float or np.ndarray
            Up-crossing period (s)

        rl : scipy.stats.rv_frozen
            Rayleigh distribution of maxima (single amplitude)
        """
        self.m0 = m0
        self.m2 = m2
        self._basic()

    def _basic(self):
        #Rayleigh distribution
        self.rl = st.rayleigh_c( self.m0**0.5 )

        #Mean up-crossing period
        self.Rtz = sp.RtzFromM0M2( self.m0,self.m2 )

        self.Rs = 4.004 * self.m0**0.5

    @classmethod
    def FromRsRtz(cls , Rs , Rtz):
        """Compute significant range and mean upcrossing period.

        Parameters
        ----------
        Rs : float
            Significant response (double amplitude)
        Rtz : TYPE
            Mean up-crossing period
        """
        m0 = ( Rs / 4.004 )  ** 2
        m2 = ( 2*np.pi / Rtz )**2 * m0
        return cls( m0 , m2 )

    def getRs(self):
        """Compute significant range.

        Returns
        -------
        float
            Significant response (double amplitude)

        """
        return self.Rs

    def getAs(self):
        """Compute significant amplitude.

        Returns
        -------
        float
            Significant amplitude
        """
        return 2.002 * self.m0**0.5

    def ampFromRperiod(self , duration) :
        """Get response with RP = duration.

        Parameters
        ----------
        m0 : float
            Zero order spectral moment.
        m2 : float
            Second order spectral moment.
        duration : float
            Duration (in seconds).

        Returns
        -------
        float
            amplitude with return period = "duration"

        """
        p = self.Rtz / duration
        return (2*self.m0*np.log(1/p))**0.5

    def nExceed(self, value , duration ):
        """Return expected number of exceedance in given duration.

        Parameters
        ----------
        value : float
            Amplitude.
        duration : float
            Duration (in seconds).

        Returns
        -------
        float
            Number of excedance per duration

        """
        return self.rl.sf(value) * duration / self.Rtz

    def ampFromRisk( self , risk, duration ) :
        """Amplitude associated to a given risk over a given duration.

        Parameters
        ----------
        risk : float or array
            Risk (between 0. and 1.)
        duration : float
            duration, in seconds
        Returns
        -------
        float
            Amplitude

        """
        return sp.ampFromRisk( risk, duration , self.m0 , self.m2 )

    def riskFromAmp(self, value, duration):
        """Return the risk of exceeding "value" in the given duration

        Parameters
        ----------
        value : float
            Value for which exceedance probability is desired
        duration : float
            Duration in s.

        Returns
        -------
        float
           risk (exceedance probability)

        """

        return self.getShtMaxDistribution(duration).sf(value)



    def meanMaxAmplitude( self , duration ):
        """Mean maximum on duration.

        Parameters
        ----------
        duration : float
            Sea-state duration, in seconds.

        Returns
        -------
        float
            Mean maximum on duration.

        """
        n = duration / self.Rtz
        return (  ( 2*np.log(n))**0.5 + np.euler_gamma / (2*np.log(n))**0.5 ) * self.m0**0.5



    def getShtMaxDistribution( self , duration ) :
        """Return the distribution of the maximum on duration  ( Rayleigh**n ).

        Parameters
        ----------
        duration : float
            Duration of the seastate

        Returns
        -------
        rv_frozen
            Distribution of the duration maxima. (has .pdf, .cdf, .isf ...)

        """
        n = duration / self.Rtz

        return st.Powern( self.rl, n )



    def iHsRatio( self, targetAmp, probIDSS ) :
        """Return the  increased Hs so that the target value probability is probIDSS.

        Parameters
        ----------
        targetAmp
            Amplitude to target
        probIDSS
            Probability of the target amplitude on the Increased Design Sea-State

        Returns
        -------
            Increased Design Sea-State, ratio iHs/Hs

        """
        return np.sqrt(- (targetAmp)**2 / ( 2 * self.m0 * np.log(probIDSS)) )


    def sample_each_seastate(self, duration, seed = None) :
        """Sample randomly maximum reponse on sea-state(s)

        Parameters
        ----------
        duration : float
            Sea-state duration

        seed : int
            Seed for random number generator. Default to None (random seed).

        Returns
        -------
        float or array-like
            Sample on each m0/m2 case

        """
        if isinstance( self.Rtz , float) :
            return self.getShtMaxDistribution( duration ).ppf( np.random.default_rng(seed).random(size = 1)[0] )
        else :
            return self.getShtMaxDistribution( duration ).ppf( np.random.default_rng(seed).random( self.Rtz.shape ) )



def ampFromRperiod( duration, m0, m2 ):
    """Get response with RP = duration.

    Parameters
    ----------
    m0 : float
        Zero order spectral moment.
    m2 : float
        Second order spectral moment.
    duration : float
        Duration (in seconds).

    Returns
    -------
    float
        amplitude with return period = "duration"
    """
    Rtz = sp.RtzFromM0M2(m0 , m2)
    p = Rtz / duration
    return (2*m0*np.log(1/p))**0.5




def nExceed(value , duration , m0, m2) :
    """

    Parameters
    ----------
    value  : float
        Value to be exceeded (single amplitude).
    duration : float
        Duration (in seconds).
    m0 : float
        Zero order spectral moment.
    m2 : float
        Second order spectral moment.

    Returns
    -------
    float
        Number of exceedance expected in duration

    """
    _, Rtz = sp.RsRtzFromM0M2(m0 , m2)
    p = st.rayleigh_c( m0**0.5 ).sf(value)
    return p * duration / Rtz



def RsFromM0(m0):
    """
    Copy of RsFromM0(m0) function from SpectralSht_m.f90

    Significant response (double amplitude)
    """
    return 4.004 * m0**0.5

def AsFromM0(m0):
    """
    Copy of AsFromM0(m0) function from SpectralSht_m.f90

    Significant amplitude (double amplitude)
    """
    return 2.002 * m0**0.5



def RtzFromM0M2(m0, m2):
    """
    Now in cpp

    Copy of AsFromM0(m0) function from SpectralSht_m.f90

    Mean upcrossing-period
    """
    return 2 * np.pi * (m0/m2)**0.5


def ampFromRisk_py( risk, duration, m0, m2 ):
    """ Now in cpp

    Parameters
    ----------
    risk : float
        Exceedance probability.
    duration : float
        Seastate duration (seconds).
    m0 : float
        Zero order spectral moment.
    m2 : float
        Second order spectral moment.

    Returns
    -------
    ampFromRisk : float
        Response value.

    """

    _, Rtz = sp.RsRtzFromM0M2(m0 , m2)
    n = duration / Rtz
    ampFromRisk = ( 2.*m0 * np.log( -1. / ( (1-risk)**(1./n) - 1 ) ) )**0.5
    return ampFromRisk


def msi_from_motion( ss , rao_motion , t) :
    """Compute MSI from seastate and RAO.

    Parameters
    ----------
    ss : sp.SeaState
        SeaState on which the MSI index is tp be evaluated
    rao_motion : sp.Rao
        Vertical motion rao
    t : float
        Time (minutes)

    Returns
    -------
    MSI index

    """
    #TODO check that RAO is motion

    rao_vel = rao_motion.getDerivate( n = 1)
    rSpec = sp.ResponseSpectrum( ss , rao_vel )
    m2 , m4 = rSpec.getM0M2()

    return msi(  m2 , m4 , t  )



def msi(m2_mvt, m4_mvt, t):
    """Compute Motion Sickness Incidence (MSI) according to McCauley and al. (1976).

    Parameters
    ----------
    m2_mvt : float
        Spectral moment of order 2 of vertical motion. (= m0 of velocity)
    m4_mvt : float
        Spectral moment of order 4 of vertical motion. (= m2 of velocity = m0 of acceleration)
    t : float
        t is the time of exposure in minutes

    Returns
    -------
    msi_value : float
        MSI index
    """

    a = 0.798*np.sqrt(m4_mvt) / 9.81
    f = ( 1 / (2 * np.pi) ) * np.sqrt(m4_mvt / m2_mvt)  # Frequency calculated from velocity.
    return msi_McCauley( a , f , t )

def msi_McCauley( acc_rms_g , f, t ):
    """


    Parameters
    ----------
    acc_rms_g : float
        Acceleration (RMS, g)
    f : float
        Wave frequency
    t : float
        Exposure duration (Minutes)

    Returns
    -------
    msi_value : float
        MSI index.

    """
    from scipy import special

    sigma_a = 0.47
    sigma_t = 0.76

    rho = -0.75
    mu_t = 1.46
    mu_a = 0.87 + 4.36*np.log10(f) + 2.73*(np.log10(f))**2

    z_a  = (np.log10(acc_rms_g) - mu_a)/sigma_a
    z_t  = (np.log10(t) - mu_t)/sigma_t
    z_t1 = (z_t - rho*z_a)/np.sqrt(1 - rho**2)

    phi_za  = 0.5*(1 + special.erf(z_a/np.sqrt(2)))
    phi_zt1 = 0.5*(1 + special.erf(z_t1/np.sqrt(2)))

    msi_value = 100*phi_za*phi_zt1

    return msi_value




def mii( seastate, rao_aroll, rao_accy, rao_aheave, duration , check_unit = True ):
    """Return MII criterion (Defined in BV NR-483)


    Parameters
    ----------
    seastate : sp.SeaState
        Seastate considered
    rao_aroll : sp.Rao
        Roll acceleration (in rad/s/s)
    rao_accy : sp.Rao
        Transverse acceleration (including g*theta , "ACCY" keyword in HydroStar)
    rao_heave : sp.Rao
        Heave transfer function
    check_unit : bool
        Check that roll is not in degree (if roll > 1.0 ==> raise exception). Default to True

    Returns
    -------
    MII : float
        exceedances over the considered duration
    """

    if check_unit:
        # TODO : Check that aroll is not crazy (i.e. in degree)
        pass

    # Value specified by BV NR-483. Not meant to be modified (Would be nice to find the original reference).
    h = 1.20
    b = 1.20 * 0.25

    GLFEp = (1/3) * h * rao_aroll - rao_accy - (b/h) * rao_aheave
    GLFEs = (1/3) * h * rao_aroll - rao_accy + (b/h) * rao_aheave

    stat_p = sp.ResponseSpectrum(seastate, GLFEp).getSpectralStats()
    stat_s = sp.ResponseSpectrum(seastate, GLFEs).getSpectralStats()

    a = ( b / h ) * 9.81

    mii_p = stat_p.nExceed(a, duration)
    mii_s = stat_s.nExceed(a, duration)

    return mii_p + mii_s



if __name__ =="__main__":


    rs, rtz = 1, 10
    m0, m2 = sp.m0m2FromRsRtz(rs, rtz)
    stats = SpectralStats( m0 , m2 )
    statsVect = SpectralStats( np.array([m0, m0]) , np.array([m2, m2]) )
    statsVect.nExceed(  statsVect.ampFromRperiod(  10800 ) , 10800)

    samples = statsVect.sample_each_seastate( 3600 )

    # print (statsVect)
    stats.meanMaxAmplitude(10800)

    from matplotlib import pyplot as plt
    p = np.linspace(0.01,0.99,100)
    fig, ax = plt.subplots()
    ax.plot(  stats.ampFromRisk( p, duration = 10800 ) , p )
    ax.set_yscale( "log" )

    statsVect.getShtMaxDistribution(10800).isf( 0.1 )


