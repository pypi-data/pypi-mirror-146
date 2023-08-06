import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline
from Snoopy import logger
from droppy.pyplotTools import probN
from scipy.stats import beta

class ReturnLevel():
    """Compute return period from samples.

    Notes
    -----
    Assumes :
        - independent events
        - that number of events in the duration is always the same.

    All relates to the following formulae (probability of not exceeding return value on return period is 1/e) :

        $P(X_{RP}, RP) = 1 / e$

    with:

        $P(X, T) = P_c^{T / Rtz}$

    $P_c$ being the non-exceedance probability on each events (can be up-crossing period)

    $RP = - Rtz / ln( P_c(x) )$

    This is not to be used for POT, where number of threshold exceedance is random (Poisson process)
    """

    def __init__(self, data, duration, alphap = 0. , betap = 0.):
        """Construct ReturnLevel instance

        Parameters
        ----------
        data : array like
            data samples (independent events)
        duration : float
            Total duration covered by the data. If None, duration is retrieve from data index (if Series). Each event thus corresponds to DT = duration / len(data).
        alphap : float, optional
            alpha coefficient for empirical distribution. The default is 0..
        betap : float, optional
            beta coefficient for empirical distribution. The default is 0..

        Example
        ------
        >>> rl = ReturnLevel( data , duration = 10800 )
        >>> rl.rp_2_x( 3600  )
        >>> rl.plot()

        """

        self.data = data

        self._n = len(data)

        if duration is None :
            self._duration = data.index.max() - data.index.min()
        else :
            self._duration = duration


        # Empirical exceedance probabilitys
        prob = probN(self._n, alphap = alphap , betap = betap)

        # Empirical return period
        self._rp = -duration / (self._n * np.log( 1 - prob ))

        # Empirical return values
        self._rv = np.sort(data)

        # Event duration
        self.t_block = duration / self._n

        # Space for interpolator
        self._x_to_rp = None



    def _build_interp(self):
        # Build interpolator

        logger.debug("Build return level interpolator")
        self._rp_to_x = InterpolatedUnivariateSpline( self._rp , self._rv, ext = "raise" )

        # Handle duplicated data
        _, u_index = np.unique(self._rv, return_index=True)
        self._x_to_rp = InterpolatedUnivariateSpline( self._rv[u_index] , self._rp[u_index], ext = "raise")


    def plot(self, ax = None, scale_rp = 1, marker = "+" , linestyle = "", **kwargs):
        """Plot value against return period.

        Parameters
        ----------
        ax : AxesSubplot, optional
            Where to plot. The default is None.
        scale_rp : float, optional
            RP scale (for instance, in input data are seconds, but plots is desired in hours). The default is 1.
        marker : str, optional
            Marker. The default is "+".
        linestyle : str, optional
            linestyle. The default is "".
        **kwargs : any
            Optional argument passed to plt.plot()

        Returns
        -------
        ax : AxesSubplot
            The graph.
        """
        if ax is None :
            fig , ax = plt.subplots()
        ax.plot( self._rp * scale_rp , self._rv,  marker = marker, linestyle = linestyle, **kwargs)
        ax.set_xscale("log")
        ax.set(xlabel = "Return period")
        return ax

    def x_2_rp(self , x) :
        """Return period from return value

        Parameters
        ----------
        x : float
            Return value

        Returns
        -------
        float
            Return period
        """
        if self._x_to_rp is None:
            self._build_interp()
        return self._x_to_rp(x)

    def rp_2_x(self, rp) :
        """Return value from return period

        Parameters
        ----------
        rp : float
            return period

        Returns
        -------
        float
            return value
        """
        if self._x_to_rp is None:
            self._build_interp()
        return self._rp_to_x(rp)


    def x_to_rpci( self, alpha, ci_type = "n" ):
        """Return RP confidence interval for sorted empirical return values

        Parameters
        ----------
        alpha : float
            Centered confidence interval
        ci_type : TYPE, optional
            DESCRIPTION. The default is "n".

        Returns
        -------
        (np.ndarray, np.ndarray)
            Lower and upper CI.
        """

        i = np.arange(1, self._n + 1, 1)[::-1]

        if ci_type == "n" :
            betaN = beta( i , self._n + 1 - i )
        elif ci_type == "jeffrey" :
            betaN = beta( i + 0.5 , self._n + 0.5 - i )

        return betaN.ppf( alpha/2 ) , betaN.ppf(1-alpha/2)


    def plot_ci(self, alpha_ci , ax = None, scale_rp = 1.0, ci_type = "n", alpha = 0.1, **kwargs) :
        """Plot confidence interval

        Parameters
        ----------
        alpha_ci : float
            Centered confidence interval.
        ax : AxesSubplot, optional
            Where to plot. The default is None.
        scale_rp : float, optional
            RP scale (for instance, in input data are seconds, but plots is desired in hours). The default is 1.
        ci_type : str, optional
            Variant for the confidence interval, among ["n" , "jeffrey"]. The default is "n".
        alpha : float, optional
            Opacity for the filling of the confidence interval. The default is 0.1.
        **kwargs : any
            Additional arguments passed to .fillbetweenx().

        Returns
        -------
        ax : AxesSubplot
            The graph.
        """

        if ax is None :
            fig , ax = plt.subplots()

        prob_l, prob_u = self.x_to_rpci(alpha_ci, ci_type = ci_type)
        rp_l = -self._duration / (self._n * np.log( 1 - prob_l )) * scale_rp
        rp_u = -self._duration / (self._n * np.log( 1 - prob_u )) * scale_rp

        ax.fill_betweenx(self._rv, rp_l, rp_u, alpha = alpha, **kwargs)
        # ax.plot( rp_l, self._rv)
        # ax.plot( rp_u, self._rv)

        return ax


    @staticmethod
    def plot_distribution( distribution, blockSize, rp_range, ax = None, **kwargs):
        """Plot analytical distribution against return period

        Parameters
        ----------
        distribution : scipy.stats.rv_frozen
            Distribution on each event.
        blockSize : float
            duration of each event
        ax : plt.Axis, optional
            Where to plot. The default is None.

        Returns
        -------
        ax : plt.Axis
            The graph
        """

        if ax is None :
            fig, ax = plt.subplots()

        ax.plot( rp_range, ReturnLevel.rp_to_x_distribution( distribution, blockSize, rp_range) , **kwargs)
        ax.set_xscale("log")
        return ax


    @staticmethod
    def x_to_rp_distribution( distribution, blockSize, x):
        """Calculate return period of a given value x. x follows "distribution" on each even that has a duration "blockSize".

        Parameters
        ----------
        distribution : scipy.stats.rv_frozen
            Distribution on each event.
        blockSize : float
            duration of each event

        x : float
            Value

        Returns
        -------
        rp : float
            return period
        """

        return -blockSize / np.log( distribution.cdf(x) )


    @staticmethod
    def rp_to_x_distribution(distribution, blockSize, rp):
        """Calculate return value x from return period rp. x follows "distribution" on each even that has a duration "blockSize".

        Parameters
        ----------
        distribution : scipy.stats.rv_frozen
            Distribution on each event.
        blockSize : float
            duration of each event
        rp : float or np.ndarray
            return period

        Returns
        -------
        x : float or np.ndarray
            return value
        """
        p_ = 1 - np.exp(-blockSize / (rp))
        return distribution.isf(p_)




