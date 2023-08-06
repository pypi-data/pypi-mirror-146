import numpy as np
import vtk
from vtk.util import numpy_support
from .waterline import getHalfCircDomain
from Snoopy import Meshing as msh

def extractWaterLine(hullPolydata, x_center = 0.0, side = +1):
    """ Extract waterline from wetted hull
    Works using vtkFeatureEdges and vtkContourLoopExtraction

    return arrays of waterline nodes (xyz)
    """

    #--- Retrieve waterline
    wl = vtk.vtkFeatureEdges()
    wl.SetInputData( hullPolydata )
    wl.BoundaryEdgesOn()
    wl.FeatureEdgesOff()
    wl.NonManifoldEdgesOff()
    wl.ManifoldEdgesOff()
    wl.Update()
    loops = vtk.vtkContourLoopExtraction()
    loops.SetInputConnection(wl.GetOutputPort())
    loops.Update()
    loops_p = loops.GetOutput()
    numpy_support.vtk_to_numpy(  loops_p.GetPoints().GetData() )
    idList = vtk.vtkIdList()
    loops_p.GetCellPoints(0, idList)
    nId = [idList.GetId(i) for i in range( idList.GetNumberOfIds() )]
    orderedCoord = numpy_support.vtk_to_numpy(  wl.GetOutput().GetPoints().GetData() ) [nId]

    return orderedCoord

def createHalfFreeSurfaceMesh_polydata( hullPolydata, R , dx, dy, x_center = 0., y_center = 0. , side = +1, orderedCoord = None) :
    """ Create circulat free-surface mesh around a simple hull.

    :param Mesh hullMesh : hull mesh (full)
    :param float R : Radius of the free surface
    :param float dx : cell size
    :param float dy : cell size
    :param float x_center : free-surface center
    :param float y_center : free-surface center

    """
    #--- Create background free-surface mesh
    rect = createRectangularGrid( x_min = x_center - 2*R,
                                  x_max = x_center + 2*R,
                                  dx = dx,
                                  y_min = y_center - 2*R,
                                  y_max = y_center + 2*R,
                                  dy = dy )

    if orderedCoord is None:
        orderedCoord = extractWaterLine( hullPolydata, side = side )

    res = getHalfCircDomain( orderedCoord, r=R , n=100,  side = side, x_center = x_center, y_center = y_center )

    cont = createPolygon(res)
    cookie = vtk.vtkCookieCutter()
    cookie.SetInputData(rect)
    cookie.SetLoopsData(cont)
    cookie.Update()

    return cookie.GetOutput()


def createFreeSurfaceMesh( *args, **kwargs ):
    """
    Create a full free surface mesh around the hull, using cookieCutter

    :param Mesh hullMesh : hull mesh (full)
    :param float R : Radius of the free surface
    :param float dx : cell size
    :param float dy : cell size
    :param float x_center : free-surface center
    :param float y_center : free-surface center
    """

    fs1 = createHalfFreeSurfaceMesh(*args, side = +1, **kwargs)
    fs2 = createHalfFreeSurfaceMesh(*args, side = -1, **kwargs)
    fs1.append(fs2)
    return fs1


def createHalfFreeSurfaceMesh( hullMesh, R , dx, dy, x_center = 0., y_center = 0., side = +1, orderedCoord = None ) :
    """ Create circulat free-surface mesh around a hull.

    :param Mesh hullMesh : hull mesh (full)
    :param float R : Radius of the free surface
    :param float dx : cell size
    :param float dy : cell size
    :param float x_center : free-surface center
    :param float y_center : free-surface center
    """
    polydata = createHalfFreeSurfaceMesh_polydata(hullMesh.toVtkPolyData(), R, dx, dy, x_center, y_center, side=side, orderedCoord = orderedCoord )
    return msh.Mesh.FromPolydata(polydata)


def createPolygon( pointsArray ):
    """
    Create polydata with one polygon from ordered list of points
    """

    nTot = len(pointsArray)
    loops = vtk.vtkPolyData()
    loopPts = vtk.vtkPoints()
    loopPolys = vtk.vtkCellArray()
    loops.SetPoints(loopPts)
    loops.SetPolys(loopPolys)
    loopPts.SetNumberOfPoints(nTot)
    loopPolys.InsertNextCell(nTot)
    for i in range(nTot) :
        loopPts.SetPoint( i, pointsArray[i,:]  )
        loopPolys.InsertCellPoint(i)
    return loops


def createRectangularGrid(x_min, x_max, dx, y_min, y_max, dy):
    """
    Create a rectangular grid polydata
    """

    x_dim = int((x_max - x_min) / dx)
    y_dim = int((y_max - y_min) / dy)

    planeSource = vtk.vtkPlaneSource()
    planeSource.SetOrigin(x_min, y_min, 0.0)
    planeSource.SetPoint1(x_max, y_min, 0.0)
    planeSource.SetPoint2(x_min, y_max, 0.0)
    planeSource.SetXResolution(x_dim)
    planeSource.SetYResolution(y_dim)
    planeSource.Update()

    return planeSource.GetOutput()

def creatDiskGrid( r, dx, dy, x_center = 0, y_center = 0 ) :

    rect = createRectangularGrid( -r, +r, dx, -r, +r, dy )
    n_circ = 100
    circle = np.zeros( (n_circ,3), dtype = float )
    angle = np.linspace(0 , 2*np.pi, n_circ, endpoint = False)
    circle[:,0] = r*np.cos( angle )
    circle[:,1] = r*np.sin( angle )
    cont = createPolygon(circle)

    cookie = vtk.vtkCookieCutter()
    cookie.SetInputData(rect)
    cookie.SetLoopsData(cont)
    cookie.Update()
    return cookie.GetOutput()



