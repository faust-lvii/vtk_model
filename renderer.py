import vtk
import random
import math

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

# Create 3D cube using lines
def create_3d_cube(size, center, renderer):
    # Calculate cube vertices
    half_size = size * 0.6  # Half the size for the cube
    vertices = [
        [center[0] - half_size, center[1] - half_size, center[2] - half_size],  # 0
        [center[0] + half_size, center[1] - half_size, center[2] - half_size],  # 1
        [center[0] + half_size, center[1] + half_size, center[2] - half_size],  # 2
        [center[0] - half_size, center[1] + half_size, center[2] - half_size],  # 3
        [center[0] - half_size, center[1] - half_size, center[2] + half_size],  # 4
        [center[0] + half_size, center[1] - half_size, center[2] + half_size],  # 5
        [center[0] + half_size, center[1] + half_size, center[2] + half_size],  # 6
        [center[0] - half_size, center[1] + half_size, center[2] + half_size]   # 7
    ]
    
    # Define edges (vertex pairs)
    edges = [
        [0, 1], [1, 2], [2, 3], [3, 0],  # Bottom face
        [4, 5], [5, 6], [6, 7], [7, 4],  # Top face
        [0, 4], [1, 5], [2, 6], [3, 7]   # Vertical edges
    ]
    
    # Create diagonal lines for 3D effect
    diagonals = [
        [0, 6], [1, 7], [2, 4], [3, 5],  # Cross diagonals
        [0, 2], [1, 3], [4, 6], [5, 7],  # Face diagonals
        [0, 5], [1, 4], [2, 7], [3, 6]   # Mixed diagonals
    ]
    
    # Combine all lines
    all_lines = edges + diagonals
    
    # Create actors for each line
    line_actors = []
    for start_idx, end_idx in all_lines:
        line_source = vtk.vtkLineSource()
        line_source.SetPoint1(vertices[start_idx])
        line_source.SetPoint2(vertices[end_idx])
        
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(line_source.GetOutputPort())
        
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1, 1, 1)  # White color
        actor.GetProperty().SetLineWidth(2)
        
        renderer.AddActor(actor)
        line_actors.append(actor)
    
    return line_actors

# Create mapper (for main model)
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# Create actor (to add model to scene)
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.SetPosition(-center_x, -center_y, -center_z)

# Create animated lines
class AnimatedLine:
    def __init__(self, renderer, start_point):
        self.line_source = vtk.vtkLineSource()
        self.line_source.SetPoint1(start_point)
        
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(self.line_source.GetOutputPort())
        
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        self.actor.GetProperty().SetColor(1, 1, 1)
        self.actor.GetProperty().SetLineWidth(2)
        self.actor.GetProperty().SetOpacity(0.15)
        
        # Enable transparency
        self.actor.GetProperty().SetAmbient(0.3)
        self.actor.GetProperty().SetDiffuse(0.7)
        self.actor.GetProperty().SetSpecular(0.2)
        
        renderer.AddActor(self.actor)
        
        # Animation parameters
        self.speed = 0.5
        self.start_pos = list(start_point)
        self.current_pos = list(start_point)
        self.generate_random_length()
        
    def generate_random_length(self):
        # Generate random length between size*1 and size*4
        self.length = random.uniform(size * 1, size * 4)
        
    def update(self):
        # Move the line from left to right
        self.current_pos[0] += self.speed
        
        # Update line position
        self.line_source.SetPoint1(self.current_pos)
        end_point = [
            self.current_pos[0] + self.length,
            self.current_pos[1],
            self.current_pos[2]
        ]
        self.line_source.SetPoint2(end_point)
        
        # Reset position if line has moved too far and generate new random length
        if self.current_pos[0] > size * 6:
            self.current_pos = list(self.start_pos)
            self.generate_random_length()

# Create renderer
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0, 0, 0)

# Enable transparency in renderer
renderer.UseDepthPeelingOn()
renderer.SetMaximumNumberOfPeels(4)
renderer.SetOcclusionRatio(0.1)

# Create 3D cube
cube_center = [center_x + 0.5, center_y, center_z - 4]
cube_actors = create_3d_cube(size, cube_center, renderer)

# Create animated lines
animated_lines = []
num_lines = 16  # Total number of lines
total_path_length = size * 12  # Increased total path length
spacing = total_path_length / num_lines

# Create lines at different heights and positions
for i in range(num_lines):
    # Stagger starting positions along X-axis
    start_x = -size * 6  # Start further left
    
    # Distribute lines in a grid pattern
    row = i // 4
    col = i % 4
    
    # Calculate Y and Z positions for grid arrangement
    start_y = -size * 0.6 + col * (size * 0.4)  # Spread in Y direction
    start_z = center_z - size * 0.6 + row * (size * 0.4)  # Spread in Z direction
    
    line = AnimatedLine(renderer, [start_x, start_y, start_z])
    animated_lines.append(line)

# Create render window with low resolution
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(720, 480)

# Add pixelation effect
image_filter = vtk.vtkWindowToImageFilter()
image_filter.SetInput(render_window)
image_filter.SetScale(1)
image_filter.SetInputBufferTypeToRGB()

# Create texture and apply pixelation
texture = vtk.vtkTexture()
texture.SetInputConnection(image_filter.GetOutputPort())
texture.InterpolateOff()

# Create interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Configure camera settings
camera = renderer.GetActiveCamera()
camera.SetPosition(0, -30, 25)
camera.SetFocalPoint(0, 3, -1)
camera.SetViewUp(0, 1, 0)

# Animation function
def animate(obj, event):
    # Rotate the main model
    actor.RotateZ(1)
    
    # Rotate all cube lines
    for cube_actor in cube_actors:
        cube_actor.RotateZ(-1)
    
    # Update animated lines
    for line in animated_lines:
        line.update()
    
    image_filter.Modified()
    render_window.Render()

# Add timer callback
interactor.AddObserver('TimerEvent', animate)
interactor.Initialize()

# Start timer
timer_id = interactor.CreateRepeatingTimer(30)

# Start visualization
render_window.Render()
interactor.Start()
