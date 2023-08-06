# -*- coding: utf-8 -*-

from matplotlib import cm
import vtk

def matplotlib_to_vtkLut( cmap = "Blues_r" ):
    """
    Args:
        cmap (str, optional): Matplotlib colormap name. Defaults to "Blues_r".

    Returns:
        lut (vtkLookupTable): VTK look-up-table.
    """

    # Colour transfer function from matplotlib
    cmap = cm.get_cmap(cmap)

    N = 256
    # Lookup table.
    lut = vtk.vtkLookupTable()
    lut.SetNumberOfColors(N)
    for i in range(N):
        lut.SetTableValue(i, *cmap(i/N))
    lut.Build()
    return lut