def xrp_pdf( x, rp, alpha, T_block, dist ):
    """Compute probability density of the empirical return value x, with return period 'rp', knowin simulated time and distribution.

    Parameters
    ----------
    x : float or np.ndarray
        Response value
    rp : float
        return value
    alpha : float
        ratio between data duration and return period
    T_block : float
        Block size (fixed event duration)
    dist : stats.rv_continuous
        Disitribution of event

    Returns
    -------
    float or np.ndarray
        Prability density of x.
    """
    nu = 1 / T_block
    p = np.exp(-1/(nu*rp))
    return dist.pdf( x ) * beta( (nu*alpha*rp+1) * p , (nu*alpha*rp+1)*(1-p) ).pdf(dist.cdf(x))


def xrp_cdf( x, rp, alpha, T_block, dist ):
    """Compute cumulative probability of the empirical return value x, with return period 'rp', knowin simulated time and distribution.

    Parameters
    ----------
    x : float or np.ndarray
        Response value
    rp : float
        return value
    alpha : float
        ratio between data duration and return period
    T_block : float
        Block size (fixed event duration)
    dist : stats.rv_continuous
        Disitribution of event

    Returns
    -------
    float or np.ndarray
        Prability density of x.
    """
    nu = 1 / T_block
    p = np.exp(-1/(nu*rp))
    return beta( (nu*alpha*rp+1) * p , (nu*alpha*rp+1)*(1-p) ).cdf( dist.cdf(x) )





