import os
import numpy as np
import subprocess
from matplotlib import pyplot as plt
from scipy.interpolate import InterpolatedUnivariateSpline
from Snoopy.Meshing.mesh_io import read_gridgen_c
from Snoopy.Meshing.waterline import getHalfCircDomain, getHalfWaterline


class Gridgen_case(object) :
    def __init__(self, name, inputGrid, boundary , gridgen_path):
        self.name = name

        self.inputGrid = inputGrid
        self.boundary = boundary

        self.inputFileName = f"{self.name}_gridgen.txt"
        self.boundaryFile = f"{self.name}_boundary.txt"
        self.outputFile = f"{self.name}_output.txt"
        self.inputGridFile = f"{self.name}_inputGrid.txt"

        self._nx = self.inputGrid.nx
        self._ny = self.inputGrid.ny

        self.gridgen_path = gridgen_path


    def write( self ):
        """
        Create the corresponding file for Gridgen's input
        """
        self.writeBoundary()
        self.inputGrid.write( self.inputGridFile )

        with open( self.inputFileName, 'w') as f :
            f.write(f'input {self.boundaryFile}\n')
            f.write(f'output {self.outputFile}\n')
            f.write(f'grid {self.inputGridFile}\n')
            #f.write( "rectangle {:}_rect.txt".format( self.name ) )

    def run(self) :
        self.write()
        subprocess.call(  [ self.gridgen_path, self.inputFileName] )
        self.correctOutputHeader()

    def correctOutputHeader(self) :
        """
        Define the dimensions at the first line of Gridgen's output file
        """
        Mat = np.loadtxt(self.outputFile)
        Dim = int( np.size(Mat)/2 )
        dat = open (self.outputFile, 'w')
        dat.write(f'##  {self.inputGrid.nx} x {self.inputGrid.ny}\n')
        for i in range (0,Dim):
            dat.write(str (Mat[i,0]) + ' ' + str(Mat[i,1]) + '\n')
        dat.close()

    def getOutputMesh(self):
        return read_gridgen_c(self.outputFile)

    def plotOutputMesh(self, ax = None):
        if ax is None:
            fig, ax = plt.subplots()
        self.getOutputMesh().plot2D(ax=ax)
        self.plotBoundary(ax=ax)
        return ax


    def plotBoundary(self, ax = None):
        if ax is None:
            fig, ax = plt.subplots()
        ax.scatter(  self.boundary[:,0], self.boundary[:,1] , c = np.arange( len(self.boundary) ) )
        return ax

    def clean(self):
        for file in [self.inputFileName, self.outputFile, self.boundaryFile, self.inputGridFile] :
            if os.path.exists(file) : os.remove(file)





class Gridgen_FSCase( Gridgen_case ):

    @classmethod
    def Build(cls, name, waterline, radius, nx = None, ny = None, forceWaterline = True, inputGrid = None, gridgen_path="gridgen.exe", side = +1) :
        """
        Create the corresponding file for Gridgen's input
        """

        halfWaterline = getHalfWaterline(waterline, side = side )

        if ny is not None :
            if inputGrid is not None :
                raise(ValueError("Either inputGrid or ny should be input, not both"))
            if nx is None:
                nx = len(halfWaterline)
            elif forceWaterline :
                raise(ValueError("Cannot force nx if forceWaterline is True"))
            inputGrid = StructuredGrid.BuildUniform(nx, ny )

        X0 = ( waterline[:,0].min() + waterline[:,0].max()) / 2.
        boundary = getHalfCircDomain( waterline, n = len(halfWaterline) , side = side, x_center=X0, r = radius )[::-1]
        res = cls( name , inputGrid, boundary = boundary, gridgen_path = gridgen_path)
        res.waterline = waterline
        res.halfWaterline = halfWaterline
        res.forceWaterline = forceWaterline
        res.radius = radius
        res.side = side
        return res

    def getMapping_waterline(self):
        """
        return interpolator from output curvilinear abscissa to input X
        """
        #Get output normed abscissa
        input_x = self.inputGrid.xs[:self._nx]
        output_xy = np.loadtxt (self.outputFile, skiprows = 1, max_rows = self._nx)
        output_c = distanceArray(output_xy, norm = True)
        if self.side > 0. :
            return input_x, output_c
        else:
            return input_x, 1-output_c

    def getNewInputGrid(self, forceWaterline = True, forceExternal = False) :

        if forceWaterline :
            x_in, x_out = self.getMapping_waterline()
            X_Waterline = distanceArray(self.halfWaterline, norm = True)
            spl = InterpolatedUnivariateSpline(self.side*x_out, x_in, k = 3)
            x = spl(self.side*X_Waterline)
        else:
            x = np.linspace(0, 1, self._nx)

        if forceExternal:
            raise(NotImplementedError)
        else:
            y = np.linspace(0, 1, self._ny)

        X, Y = np.meshgrid(x,y)
        return StructuredGrid( X.flatten(), Y.flatten(), self._nx, self._ny )

    def run(self):

        print ("Call Gridgen step 1")
        Gridgen_case.run(self)
        print ("Gridgen step 1 done")

        if self.forceWaterline :
            print ("Call Gridgen step 2")
            self = Gridgen_FSCase.Build( self.name, self.waterline, self.radius, inputGrid = self.getNewInputGrid(forceWaterline = True), side = self.side,
                                        forceWaterline=False, gridgen_path = self.gridgen_path )
            Gridgen_case.run(self)
            print ("Gridgen step 2 done")


    def writeBoundary(self):
        """
        Create the file with final points
        """

        if self.side > 0 :
            iStart = 0
        else:
            iStart = len(self.halfWaterline)-1
        with open (self.boundaryFile,'w') as f :
            for i, (x , y) in enumerate(self.boundary[:,:2]) :
                if i == iStart :
                    f.write( f"{x}  {y}  1*\n")
                else:
                    if ( abs(y) < 1e-5) :
                        f.write ( f" {x} {y} 1\n")
                    else:
                        f.write ( f" {x} {y}\n")



