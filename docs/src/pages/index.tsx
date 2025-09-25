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
        <div className={styles.heroContent}>
          <Heading as="h1" className={clsx("hero__title", styles.heroTitle)}>
            {siteConfig.title}
          </Heading>
          <p className={clsx("hero__subtitle", styles.heroSubtitle)}>
            {siteConfig.tagline}
          </p>
          <div className={styles.buttons}>
            <Link
              className={clsx("button button--primary button--lg", styles.getStartedButton)}
              to="/quickstart">
              🚀 Get Started
            </Link>
          </div>
          <div className={styles.codeExample}>
            <code>gnosari --config "examples/team.yaml" --message "Your message"</code>
          </div>
        </div>
      </div>
    </header>
  );
}

function TeamsSection() {
  return (
    <section className={styles.teamsSection}>
      <div className="container">
        <div className="row">
          <div className="col col--6">
            <div className={styles.sectionContent}>
              <div>
                <div className={styles.sectionIcon}>👥</div>
                <Heading as="h2" className={styles.sectionTitle}>Teams</Heading>
                <p className={styles.sectionDescription}>
                  Build sophisticated AI teams with YAML configuration. Define agent roles, 
                  coordination patterns, and workflows with simple declarative syntax.
                </p>
                <div className={styles.featureGrid}>
                  <div className={styles.featureItem}>
                    <span className={styles.featureIcon}>📋</span>
                    <span>YAML Configuration</span>
                  </div>
                  <div className={styles.featureItem}>
                    <span className={styles.featureIcon}>🔄</span>
                    <span>Multi-Agent Coordination</span>
                  </div>
                  <div className={styles.featureItem}>
                    <span className={styles.featureIcon}>⚙️</span>
                    <span>Flexible Workflows</span>
                  </div>
                </div>
              </div>
              <Link
                className={clsx("button button--primary", styles.sectionButton)}
                to="/teams">
                Learn About Teams
              </Link>
            </div>
          </div>
          <div className="col col--6">
            <div className={styles.codeBlock}>
              <div className={styles.codeBlockHeader}>team.yaml</div>
              <pre className={styles.codeBlockContent}>
                <code>{`name: Research Team
agents:
  - name: Coordinator
    orchestrator: true
    instructions: >
      Manage research tasks and delegate
      to specialized agents.
    model: gpt-4o
    
  - name: Researcher  
    instructions: >
      Conduct thorough research and
      gather information.
    model: gpt-4o-mini
    tools: [web_search, knowledge_query]`}</code>
              </pre>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function AgentsSection() {
  return (
    <section className={styles.agentsSection}>
      <div className="container">
        <div className="row">
          <div className="col col--6">
            <div className={styles.codeBlock}>
              <div className={styles.codeBlockHeader}>agent-config.yaml</div>
              <pre className={styles.codeBlockContent}>
                <code>{`agents:
  - name: Writing Specialist
    instructions: >
      You are a professional writer who creates
      clear, engaging content with proper structure.
    model: claude-3-5-sonnet
    temperature: 0.7
    tools: 
      - file_operations
      - knowledge_query
    knowledge:
      - style_guide
      - company_docs`}</code>
              </pre>
            </div>
          </div>
          <div className="col col--6">
            <div className={styles.sectionContent}>
              <div>
                <div className={styles.sectionIcon}>🤖</div>
                <Heading as="h2" className={styles.sectionTitle}>Agents</Heading>
                <p className={styles.sectionDescription}>
                  Configure intelligent agents with specific roles, instructions, and capabilities. 
                  Each agent can use different models, tools, and knowledge bases.
                </p>
                <div className={styles.featureGrid}>
                  <div className={styles.featureItem}>
                    <span className={styles.featureIcon}>🧠</span>
                    <span>Multi-Model Support</span>
                  </div>
                  <div className={styles.featureItem}>
                    <span className={styles.featureIcon}>🎯</span>
                    <span>Specialized Instructions</span>
                  </div>
                  <div className={styles.featureItem}>
                    <span className={styles.featureIcon}>🔧</span>
                    <span>Custom Tool Access</span>
                  </div>
                </div>
              </div>
              <Link
                className={clsx("button button--primary", styles.sectionButton)}
                to="/agents">
                Configure Agents
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}


function OrchestrationSection() {
  return (
    <section className={styles.orchestrationSection}>
      <div className="container">
        <div className="text--center">
          <div className={styles.sectionIcon}>🎭</div>
          <Heading as="h2" className={styles.sectionTitle}>Orchestration & Coordination</Heading>
          <p className={styles.sectionDescription}>
            Enable seamless collaboration between agents through handoffs, delegation, and real-time coordination patterns.
          </p>
        </div>
        <div className="row">
          <div className="col col--4">
            <div className={styles.coordCard}>
              <div className={styles.coordIcon}>🔄</div>
              <Heading as="h3">Handoffs</Heading>
              <p>Transfer conversation control between agents for specialized handling of different tasks.</p>
              <Link to="/coordination/handoffs" className={styles.coordLink}>Learn More →</Link>
            </div>
          </div>
          <div className="col col--4">
            <div className={styles.coordCard}>
              <div className={styles.coordIcon}>📤</div>
              <Heading as="h3">Delegation</Heading>
              <p>Send tasks to other agents and receive results without losing conversation context.</p>
              <Link to="/coordination/delegation" className={styles.coordLink}>Learn More →</Link>
            </div>
          </div>
          <div className="col col--4">
            <div className={styles.coordCard}>
              <div className={styles.coordIcon}>🎯</div>
              <Heading as="h3">Orchestration</Heading>
              <p>Coordinate complex workflows with intelligent routing and task management.</p>
              <Link to="/coordination/orchestration" className={styles.coordLink}>Learn More →</Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function ToolsSection() {
  return (
    <section className={styles.toolsSection}>
      <div className="container">
        <div className="text--center">
          <div className={styles.sectionIcon}>🛠️</div>
          <Heading as="h2" className={styles.sectionTitle}>Powerful Tools Ecosystem</Heading>
          <p className={styles.sectionDescription}>
            Agents can access a rich ecosystem of built-in tools and dynamically discover new capabilities through MCP servers.
          </p>
        </div>
        <div className="row">
          <div className="col col--6">
            <div className={styles.toolCategory}>
              <Heading as="h3">🔧 Built-in Tools</Heading>
              <div className={styles.toolGrid}>
                <div className={styles.toolItem}>
                  <span className={styles.toolIcon}>🌐</span>
                  <div>
                    <strong>Web Search</strong>
                    <p>Search the web for real-time information</p>
                  </div>
                </div>
                <div className={styles.toolItem}>
                  <span className={styles.toolIcon}>📁</span>
                  <div>
                    <strong>File Operations</strong>
                    <p>Read, write, and manage files securely</p>
                  </div>
                </div>
                <div className={styles.toolItem}>
                  <span className={styles.toolIcon}>🗄️</span>
                  <div>
                    <strong>Database Access</strong>
                    <p>Query MySQL and other databases</p>
                  </div>
                </div>
                <div className={styles.toolItem}>
                  <span className={styles.toolIcon}>🔗</span>
                  <div>
                    <strong>API Requests</strong>
                    <p>Make HTTP requests to external services</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="col col--6">
            <div className={styles.toolCategory}>
              <Heading as="h3">⚡ MCP Integration</Heading>
              <div className={styles.mcpFeatures}>
                <div className={styles.mcpFeature}>
                  <span className={styles.mcpIcon}>🔍</span>
                  <div>
                    <strong>Dynamic Discovery</strong>
                    <p>Agents automatically discover new tools from MCP servers</p>
                  </div>
                </div>
                <div className={styles.mcpFeature}>
                  <span className={styles.mcpIcon}>🔧</span>
                  <div>
                    <strong>Extensible</strong>
                    <p>Add custom tools and integrate third-party services</p>
                  </div>
                </div>
                <div className={styles.mcpFeature}>
                  <span className={styles.mcpIcon}>📡</span>
                  <div>
                    <strong>Protocol Standard</strong>
                    <p>Based on Model Context Protocol for interoperability</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="text--center" style={{marginTop: '2rem'}}>
          <Link
            className={clsx("button button--primary button--lg", styles.sectionButton)}
            to="/tools/intro">
            Explore All Tools
          </Link>
        </div>
      </div>
    </section>
  );
}

function KnowledgeSection() {
  return (
    <section className={styles.knowledgeSection}>
      <div className="container">
        <div className="row">
          <div className="col col--6">
            <div className={styles.sectionContent}>
              <div>
                <div className={styles.sectionIcon}>📚</div>
                <Heading as="h2" className={styles.sectionTitle}>Knowledge Bases</Heading>
                <p className={styles.sectionDescription}>
                  Integrate RAG capabilities with Embedchain to give agents access to your documents, 
                  websites, and knowledge repositories.
                </p>
                <div className={styles.knowledgeTypes}>
                  <div className={styles.knowledgeType}>
                    <span className={styles.knowledgeIcon}>🌐</span>
                    <span>Websites & Sitemaps</span>
                  </div>
                  <div className={styles.knowledgeType}>
                    <span className={styles.knowledgeIcon}>📄</span>
                    <span>Documents & PDFs</span>
                  </div>
                  <div className={styles.knowledgeType}>
                    <span className={styles.knowledgeIcon}>🎥</span>
                    <span>Videos & Transcripts</span>
                  </div>
                  <div className={styles.knowledgeType}>
                    <span className={styles.knowledgeIcon}>💾</span>
                    <span>Custom Data Sources</span>
                  </div>
                </div>
              </div>
              <Link
                className={clsx("button button--primary", styles.sectionButton)}
                to="/knowledge-bases/intro">
                Setup Knowledge Bases
              </Link>
            </div>
          </div>
          <div className="col col--6">
            <div className={styles.codeBlock}>
              <div className={styles.codeBlockHeader}>knowledge.yaml</div>
              <pre className={styles.codeBlockContent}>
                <code>{`knowledge:
  - id: company_docs
    name: Company Documentation
    type: sitemap
    config:
      embedder:
        provider: openai
        model: text-embedding-3-small
    data:
      - https://docs.company.com/sitemap.xml
      - ./documents/policies.pdf
      
agents:
  - name: Support Agent
    knowledge: [company_docs]
    tools: [knowledge_query]`}</code>
              </pre>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function GetStartedSection() {
  return (
    <section className={styles.getStartedSection}>
      <div className="container">
        <div className="text--center">
          <Heading as="h2" className={styles.sectionTitle}>Ready to Build Your AI Workforce?</Heading>
          <p className={styles.sectionDescription}>
            Get started with Gnosari in minutes and create your first intelligent agent team.
          </p>
          <div className={styles.ctaButtons}>
            <Link
              className={clsx("button button--primary button--lg", styles.primaryCta)}
              to="/quickstart">
              🚀 Quick Start Guide
            </Link>
            <Link
              className={clsx("button button--secondary button--lg", styles.secondaryCta)}
              to="/what-is-gnosari">
              📖 Learn More
            </Link>
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
        <TeamsSection />
        <AgentsSection />
        <OrchestrationSection />
        <ToolsSection />
        <KnowledgeSection />
        <GetStartedSection />
      </main>
    </Layout>
  );
}
