import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module-1-the-robotic-nervous-system/chapter-1-embodied-control-and-middleware',
        'module-1-the-robotic-nervous-system/chapter-2-ros-2-nodes-topics-services-actions',
        'module-1-the-robotic-nervous-system/chapter-3-python-agents-ros-controllers',
        'module-1-the-robotic-nervous-system/chapter-4-urdf-for-humanoid-anatomy',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'module-2-the-digital-twin/chapter-1-physics-gravity-and-collision-modeling',
        'module-2-the-digital-twin/chapter-2-gazebo-simulation-pipelines',
        'module-2-the-digital-twin/chapter-3-sensor-simulation',
        'module-2-the-digital-twin/chapter-4-unity-for-human-robot-interaction',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'module-3-the-ai-robot-brain/chapter-1-isaac-sim-and-synthetic-data',
        'module-3-the-ai-robot-brain/chapter-2-isaac-ros-and-hardware-acceleration',
        'module-3-the-ai-robot-brain/chapter-3-vslam-and-nav2-for-humanoids',
        'module-3-the-ai-robot-brain/chapter-4-sim-to-real-transfer',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision–Language–Action (VLA)',
      items: [
        'module-4-vision-language-action/chapter-1-voice-to-action',
        'module-4-vision-language-action/chapter-2-cognitive-planning-with-llms',
        'module-4-vision-language-action/chapter-3-multimodal-perception',
        'module-4-vision-language-action/chapter-4-safety-constraints-and-action-validation',
      ],
    },
    {
      type: 'category',
      label: 'Module 5: Capstone — Autonomous Humanoid',
      items: [
        'module-5-capstone-autonomous-humanoid/chapter-1-system-architecture',
        'module-5-capstone-autonomous-humanoid/chapter-2-navigation-and-obstacle-avoidance',
        'module-5-capstone-autonomous-humanoid/chapter-3-object-recognition-and-manipulation',
        'module-5-capstone-autonomous-humanoid/chapter-4-full-autonomous-demo',
      ],
    },
  ],
};

export default sidebars;
