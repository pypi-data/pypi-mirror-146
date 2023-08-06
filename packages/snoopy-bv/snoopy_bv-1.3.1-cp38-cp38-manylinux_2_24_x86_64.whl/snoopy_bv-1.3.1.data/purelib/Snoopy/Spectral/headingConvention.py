import numpy as np


"""
   Routines to convert and check heading convention (local, global... ) and visualize the configuration

   Snoopy 'global' heading convention is not the StarSpec one!

"""



def local_from_wave_and_vessel( wave_heading, vessel_azimuth, convention = "snoopy" ):
    """Convert from global reference system to local reference system.


    Parameters
    ----------
    wave_heading : float or np.ndarray
        Wave heading, in global reference frame.

    vessel_azmiuth : float or np.ndarray
        Ship heading, in global reference frame.

    convention : str
        Convention in which wave_heading and vessel_azimuth are input.


    Returns
    -------
    relative_heading : float or np.ndarray
        Relative wave heading (np.pi == head-wave)


    Convention description
    ----------------------

        Local (attached to the ship)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        Relative wave heading convention (HydroStar == Snoopy) :
            np.pi       : Head wave
            np.pi / 2   : Wave from starboard
            0.0         : Following waves
            -np.pi / 2  : Wave from portside


        Global (attached to earth)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~

        Snoopy "global reference system" : Trigonometric angle (same for both wave and vessel direction)

            0         : Towards increasing x
            np.pi / 2 : Towards increasing y
            np.pi       : Wave coming from positive x, toward negative x
            -np.pi / 2  : Wave coming from positive y, toward negative y

            0           : Vessel pointing to positive x
            np.pi / 2   : Vessel pointing to positive y
            np.pi       : Vessel pointing to negative x
            -np.pi / 2  : Vessel pointing to negative y


        Starspec "global convention" : "meteorological convention for waves"
            0 : Waves from North, Ship point to North,
            np.pi : Waves from East, Ship point to East

    Notes
    -----
    In case of head-aches, use "plotHeadingConfiguration()" !


    """

    if convention.lower() == "starspec" :
        relative_heading = np.pi - wave_heading + vessel_azimuth
    elif convention.lower() == "snoopy":
        relative_heading = wave_heading - vessel_azimuth
    else :
        raise(Exception(f"Convention {convention:} not known. Use 'snoopy' or 'starspec'"))

    return relative_heading



def get_new_wave_heading( wave_heading, vessel_azimuth, new_vessel_azimuth, convention ):
    """Return new global wave heading that keeps relative wave heading the same with the new azimuth

    Mainly used for StarSpec, where azimuth is fixed.

    Parameters
    ----------
    wave_heading : float or np.ndarray
        Wave heading, in global reference frame.

    vessel_azmiuth : float or np.ndarray
        Ship heading, in global reference frame.

    convention : str
        Convention in which wave_heading and vessel_azimuth are input and output.

    Returns
    -------
    float or np.ndarray
        Global wave heading

    """

    if convention.lower() == "starspec" :
        return (wave_heading - vessel_azimuth + new_vessel_azimuth) % (2*np.pi)
    else :
        raise(NotImplementedError)
        return



