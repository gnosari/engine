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
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--primary button--lg"
            to="/intro">
            Get Started - 5min ⏱️
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="/examples">
            View Examples
          </Link>
        </div>
        <div className={styles.codeExample}>
          <code>gnosari --config "examples/team.yaml" --message "Your message"</code>
        </div>
      </div>
    </header>
  );
}

function QuickStartSection() {
  return (
    <section className={styles.quickStart}>
      <div className="container">
        <div className="row">
          <div className="col col--8 col--offset-2">
            <div className="text--center">
              <Heading as="h2">Quick Start</Heading>
              <p className={styles.quickStartDescription}>
                Get up and running with Gnosari AI Teams in minutes. Create your first multi-agent team with just a few commands.
              </p>
            </div>
            <div className={styles.codeBlock}>
              <div className={styles.codeBlockHeader}>
                <span>Terminal</span>
              </div>
              <pre className={styles.codeBlockContent}>
                <code>{`# Install dependencies
poetry install

# Run your first team
gnosari --config "examples/team.yaml" --message "Hello team!" --stream

# Create custom team configuration
gnosari --config "my-team.yaml" --message "Your task"`}</code>
              </pre>
            </div>
            <div className="text--center">
              <Link
                className="button button--primary button--lg"
                to="/intro">
                Learn More in Documentation
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function KeyBenefits() {
  return (
    <section className={styles.keyBenefits}>
      <div className="container">
        <div className="row">
          <div className="col col--12">
            <div className="text--center">
              <Heading as="h2">Why Choose Gnosari AI Teams?</Heading>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col col--4">
            <div className={styles.benefitCard}>
              <div className={styles.benefitIcon}>🚀</div>
              <Heading as="h3">Production Ready</Heading>
              <p>Built for enterprise use with robust error handling, logging, and monitoring capabilities.</p>
            </div>
          </div>
          <div className="col col--4">
            <div className={styles.benefitCard}>
              <div className={styles.benefitIcon}>🔧</div>
              <Heading as="h3">Highly Configurable</Heading>
              <p>YAML-based team configuration with per-agent model settings, tools, and knowledge bases.</p>
            </div>
          </div>
          <div className="col col--4">
            <div className={styles.benefitCard}>
              <div className={styles.benefitIcon}>🌐</div>
              <Heading as="h3">Multi-Provider</Heading>
              <p>Support for OpenAI, Anthropic, DeepSeek, Google, and other LLM providers in a single team.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Orchestrate multi-agent teams using Large Language Models with streaming delegation and dynamic tool discovery">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
        <QuickStartSection />
        <KeyBenefits />
      </main>
    </Layout>
  );
}
