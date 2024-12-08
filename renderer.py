import vtk

# STL dosyasını yükle
reader = vtk.vtkSTLReader()
reader.SetFileName("model.stl")
reader.Update()

# Model boyutlarını al
bounds = reader.GetOutput().GetBounds()
size = max(bounds[1]-bounds[0], bounds[3]-bounds[2], bounds[5]-bounds[4])

# Modelin merkez noktasını hesapla
center_x = (bounds[0] + bounds[1]) / 2
center_y = (bounds[2] + bounds[3]) / 2
center_z = (bounds[4] + bounds[5]) / 2

# Küp oluştur - modelden 2 kat büyük
cube = vtk.vtkCubeSource()
cube.SetXLength(size * 1.2)  # 2'den 1.2'ye küçültüldü
cube.SetYLength(size * 1.2)  # 2'den 1.2'ye küçültüldü
cube.SetZLength(size * 1.2)  # 2'den 1.2'ye küçültüldü
cube.SetCenter(center_x +0.5, center_y, center_z -4)  # Küpü modelin merkezine hizala

# Küp için mapper ve actor
cube_mapper = vtk.vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube.GetOutputPort())

cube_actor = vtk.vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.GetProperty().SetRepresentationToWireframe()  # Tel kafes görünümü
cube_actor.GetProperty().SetColor(1, 1, 1)  # Beyaz renk
cube_actor.GetProperty().SetLineWidth(2)  # Çizgi kalınlığı

# Mapper oluştur (ana model için)
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# Actor oluştur (modelin sahneye eklenmesi için)
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.SetPosition(-center_x, -center_y, -center_z)  # Modeli merkeze taşı

# Renderer (çizim yapan birim) oluştur
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(cube_actor)  # Küpü ekle
renderer.SetBackground(0, 0, 0)  # Arkaplan rengi (RGB)

# Render Window oluştur
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 800)  # Pencere boyutu 800x800 olarak ayarlandı

# Render Window Interactor (etkileşim) oluştur
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Kamera ayarlarını düzenle
camera = renderer.GetActiveCamera()
camera.SetPosition(0, -30, 25)  # Kamerayı z ekseninde konumlandır
camera.SetFocalPoint(0, 3, -1)  # Merkeze bak
camera.SetViewUp(0, 1, 0)      # Yukarı yönü belirle

# Döndürme fonksiyonu
def rotate_model(obj, event):
    actor.RotateZ(1)  # Z ekseni etrafında döndür
    render_window.Render()

# Timer callback'i ekle
interactor.AddObserver('TimerEvent', rotate_model)
interactor.Initialize()

# Timer başlat
timer_id = interactor.CreateRepeatingTimer(30)  # 30ms'de bir güncelle

# Görselleştirmeyi başlat
render_window.Render()
interactor.Start()
