import sys
import numpy
from scipy.interpolate.interpolate import interp1d
from .numpy_related import get_dx, round_nearest, edges_from_center, is_multiple
from _Math import *
sys.modules["Math"] = sys.modules["_Math"]

def Interp2dVariadicAxis(x, y, xs, ys, data):
    r"""Interpolate in variadic ys.
    
    ys is supposed varying non uniformly with respect to x.
    
    :param float x: first axis value to interpolate to.
    :param float y: second axis value to interpolate to.
    :param ndarray xs: first axis vector of size nx.
    :param list ys: list of list containing the second axis varying with respect to first axis (size of ny(x) ).
    :param list data: list of list containing the data to interpolate (size of (nx, ny(x)) ).
    :return: float: data value interpolated at x and y.
    """
    # First get the surrounding time instants
    it0 = (numpy.abs(xs-x)).argmin()
    it1 = min(it0+1, len(xs)-1)
    if it0 == it1:
        return interp1d(ys[it1], data[it1])(y)
    dataY0 = interp1d(ys[it0], data[it0])(y)
    dataY1 = interp1d(ys[it1], data[it1])(y)
    x0 = xs[it0]
    x1 = xs[it1]
    return interp1d([x0, x1], [dataY0, dataY1])(x)
