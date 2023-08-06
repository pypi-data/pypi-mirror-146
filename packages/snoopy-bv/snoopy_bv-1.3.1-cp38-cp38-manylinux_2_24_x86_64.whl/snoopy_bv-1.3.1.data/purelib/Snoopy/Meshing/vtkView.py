from Snoopy.Meshing.colorMapSelector import matplotlib_to_vtkLut




def viewPolyData( polydata, *, cellFieldName = None, cellCmap = "Blues"):
    import vtk
    actor = getPolydataActor(  polydata, cellFieldName = cellFieldName, cellCmap = cellCmap )
    
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(800, 600)
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindowInteractor.SetInteractorStyle( vtk.vtkInteractorStyleTrackballCamera() )

    renderer.AddActor(actor)
    renderWindow.Render()
    renderWindowInteractor.Start()


def getPolydataActor( polydata, *, cellFieldName = None, cellCmap = "Blues" ):
    import vtk

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData( polydata )

    if cellFieldName is not None :
        mapper.SetLookupTable( matplotlib_to_vtkLut( cellCmap ) )
        mapper.SetScalarModeToUseCellFieldData()
        mapper.SelectColorArray( cellFieldName )

    mapper.SetScalarRange( 0.0,  10.0)
    mapper.SetUseLookupTableScalarRange(False)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetEdgeVisibility(1)
    return actor


def polydataPicture( polydata, *, cellFieldName = None, cellCmap = "Blues", outputFile ):
    import vtk
    w2if = vtk.vtkRenderLargeImage()
    #w2if.SetMagnification(4)   # => Resoulition of the picture
    
    actor = getPolydataActor(  polydata, cellFieldName = cellFieldName, cellCmap = cellCmap )
    
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(800, 600)
    
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(1, 1, 1)  # White background
    renderer.AddActor(actor)
    renderWindow.AddRenderer(renderer)

    
    w2if.SetInput(renderer)
    w2if.Update()

    writer = vtk.vtkPNGWriter()
    writer.SetFileName(outputFile)
    writer.SetInputConnection(w2if.GetOutputPort())
    writer.Write()

