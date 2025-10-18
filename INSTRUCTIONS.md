# Instructions for Trash Management Simulation

## Requirements

- Python 3.x
- [Pygame](https://www.pygame.org/)
- [PyOpenGL](http://pyopengl.sourceforge.net/)

## Setup

1. **Create and activate a virtual environment:**

   On Linux/macOS:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

   On Windows:
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install the required Python packages:**
   ```sh
   pip install pygame PyOpenGL PyOpenGL_accelerate numpy
   ```

## Running the Simulation

Run the main simulation script:

```sh
python main.py
```

A window will open displaying a 3D city grid with autonomous garbage collection vehicles and trash objects.

## Controls

- **Arrow keys**: Rotate and elevate the camera view.
  - Left/Right: Rotate horizontally
  - Up/Down: Change elevation angle
- **Close window**: Exit the simulation