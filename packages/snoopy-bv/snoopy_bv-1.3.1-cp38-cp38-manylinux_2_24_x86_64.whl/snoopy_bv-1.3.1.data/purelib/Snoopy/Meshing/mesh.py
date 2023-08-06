import os
import numpy as np
from vtk.util import numpy_support
import _Meshing
from Snoopy import Geometry as geo
from Snoopy import logger



class Mesh(_Meshing.Mesh):


    @property
    def nbpanels(self):
        return len(self.quads) + len(self.tris)

    @property
    def nbtris(self):
        return len(self.tris)

    @property
    def nbquads(self):
        return len(self.quads)

    @property
    def nbnodes(self):
        return len(self.nodes)


    @property
    def hasPanelData(self):
        return self.getPanelsData().shape[1] > 0

    def getDataRange(self) :

        if self.hasPanelData:
            return np.min(self.getPanelsData()), np.max(self.getPanelsData())
        else :
            return [np.nan , np.nan]


    def integrate_volume_py(self, direction = 2, nbGP = 1) :
        """ Compute and return the mesh volume
            param direction : integration direction (0=>x, 1=>y, 2=>z)

            V = $\int_{M} n_x * x * ds$  (for direction=0)
        """
        if nbGP is not None :
            self.refreshGaussPoints(nbGP)
        gp = self.getGaussPoints()
        normals = self.getNormalsAtGaussPoints()
        weight = self.getGaussWiWjdetJ()
        return np.sum(gp[:,direction] * normals[:,direction] * weight)
    
    
    def integrate_waterPlaneArea(self, nbGP = 1):
        if nbGP is not None :
            self.refreshGaussPoints(nbGP)
        gp = self.getGaussPoints()
        normals = self.getNormalsAtGaussPoints()
        weight = self.getGaussWiWjdetJ()
        return -np.sum(normals[:,2] * weight)
    

    def integrate_cob_py(self, nbGP = 1):
        """ Compute and return the center of buoyancy (Assuming closed hull, with free-surface at z=0)
        """
        if nbGP is not None :
            self.refreshGaussPoints(nbGP)

        volume = self.integrate_volume(nbGP =nbGP)
        gp = self.getGaussPoints()
        normals = self.getNormalsAtGaussPoints()
        weight = self.getGaussWiWjdetJ()
        x = np.sum(gp[:,2] * normals[:,2] * gp[:,0] * weight)
        y = np.sum(gp[:,2] * normals[:,2] * gp[:,1] * weight)
        z = np.sum(0.5*(gp[:,0] * normals[:,0] + gp[:,1] * normals[:,1]) * gp[:,2] * weight)
        return np.array([x,y,z]) / volume
    
    def integrate_waterPlaneCenter(self, nbGP = 1):
        Sw = self.integrate_waterPlaneArea(nbGP = nbGP)
        Aw = np.zeros(3,dtype='float')
        
        if nbGP is not None :
            self.refreshGaussPoints(nbGP)
        gp = self.getGaussPoints()
        normals = self.getNormalsAtGaussPoints()
        weight = self.getGaussWiWjdetJ()
        
        Aw[0:2] = -np.sum(gp[:,0:2] * (normals[:,2] * weight).reshape(-1,1), axis=0) / Sw
        
        return Aw
    
    

    def write(self, filename, *args, **kwargs):

        p = os.path.dirname(filename)
        if p and not os.path.exists( p ) :
            os.makedirs( p )

        if os.path.splitext(filename)[-1] in [".hst",".hs0"] :
            self.writeHydroStar(filename, *args, **kwargs)
        else :
            _Meshing.Mesh.write(self, filename, *args, **kwargs)


    @classmethod
    def ReadVtu(cls, filename, polygonHandling = "ignore"):
        """Read .vtu files

        Parameters
        ----------
        filename : str
            Filename

        Returns
        -------
        msh.Mesh
            Read mesh

        """
        import vtk
        reader = vtk.vtkXMLUnstructuredGridReader()
        reader.SetFileName(filename)
        reader.Update()
        return Mesh.FromPolydata( reader.GetOutput(), polygonHandling=polygonHandling )


    def writeHydroStar(self, filename, panelType=1):
        """Write to HydroStar format
        """

        s_nodes = ""
        for i, n in enumerate(self.nodes) :
            s_nodes += "{:} {:.5e} {:.5e} {:.5e}\n" .format( i+1 , *n)

        s_panels = ""
        ipanel = 1
        for n in self.quads :
            n_off = n + 1
            if panelType == 0: s_panels += "{} {} {} {}\n".format( *n_off )
            else: s_panels += "{} {} {} {} {}\n".format( ipanel, *n_off )
            ipanel += 1

        for n in self.tris :
            n_off = n + 1
            if panelType == 0: s_panels += "{} {} {}\n".format( *n_off )
            else:  s_panels += "{} {} {} {}\n".format( ipanel, *n_off )
            ipanel += 1

        with open(filename, "w") as f :
            f.write( "NUMPANEL 1 1 {}\n".format(self.nbpanels))
            f.write( "COORDINATES\n{:}ENDCOORDINATES\n".format(s_nodes) )
            if panelType == 0: f.write( "PANEL TYPE 0\n{:}ENDPANEL\n".format(s_panels))
            else: f.write( "PANEL TYPE 1\n{:}ENDPANEL\n".format(s_panels))
            f.write( "ENDFILE")
        return


    def writeMsh( self, filename  ):
        """ Write to msh (Moloh)
        """

        s_nodes = ""
        for i, n in enumerate(self.nodes) :
            s_nodes += "{:} {:.5e} {:.5e} {:.5e}\n" .format( i+1 , *n)


        s_panels = ""
        ipanel = 1
        for n in self.quads :
            n_off = n + 1
            s_panels += "{} {} {} {} {} 1 0\n".format( ipanel, *n_off )
            ipanel += 1

        for n in self.tris :
            n_off = n + 1
            s_panels += "{} {} {} {} {} 1 0\n".format( ipanel, *n_off, n_off[-1] )
            ipanel += 1

        with open(filename, "w") as f :
            f.write( "NODES\n{:}ENDNODES\n".format(s_nodes) )
            f.write( "PANELS\n{:}ENDPANELS\n".format(s_panels))
            f.write( "GROUPS\n1 Hull\nENDGROUPS")

        return



    def getCb(self):
        dims = [ a[1]-a[0] for a in self.getBounds() ]
        return self.integrate_volume() / np.prod( dims )


    def __str__(self) :
        """
        """

        if self.nbnodes == 0 :
            return "Empty mesh"

        s = """
#------- Mesh object ------------------------#
Number of nodes  : {:}
Number of panels : {:}  ({:} QUAD and {:} TRIS)
Length      : {:.1f}
Beam        : {:.1f}
Draft/Depth : {:.1f}
Volume      : {:.1f}
Bounds : x=[{:8.2f},{:8.2f}]
         y=[{:8.2f},{:8.2f}]
         z=[{:8.2f},{:8.2f}]
#--------------------------------------------#"""
        return s.format( self.nbnodes, self.nbpanels, self.nbquads, self.nbtris,
                         self.getBounds()[0][1] - self.getBounds()[0][0],
                         self.getBounds()[1][1] - self.getBounds()[1][0],
                         self.getBounds()[2][1] - self.getBounds()[2][0],
                         self.integrate_volume(),
                         *[item for sublist in self.getBounds() for item in sublist] )


    def getBounds(self) :
        return [(np.min(self.nodes[:,0]), np.max(self.nodes[:,0])) ,
                (np.min(self.nodes[:,1]), np.max(self.nodes[:,1])) ,
                (np.min(self.nodes[:,2]), np.max(self.nodes[:,2])) ]



    def rotateAxis( self, axis=[0.,1.,0.], angle=0. ):
        """ Rotate a mesh around axis given by vector (angle in radians)

        """
        if angle != 0.:
            v = geo.Vector(axis)
            v.normalise()
            rmat = np.transpose(geo.AxisAndAngle(v,angle).getMatrix())

            self.setVertices( np.matmul(self.getVertices(),rmat) )

    def rotateZYX( self, center=[0.,0.,0.], angle=[0.,0.,0.] ):
        """ Rotate a mesh around center with Euler angles [roll, pitch, yaw] (angle in radians)

        """
        if any(angle) != 0.:
            rmat = geo.EulerAngles_XYZ_e(*angle).getMatrix()

            #Apply rotation around center : V' = [rmat]*[V-center] + center
            self.offset([-1.*i for i in center])
            self.setVertices( np.transpose(np.matmul(rmat,np.transpose(self.getVertices()))) )
            self.offset(center)

    @staticmethod
    def convertToVtk(mesh, offset=(0., 0., 0.)):
        """Copy mesh to vtk polydata structure
        """
        import vtk
        polydata = vtk.vtkPolyData()
        points = vtk.vtkPoints()

        polydata.SetPoints(points)
        cells = vtk.vtkCellArray()
        polydata.SetPolys(cells)

        for xyz in mesh.nodes:
            points.InsertNextPoint( xyz + offset)

        for panel in mesh.tris :
            polydata.InsertNextCell( vtk.VTK_TRIANGLE, 3, panel  )

        for panel in mesh.quads :
            polydata.InsertNextCell( vtk.VTK_QUAD, 4, panel  )

        if mesh.hasPanelsData():
            dataArray = numpy_support.numpy_to_vtk(mesh.getPanelsData())
            dataArray.SetName("Porosity")
            polydata.GetCellData().AddArray( dataArray )

        return polydata

    def toVtkPolyData(self, offset=(0., 0., 0.)):
        return Mesh.convertToVtk(self, offset)

    def vtkView(self, *args, **kwargs) :
        """ Display mesh with vtk
        """
        from .vtkView import viewPolyData
        viewPolyData(self.toVtkPolyData(), *args, **kwargs)

    def toImage(self, outputFile, **kwargs):
        from .vtkView import polydataPicture
        polydataPicture(self.toVtkPolyData(), outputFile = outputFile, **kwargs)


    @classmethod
    def FromPolydata(cls, polydata, polygonHandling = "triangulate"):
        """ Fill Mesh instance from vtk grid """
        import vtk
        from vtk.util import numpy_support
        points = polydata.GetPoints()

        etris = np.zeros( (0,3), dtype = int)
        equads = np.zeros( (0,4), dtype = int)

        if points is None :
            return cls( Vertices = np.zeros( (0,3), dtype = float ), Tris = etris, Quads = equads  )
        elif polydata.GetPoints().GetNumberOfPoints() == 0:
            return cls( Vertices = np.zeros( (0,3), dtype = float ), Tris = etris, Quads = equads  )


        nodes = numpy_support.vtk_to_numpy(  points.GetData() )

        # Get cell data
        idList = vtk.vtkIdList()
        quads = []
        tris = []
        notHandled = []
        for ipanel in range(polydata.GetNumberOfCells()):
            polydata.GetCellPoints(ipanel, idList)

            nNodes = idList.GetNumberOfIds()

            nodesId = [idList.GetId(i) for i in range(nNodes)]

            if nNodes == 4:
                quads.append( nodesId )
            elif nNodes == 3:
                tris.append( nodesId )
            elif polygonHandling == "triangulate" :  # Polygon, to be triangulated
                nodesId = np.array(nodesId)
                notHandled.append( ipanel )
                trisIds = vtk.vtkIdList()
                polydata.GetCell(ipanel).Triangulate(trisIds)
                for itri in range( trisIds.GetNumberOfIds() // 3 ):
                    subId = [ trisIds.GetId( itri*3 + 0 ), trisIds.GetId( itri*3 + 1 ), trisIds.GetId( itri*3 + 2 ) ]
                    tris.append( nodesId[subId] )

        if len(tris) == 0:
            tris = etris
        else :
            tris = np.array(tris, dtype = int)

        if len(quads) == 0:
            quads = equads
        else :
            quads = np.array(quads, dtype = int)

        return cls( Vertices = nodes, Tris = tris, Quads = quads  )



    def extractWaterLineSegments(self, eps=1e-4):
        #Extract all segments
        seg = self.getSegments()

        #Segments at z=0
        zSeg = np.max( np.abs(self.nodes[:,2][seg]) , axis = 1)
        waterline = seg[ np.where( zSeg < eps )[0]]
        return waterline



    def checkTightWaterlines( self , waterline ) :
        """


        Parameters
        ----------
        waterline : np.ndarray
            Waterline segments (nodes connectivity)

        Returns
        -------
        bool
            True if waterline is closed.

        """

        wl = waterline.flatten()
        unique, counts = np.unique(wl, return_counts=True)

        id_free = np.where( counts != 2 )
        if len (id_free[0]) == 0 :
            return True
        else :
            logger.debug( self.nodes[ unique[id_free] ]  )
            return False



    def extractWaterLineLoops(self, eps=1e-4):
        """ Regroup waterline per loops


        Parameters
        ----------
        eps : TYPE, optional
            DESCRIPTION. The default is 1e-4.

        Returns
        -------
        list_loop : list
            List of waterline closed loops

        """
        waterline = self.extractWaterLineSegments(eps)

        if not self.checkTightWaterlines(waterline) :
            raise(Exception( "Can not clear waterplane, waterline is not closed" ))

        logger.debug( f"{len(waterline):} waterline segments extracted" )

        #Check loops are closed :
        if not (np.sort( waterline[:,0] ) == np.sort( waterline[:,1] )).all():
            logger.info( "Waterline is not closed" )
            return []

        #TO DO : optimize (with sorting ?)
        done = []
        list_loop = []
        while len(done) != len(waterline):
            for iSegNotDone in range(len(waterline)) :
                if iSegNotDone not in done :
                    break
            loop = [ waterline[ iSegNotDone  ] ]
            done.append(iSegNotDone)
            while loop[0][0] != loop[-1][1] :
                ic = np.where( waterline[:,0] == loop[-1][1] )[0][0]
                loop.append( waterline[ic] )
                done.append(ic)
            list_loop.append(loop)
        return list_loop


    def extractWaterline(self, eps = 1e-4):
        """ Extract waterline from hull mesh.
        Return array of node ids.
        """

        waterline = self.extractWaterLineSegments(eps)


        #Ensure continous contour
        startSeg = 0
        orderWaterLine = np.empty( waterline.shape, dtype = int )
        orderWaterLine[0,:] = waterline[startSeg,:]
        for i in range(1, len(waterline) ) :
            ic = np.where( waterline[:,0] == orderWaterLine[i-1,1] )[0][0]
            orderWaterLine[i,:] = waterline[ic,:]

        #Start from aft central point
        symPlane = np.where( np.abs(self.nodes[ orderWaterLine[:,0], 1 ]) < eps )[0]
        if len(symPlane) > 0:
            startNode = orderWaterLine[symPlane[ np.argmax(  self.nodes[orderWaterLine[symPlane,0], 0]  ) ],0]
            orderWaterLine = np.roll( orderWaterLine, -np.where(orderWaterLine[:,0] == startNode)[0][0] , axis = 0)

        return orderWaterLine


    def extractWaterlineCoords(self, eps = 1e-4):
        """ Return waterline, as table of coordinates xyz
        """
        nodesId = self.extractWaterline(eps=eps)
        return self.nodes[ nodesId[:,0] ]


    def getWaterlineBound( self ):
        """Return waterline bounds
        """

        nodes = self.extractWaterlineCoords()

        return [ (np.min( nodes[:,0] ), np.max( nodes[:,0])   ),
                 (np.min( nodes[:,1] ), np.max( nodes[:,1] )  ),
                 (np.min( nodes[:,2] ), np.max( nodes[:,2] )  )]



    def plotWaterline(self, ax=None, eps = 1e-4, **kwargs):
        from matplotlib import pyplot as plt
        if ax is None :
            fig, ax = plt.subplots()

        orderWaterLine = self.extractWaterline(eps = eps)
        ax.plot( self.nodes[ orderWaterLine.flatten() , 0 ], self.nodes[ orderWaterLine.flatten() , 1 ], "-", **kwargs )
        return ax

    def plotWaterlineLoops(self, ax=None, eps = 1e-4, **kwargs):
        from matplotlib import pyplot as plt
        if ax is None :
            fig, ax = plt.subplots()
        loops = self.extractWaterLineLoops()
        for loop in loops :
            for seg in loop:
                ax.plot( self.nodes[seg][:,0], self.nodes[seg][:,1], "-" )
        return ax


    def plot2D(self, *args, **kwargs):
        """Plot surface mesh (z coordinates ignored) with matplotlib
        """
        from droppy.pyplotTools import plotMesh
        return plotMesh( self.nodes, self.quads, self.tris, *args, **kwargs)



#Make C++ wrapped function return the python subclass. Warning : Make a copy
for method in ["getCutMesh"]:
    def makeFun(method):
        fun = getattr(_Meshing.Mesh, method)
        def newFun(*args,**kwargs) :
            return Mesh(fun(*args, **kwargs))
        newFun.__doc__ = fun.__doc__
        return newFun
    setattr(Mesh, method+"Copy", makeFun(method))





