import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import styles from './styles.module.css';

export default function ModuleCard({title, description, to}: {title: string, description: string, to: string}) {
  return (
    <div className={clsx('module-card depth-layer-2', styles.moduleCard)}>
      <h3>{title}</h3>
      <p>{description}</p>
      <Link to={to} className="button button--secondary button--sm">
        Start Learning
      </Link>
    </div>
  );
}