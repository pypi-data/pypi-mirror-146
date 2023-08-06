import numpy as np
import _WaveKinematic
import pandas as pd

availableWaveKinematic = [
                         'FirstOrderKinematic',
                         'SecondOrderKinematic',
                         'SecondOrderKinematic21',
                         'Wheeler1st',
                         'Wheeler2nd',
                         'DeltaStretching',
                         ]


class WaveKinematicABC( object) :

    def getElevation_SE( self , time , x, y , speed = 0.0 ) :
        """Return wave elevation at a fixed position, as pandas Series.


        Parameters
        ----------
        time : float or array-like
            Time
        x : float or array-like
            x coordinates of the point.
        y : float or array-like
            y coordinates of the point.
        speed : float, optional
            Speed. The default is 0.0.

        Returns
        -------
        pd.Series
            Wave elevation
        """

        res = self.getElevation(  time , x, y , speed = speed )
        se = pd.Series( index = pd.Index(time , name = "Time") , data = res )
        se.name = "eta (m)"
        return se
        
    def getPressure_SE( self , time , x, y , z ) :
        """Return wave dynamic pressure at a fixed position, as pandas Series.


        Parameters
        ----------
        time : float or array-like
            Time
        x : float or array-like
            x coordinates of the point.
        y : float or array-like
            y coordinates of the point.
        z : float or array-like
            z coordinates of the point.

        Returns
        -------
        pd.Series
            Wave pressure (in m).
        """

        res = self.getPressure( time , x, y, z )
        se = pd.Series( index = pd.Index(time , name = "Time") , data = res )
        se.name = "Pressure"
        return se


    def getElevation_DF( self , time , xVect , y , speed = 0.0 ) :
        """Return wave elevation along X axis as pandas dataframe (time, x0, x1 ... xn).
        """
        res = self.getElevation2D(  time , xVect, np.full( time.shape, y) , speed = speed )
        return pd.DataFrame( index = time , data = res, columns = xVect )


    def getVelocity_DF( self , time , x, y , z, speed = 0.0, index = "time" ) :
        """Return wave velocity at a fixed position, as pandas DataFrame (time, vx, vy, vz).

        Parameters
        ----------
        time : array
            Time
        x : float
            x coordinates of the point.
        y : float
            y coordinates of the point.
        z : float
            z coordinates of the point.
        speed : float, optional
            Speed. The default is 0.0.

        Returns
        -------
        pd.DataFrame
            Wave kinematic

        Example
        -------
        vel = kin.getVelocity_DF( time = np.arange(0., 10800 , 0.5) , [0.0 , 0.0] )

        """

        if isinstance(time , np.ndarray) :
            index = "time"
        elif isinstance(z , np.ndarray) :
            index = "z"
        else :
            raise(Exception("Only one argument should be an array"))

        # TODO Vectorize in c++ for much faster computation ?
        if index == "time" :
            res = np.empty( (len(time) , 3 ))
            for i, t in enumerate(time) :
                res[i] = self.getVelocity(  t , x + speed * t , y , z )
            return pd.DataFrame( index = pd.Index(time, name = index) , data = res ,columns = ["vx" , "vy" , "vz"] )

        elif index == "z" :
            res = np.empty( (len(z) , 3 ))
            for i, z_ in enumerate(z) :
                res[i] = self.getVelocity(  time , x + speed * time , y , z_ )
            return pd.DataFrame( index = pd.Index(z, name = index) , data = res ,columns = ["vx" , "vy" , "vz"] )


    def __call__(self , time , x , y) :
        return self.getElevation( time, x , y  )

    def getModes(self):
        return [0]


class SecondOrderKinematic(_WaveKinematic.SecondOrderKinematic, WaveKinematicABC) :
    pass

class SecondOrderKinematic21(_WaveKinematic.SecondOrderKinematic21, WaveKinematicABC) :
    pass

class FirstOrderKinematic(_WaveKinematic.FirstOrderKinematic, WaveKinematicABC) :
    pass

class Wheeler1st(_WaveKinematic.Wheeler1st, WaveKinematicABC) :
    pass

class Wheeler2nd(_WaveKinematic.Wheeler2nd, WaveKinematicABC) :
    pass

class DeltaStretching(_WaveKinematic.DeltaStretching, WaveKinematicABC) :
    pass