def plotHeadingConfiguration( wave_heading = 0.0, vessel_azimuth = 0.0, ax = None, convention = "Snoopy" ) :
    """Plot heading configuration


    Parameters
    ----------
    wave_heading : float
        Wave heading, in global reference frame.

    vessel_azmiuth : float
        Ship heading, in global reference frame.

    convention : str
        Convention in which wave_heading and vessel_azimuth are input.

    """

    from matplotlib import pyplot as plt

    if ax is None :
        fig, ax = plt.subplots( )

    ax.set_aspect("equal")


    relative_heading = local_from_wave_and_vessel(wave_heading, vessel_azimuth, convention = convention)

    #---------Wave arrow
    r_out = 4
    length = 2.0

    #---------- Vessel :
    vessel_0 = np.array( [ [ -1  , 1, ],
                           [ 1  ,  1, ],
                           [ 2.0,  0, ],
                           [ 1, -1, ],
                           [ -1, -1, ],
                           [ -1  , 1, ],
                         ] )

    rot_vessel = np.empty(vessel_0.shape)

    if convention.lower() == "starspec" :

        rot_vessel[:,0] = vessel_0[:,0] * np.cos( np.pi/2 - vessel_azimuth ) + vessel_0[:,1] * np.sin( np.pi/2 - vessel_azimuth )
        rot_vessel[:,1] = vessel_0[:,0] * np.sin( np.pi/2 - vessel_azimuth ) - vessel_0[:,1] * np.cos( np.pi/2 - vessel_azimuth )
        ax.plot( rot_vessel[:,0], rot_vessel[:,1], marker = "o" )


        #-fix dir
        r_out_f = 4.0
        length_f = 1.0
        for f in [0, np.pi/2 , np.pi , 3*np.pi / 2]:
            x_start = -r_out_f * np.cos( -f - np.pi/2 )
            y_start = -r_out_f * np.sin( -f - np.pi/2)
            dx = length_f * np.cos( -f - np.pi/2)
            dy = length_f * np.sin( -f - np.pi/2)
            ax.arrow( x_start, y_start, dx, dy, head_width  = 0.2 , length_includes_head = True)
            ax.text( x_start + 0.2, y_start + 0.2 , f"{np.rad2deg(f):.0f}" )

        #---------- Wave:
        x_start = -r_out * np.cos( -wave_heading - np.pi/2 )
        y_start = -r_out * np.sin( -wave_heading - np.pi/2)
        dx = length * np.cos( -wave_heading - np.pi/2)
        dy = length * np.sin( -wave_heading - np.pi/2)


        ax.arrow( x_start, y_start, dx, dy, head_width  = 0.5 , length_includes_head = True)

        #---------- Info
        ax.set_title("Starspec heading convention")

    else:

        #-fix dir
        r_out_f = 3.0
        length_f = 1.0
        for f in [0, np.pi/2 , np.pi , 3*np.pi / 2]:
            x_start = r_out_f * np.cos( f )
            y_start = r_out_f * np.sin( f )
            dx = length_f * np.cos( f )
            dy = length_f * np.sin( f )
            ax.arrow( x_start, y_start, dx, dy, head_width  = 0.2 , length_includes_head = True)
            ax.text( x_start + 0.2, y_start + 0.2 , f"{np.rad2deg(f):.0f}" )

        rot_vessel[:,0] = vessel_0[:,0] * np.cos( vessel_azimuth ) + vessel_0[:,1] * np.sin( vessel_azimuth )
        rot_vessel[:,1] = vessel_0[:,0] * np.sin( vessel_azimuth ) - vessel_0[:,1] * np.cos( vessel_azimuth )
        ax.plot( rot_vessel[:,0], rot_vessel[:,1], marker = "o" )

        #---------- Wave:
        x_start = -r_out * np.cos( wave_heading )
        y_start = -r_out * np.sin( wave_heading )

        dx = length * np.cos( wave_heading )
        dy = length * np.sin( wave_heading )

        ax.set_xlim( [-5, 5] )
        ax.set_ylim( [-5, 5] )
        ax.arrow( x_start, y_start, dx, dy, head_width  = 0.5 , length_includes_head = True)

        ax.set_title("Snoopy heading convention (Trigonometric)")

    ax.set_xlim( [-7, 6] )
    ax.set_ylim( [-6, 6] )
    #---------- Info
    ax.text(  -6.5, 5.5, f"Relative wave heading = { np.rad2deg(relative_heading)%360.:.1f}" )
    ax.text(  -6.5, 5.0, f"Wave heading = { np.rad2deg(wave_heading)%360.:.1f}" )
    ax.text(  -6.5, 4.5, f"Vessel azimuth = { np.rad2deg(vessel_azimuth)%360.:.1f}" )
    return ax







if __name__ == "__main__" :

    # plotHeadingConfiguration( wave_heading = np.pi, vessel_azimuth = 0.0)

    wave_heading = np.pi
    vessel_azimuth = np.pi/3

    plotHeadingConfiguration( wave_heading = wave_heading, vessel_azimuth = vessel_azimuth, convention = "starspec")

    new_vessel_azimuth = np.pi/2
    new_wave = get_new_wave_heading( wave_heading, vessel_azimuth, new_vessel_azimuth=new_vessel_azimuth, convention = "starspec" )

    plotHeadingConfiguration( wave_heading = new_wave, vessel_azimuth = new_vessel_azimuth, convention = "starspec")

