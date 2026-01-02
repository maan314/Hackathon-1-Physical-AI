import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type ModuleItem = {
  title: string;
  description: string;
  icon?: string; // Icon name or path
};

const ModuleList: ModuleItem[] = [
  {
    title: 'Module 1: The Robotic Nervous System (ROS 2)',
    description: 'Learn how ROS 2 enables real-time communication, coordination, and control across complex robotic systems',
  },
  {
    title: 'Module 2: The Digital Twin (Gazebo & Unity)',
    description: 'Build and simulate realistic robotic environments using digital twins for testing, training, and validation.',
  },
  {
    title: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
    description: 'Develop intelligent robot perception, decision-making, and autonomy using NVIDIA Isaac for AI-powered robotics.',
  },
  {
    title: 'Module 4: Vision-Language-Action (VLA)',
    description: 'Integrate vision, language, and action models to enable robots to understand, reason, and interact naturally with the world.',
  },
];

function Module({title, description, icon}: ModuleItem) {
  return (
    <div className={styles.moduleCard}>
      <div className={styles.moduleIcon}>
        {icon ? icon : (
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M2 17L12 22L22 17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M2 12L12 17L22 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        )}
      </div>
      <Heading as="h3" className={styles.moduleTitle}>{title}</Heading>
      <p className={styles.moduleDescription}>{description}</p>
    </div>
  );
}

export default function ModulesSection(): ReactNode {
  return (
    <section className={styles.modulesSection}>
      <div className={styles.modulesContainer}>
        <div className={styles.modulesGrid}>
          {ModuleList.map((props, idx) => (
            <Module key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}