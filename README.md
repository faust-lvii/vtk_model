# VTK Model Renderer

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![VTK](https://img.shields.io/badge/VTK-Latest-green.svg)](https://vtk.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## Overview

VTK Model Renderer is a sophisticated 3D visualization application built using the Visualization Toolkit (VTK). This application enables users to load and visualize STL files with an interactive 3D interface, featuring a rotating cube around the loaded model for enhanced spatial reference.

## Demonstration

<div align="center">
  <img src="mymodel.gif" alt="VTK Model Renderer Demo" width="600"/>
</div>

## Features

- Real-time 3D model visualization
- STL file format support
- Interactive rotating cube animation
- Mouse-based camera controls
- Professional rendering quality
- Zoom and pan capabilities

## Installation

### Prerequisites

- Python 3.x
- VTK library

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/faust-lvii/vtk_model.git
cd vtk_model
```

2. Install required dependencies:
```bash
pip install vtk
```

## Usage

1. Place your STL model file in the project directory as `model.stl`
2. Run the application:
```bash
python renderer.py
```

### Controls

- **Left Mouse Button**: Rotate the camera
- **Middle Mouse Button**: Pan the view
- **Right Mouse Button**: Zoom in/out
- **R Key**: Reset camera position

## Technical Details

The application utilizes VTK's powerful rendering pipeline to create high-quality 3D visualizations. Key components include:

- VTK's STL reader for model loading
- Custom animation system for cube rotation
- Optimized rendering pipeline
- Interactive camera control system

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please:
- Open an issue in the GitHub repository
- Contact the development team

## Acknowledgments

- VTK Development Team for the excellent visualization library
- Contributors and users of this project