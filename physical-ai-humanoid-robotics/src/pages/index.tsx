import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className={styles.heroSection}>
        {/* Text content on the left */}
        <div className={styles.heroText}>
          <Heading as="h1" className="hero__title">
            Physical AI & Humanoid Robotics
          </Heading>
          <p className="hero__subtitle">
            {siteConfig.tagline}
          </p>
          <div className={styles.buttons}>
            <Link
              className="button button--secondary button--lg"
              to="/docs/intro">
              Get Started
            </Link>
            <Link
              className="button button--primary button--lg"
              to="/docs/intro">
              Learn More
            </Link>
          </div>
        </div>

        {/* Floating module cards */}
        <div className={styles.moduleCards}>
          <div className={clsx(styles.moduleCard, styles.floatingElement)} style={{'--delay': '0.5'} as any}>
            <h3>Module 1: The Robotic Nervous System (ROS 2)</h3>
            <p>Learn how ROS 2 enables real-time communication, coordination, and control across complex robotic systems.</p>
          </div>
          <div className={clsx(styles.moduleCard, styles.floatingElement)} style={{'--delay': '1'} as any}>
            <h3>Module 2: The Digital Twin (Gazebo & Unity)</h3>
            <p>Build and simulate realistic robotic environments using digital twins for testing, training, and validation.</p>
          </div>
          <div className={clsx(styles.moduleCard, styles.floatingElement)} style={{'--delay': '1.5'} as any}>
            <h3>Module 3: The AI-Robot Brain (NVIDIA Isaac™)</h3>
            <p>Develop intelligent robot perception, decision-making, and autonomy using NVIDIA Isaac for AI-powered robotics.</p>
          </div>
          <div className={clsx(styles.moduleCard, styles.floatingElement)} style={{'--delay': '2'} as any}>
            <h3>Module 4: Vision-Language-Action (VLA)</h3>
            <p>Integrate vision, language, and action models to enable robots to understand, reason, and interact naturally with the world.</p>
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
