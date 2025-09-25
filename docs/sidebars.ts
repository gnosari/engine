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
    'what-is-gnosari',
    'quickstart',
    'teams',
    'agents',
    {
      type: 'category',
      label: 'Coordination',
      items: [
        'coordination/orchestration',
        'coordination/handoffs',
        'coordination/delegation',
      ],
    },
    {
      type: 'category',
      label: 'Tools',
      items: [
        'tools/intro',
        'tools/delegate-agent',
        'tools/api-request',
        'tools/file-operations',
        'tools/knowledge-query',
        'tools/mysql-query',
        'tools/sql-query',
        'tools/web-search',
        'tools/website-content',
        'tools/bash-operations',
        'tools/interactive-bash-operations',
      ],
    },
    'mcp-servers',
    {
      type: 'category',
      label: 'Knowledge Bases',
      items: [
        'knowledge-bases/intro',
        'knowledge-bases/embedchain-configuration',
      ],
    },
    {
      type: 'category',
      label: 'Registry',
      items: [
        'registry/intro',
        'registry/authentication',
        'registry/push-commands',
        'registry/pull-commands',
      ],
    },
    {
      type: 'category',
      label: 'Async Execution',
      items: [
        'queues/intro',
        'queues/async-configuration',
        'queues/cli-commands',
        'queues/worker-management',
      ],
    },
    'prompts',
    'sessions',
  ],
};

export default sidebars;
