# FreeCAD Robotic Arm Simulation

## Overview

This repository contains Python code for creating and simulating a 3D model of a vertical robot arm with revolute joints using FreeCAD. The simulation demonstrates forward kinematics principles and allows for interactive control of the robot arm's movement.

## Features

- **Parametric Design**: Easily adjustable dimensions for all components
- **Multiple Links**: Three-link arm configuration with square cross-section
- **Revolute Joints**: Two rotational joints with proper kinematic behavior
- **Forward Kinematics**: Realistic movement simulation where rotating a joint affects all dependent components
- **Interactive Control**: Function to rotate joints with customizable angles

## Technical Implementation

The robotic arm model consists of:

- **Base**: Cylindrical platform (foundation)
- **Links**: Three vertical rectangular prisms forming the arm structure
- **Joints**: Two cylindrical revolute joints connecting the links
- **Connector**: Small reference component attached to the base

## Prerequisites

- FreeCAD (v0.19 or newer recommended)
- Python 3.x
- Basic knowledge of CAD and robotics concepts

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/freecad-robot-arm.git
   ```

2. Open FreeCAD and navigate to the Macro menu

3. Select "Create..." and paste the code or "Run..." to execute the saved macro file

## Usage

The script will automatically create the robot arm model when executed. After creation, you can use the `rotate_joint()` function to control the arm:

```python
# Rotate the first joint by 30 degrees
rotate_joint(1, 30)

# Rotate the second joint by 45 degrees
rotate_joint(2, 45)
```

The function parameters are:
- `joint_num`: Which joint to rotate (1 or 2)
- `angle_deg`: Rotation angle in degrees

## How It Works

### Forward Kinematics

The `rotate_joint()` function implements forward kinematics to simulate realistic movement:

```python
def rotate_joint(joint_num, angle_deg):
    # Function implementation details...
```

When a joint rotates:
1. The joint itself rotates around its axis
2. All dependent links and joints move and rotate accordingly
3. The entire kinematic chain maintains proper structural relationships

### Key Components Creation

```python
# Create the base cylinder
base = doc.addObject("Part::Cylinder", "Base")
base.Radius = base_radius
base.Height = base_height

# Create links and joints
# ... additional code ...
```

## Applications

This robotic arm simulation can be used for:

- **Educational Purposes**: Teaching robotics and kinematics concepts
- **Design Prototyping**: Testing arm designs before physical manufacturing
- **Motion Planning**: Developing and validating movement sequences
- **Research**: Experimenting with different arm configurations
- **Integration Testing**: Basis for more complex robotic systems

## Extending the Project

Consider these enhancements:

- **Inverse Kinematics**: Calculate joint angles for desired end-effector positions
- **Path Planning**: Create functions for complex movement sequences
- **Collision Detection**: Add obstacle avoidance capabilities
- **GUI Controls**: Build an interactive interface for the simulation
- **Additional Joints**: Expand the model with more degrees of freedom
- **End Effector Tools**: Add grippers or specialized tools to the arm

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- FreeCAD development team for the excellent CAD platform
- Contributors to the FreeCAD Python API documentation
