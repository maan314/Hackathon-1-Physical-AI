import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';
import BioRobotIcon from './BioRobotIcon';
import IncruiserIcon from './IncruiserIcon';
import MechabotIcon from './MechabotIcon';
import VisibotIcon from './VisibotIcon';

type FeatureItem = {
  title: string;
  Icon: React.ComponentType;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Bio-Robot',
    Icon: BioRobotIcon,
    description: (
      <>
        Biomimetic robotics with human-like movement and interaction capabilities
      </>
    ),
  },
  {
    title: 'Incruiser',
    Icon: IncruiserIcon,
    description: (
      <>
        Advanced navigation and exploration systems for autonomous movement
      </>
    ),
  },
  {
    title: 'Mechabot',
    Icon: MechabotIcon,
    description: (
      <>
        Heavy-duty mechanical systems for industrial applications
      </>
    ),
  },
  {
    title: 'Visibot',
    Icon: VisibotIcon,
    description: (
      <>
        Computer vision and perception systems for environmental awareness
      </>
    ),
  },
];

function Feature({title, Icon, description}: FeatureItem) {
  return (
    <div className={styles.featureCard}>
      <Icon className={styles.featureSvg} />
      <Heading as="h3">{title}</Heading>
      <p>{description}</p>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className={styles.featuresSection}>
        <div className={styles.featuresGrid}>
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
