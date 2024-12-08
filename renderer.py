import vtk

# Load STL file
reader = vtk.vtkSTLReader()
reader.SetFileName("model.stl")
reader.Update()

# Get model dimensions
bounds = reader.GetOutput().GetBounds()
size = max(bounds[1]-bounds[0], bounds[3]-bounds[2], bounds[5]-bounds[4])

# Calculate model center point
center_x = (bounds[0] + bounds[1]) / 2
center_y = (bounds[2] + bounds[3]) / 2
center_z = (bounds[4] + bounds[5]) / 2

# Create cube - 1.2 times larger than the model
cube = vtk.vtkCubeSource()
cube.SetXLength(size * 1.2)  # Reduced from 2 to 1.2
cube.SetYLength(size * 1.2)  # Reduced from 2 to 1.2
cube.SetZLength(size * 1.2)  # Reduced from 2 to 1.2
cube.SetCenter(center_x +0.5, center_y, center_z -4)  # Align cube to model center

# Mapper and actor for cube
cube_mapper = vtk.vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube.GetOutputPort())

cube_actor = vtk.vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.GetProperty().SetRepresentationToWireframe()  # Wireframe view
cube_actor.GetProperty().SetColor(1, 1, 1)  # White color
cube_actor.GetProperty().SetLineWidth(2)  # Line width

# Create mapper (for main model)
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# Create actor (to add model to scene)
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.SetPosition(-center_x, -center_y, -center_z)  # Move model to center

# Create renderer (drawing unit)
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(cube_actor)  # Add cube
renderer.SetBackground(0, 0, 0)  # Background color (RGB)

# Create render window
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 800)  # Window size set to 800x800

# Create render window interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Configure camera settings
camera = renderer.GetActiveCamera()
camera.SetPosition(0, -30, 25)  # Position camera on z-axis
camera.SetFocalPoint(0, 3, -1)  # Look at center
camera.SetViewUp(0, 1, 0)      # Set up direction

# Rotation function
def rotate_model(obj, event):
    actor.RotateZ(1)  # Rotate around z-axis
    render_window.Render()

# Add timer callback
interactor.AddObserver('TimerEvent', rotate_model)
interactor.Initialize()

# Start timer
timer_id = interactor.CreateRepeatingTimer(30)  # Update every 30ms

# Start visualization
render_window.Render()
interactor.Start()
