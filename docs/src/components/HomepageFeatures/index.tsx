import type {ReactNode} from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  icon: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Multi-Agent Orchestration',
    icon: '🤖',
    description: (
      <>
        Orchestrate intelligent AI agent teams that
        collaborate through streaming delegation and
        dynamic tool discovery. Each agent can use
        different LLM models and providers.
      </>
    ),
  },
  {
    title: 'Streaming & Real-time',
    icon: '⚡',
    description: (
      <>
        Experience real-time agent interactions with
        streaming responses and live delegation. Watch
        your AI teams work together in real-time with full
        transparency.
      </>
    ),
  },
  {
    title: 'Dynamic Tool Discovery',
    icon: '🔧',
    description: (
      <>
        Agents automatically discover and use tools
        through MCP (Model Context Protocol) servers.
        Built-in tools for delegation, API requests, and
        knowledge base queries.
      </>
    ),
  },
];

function Feature({title, icon, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <div className={styles.featureIcon}>{icon}</div>
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return null;
}
