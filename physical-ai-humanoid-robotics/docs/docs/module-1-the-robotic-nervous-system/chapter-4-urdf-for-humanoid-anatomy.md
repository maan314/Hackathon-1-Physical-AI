---
sidebar_position: 4
---

# URDF for Humanoid Anatomy

## Understanding URDF

URDF (Unified Robot Description Format) is an XML-based format used in ROS to describe robot models. For humanoid robots, URDF defines the physical and visual properties of each body part and their relationships.

## Humanoid Robot Structure

A humanoid robot typically consists of:

- **Trunk**: The central body structure
- **Head**: Contains sensors like cameras and IMUs
- **Arms**: With multiple degrees of freedom for manipulation
- **Legs**: For locomotion and balance
- **End effectors**: Hands for manipulation tasks

## URDF Components for Humanoids

Key components in a humanoid URDF:

- **Links**: Represent rigid parts of the robot
- **Joints**: Define connections between links with kinematic properties
- **Visual**: Define how links appear in simulation
- **Collision**: Define collision geometry for physics simulation
- **Inertial**: Define mass properties for dynamics simulation

## Kinematic Chains

Humanoid robots have multiple kinematic chains:

- **Right arm chain**: From torso to right hand
- **Left arm chain**: From torso to left hand
- **Right leg chain**: From torso to right foot
- **Left leg chain**: From torso to left foot
- **Head chain**: From torso to head

## Best Practices for Humanoid URDF

When designing humanoid URDFs:

- Use consistent naming conventions
- Ensure proper joint limits and safety constraints
- Include accurate inertial properties for stable simulation
- Define appropriate collision geometry to prevent self-collision
- Consider the actual hardware constraints of the physical robot

## Integration with ROS Controllers

URDF models integrate with ROS controllers through:

- **Transmission interfaces** that map joint commands to actuators
- **Joint limits** that prevent dangerous movements
- **Kinematic solvers** for inverse kinematics
- **Simulation plugins** for physics and sensor simulation