def writeWaterline( waterLineCoords, filename ) :
    with open(filename , "w") as f:
        f.write( "Waterline\n")
        for i in range(len(waterLineCoords)) :
            f.write( f"{waterLineCoords[i,0]}  {waterLineCoords[i,1]}\n" )


def writeGrid(filename, xVect, yVect, nx, ny):
    """
    Write structured grid to gridgen format
    """
    assert(len(xVect) == nx*ny )
    assert(len(yVect) == nx*ny )

    data = open (filename, 'w')
    data.write('# ' + str(nx) + ' x ' + str(ny) + '\n')
    for i in range(len(xVect)):
        data.write(str(xVect[i]) + ' ' + str(yVect[i]) + '\n')





class StructuredGrid(object):
    def __init__( self, xs, ys, nx, ny ):
        self.xs = xs
        self.ys = ys
        self.nx = nx
        self.ny = ny

    def write(self, filename) :
        writeGrid(filename, self.xs, self.ys, self.nx, self.ny)


    @classmethod
    def BuildUniform( cls, nx, ny ):
        x = np.linspace(0, 1, nx)
        y = np.linspace(0, 1, ny)
        xs, ys = np.meshgrid(x,y)
        return cls( xs.flatten(), ys.flatten(), nx, ny )





def distanceArray(xy, norm = False):
    """
    Basical function which calculates distance of a structure defined by points (2D)
    """
    n = len(xy)
    res = np.zeros( (n) )
    tab1 = abs(xy[1:n,:] - xy[0:n-1,:])**2
    Deltas_x_y = np.sqrt(tab1[:,0] + tab1[:,1])
    for i in range(n-1):
        res[i+1] += res[i] + Deltas_x_y[i]

    if norm :
        res /= (res.max() - res.min())
    return res



"""
Nikola routine for structured grid with different X and Y on both side, unused for now
"""
def Coeffs_Linear_Function(Point1, Point2):
    """
    find the cofficients of a linear function (y = kx+l) defined by 2 point
    """
    if (Point1[0] == Point2[0]):
        k = 0
        l = Point1[0]
    else:
        k =  (Point2[1]-Point1[1])/(Point2[0]-Point1[0])
        l =  Point1[1] + k*(Point1[0])

    return k, l

def meshgrid_linear(x_Axe1, y_Axe1, x_Axe2, y_Axe2) :
    """
    An alternative Meshgrid for different parallel axices
    """
    nx = len(x_Axe1)
    ny = len(y_Axe1)
    X_axis1 = np.zeros( (nx,2) )
    Y_axis1 = np.zeros( (ny,2) )
    X_axis2 = np.ones( (nx,2) )
    Y_axis2 = np.ones( (ny,2) )
    X_axis1[:,0] = x_Axe1
    Y_axis1[:,1] = y_Axe1
    X_axis2[:,0] = x_Axe2
    Y_axis2[:,1] = y_Axe2
    X = []
    Y = []
    if (np.array_equiv( X_axis1[:,0], X_axis2[:,0]) and np.array_equiv( Y_axis1[:,1], Y_axis2[:,1])):
        for i in range (ny) :
            for j in range (nx) :
                X.append(X_axis1[j,0])
                Y.append(Y_axis1[i,1])
    else:
        for i in range (ny) :
            k1, l1 = Coeffs_Linear_Function(Y_axis1[i,:], Y_axis2[i,:])

            for j in range (nx) :
                k2, l2 = Coeffs_Linear_Function(X_axis1[j,:], X_axis2[j,:])
                k = k2
                l = l1 + l2

                if(k != 0):
                    x_Grid = np.linalg.tensorsolve(k,l)
                    y_Grid = l1

                else:
                    x_Grid = X_axis1[j,0]
                    y_Grid = Y_axis1[i,1]
                X.append(x_Grid)
                Y.append(y_Grid)

    Matrix_X = np.reshape(X, (ny,nx))
    Matrix_Y = np.reshape(Y, (ny,nx))
    return Matrix_X, Matrix_Y

