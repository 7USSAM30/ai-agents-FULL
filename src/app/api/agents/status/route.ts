import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Mock agent status data
    const agents = [
      {
        name: 'News Agent',
        status: 'active',
        description: 'Fetches latest news and articles',
        last_used: '2 minutes ago',
        performance_metrics: {
          accuracy: '94%',
          speed: '0.3s',
          reliability: '99.2%'
        }
      },
      {
        name: 'Research Agent',
        status: 'active',
        description: 'Provides comprehensive research',
        last_used: '1 minute ago',
        performance_metrics: {
          accuracy: '96%',
          speed: '0.8s',
          reliability: '98.8%'
        }
      },
      {
        name: 'Sentiment Agent',
        status: 'active',
        description: 'Analyzes text sentiment',
        last_used: '5 minutes ago',
        performance_metrics: {
          accuracy: '92%',
          speed: '0.2s',
          reliability: '99.5%'
        }
      },
      {
        name: 'Summarizer Agent',
        status: 'active',
        description: 'Creates intelligent summaries',
        last_used: '3 minutes ago',
        performance_metrics: {
          accuracy: '93%',
          speed: '0.5s',
          reliability: '99.1%'
        }
      },
      {
        name: 'Decision Agent',
        status: 'active',
        description: 'Makes strategic decisions',
        last_used: '10 minutes ago',
        performance_metrics: {
          accuracy: '89%',
          speed: '1.2s',
          reliability: '97.8%'
        }
      },
      {
        name: 'Frontend Agent',
        status: 'active',
        description: 'Handles UI optimization',
        last_used: '1 minute ago',
        performance_metrics: {
          accuracy: '95%',
          speed: '0.1s',
          reliability: '99.9%'
        }
      },
      {
        name: 'Documentation Agent',
        status: 'active',
        description: 'Generates documentation',
        last_used: '15 minutes ago',
        performance_metrics: {
          accuracy: '91%',
          speed: '0.7s',
          reliability: '98.5%'
        }
      },
      {
        name: 'Caching Agent',
        status: 'active',
        description: 'Manages performance cache',
        last_used: '30 seconds ago',
        performance_metrics: {
          accuracy: '98%',
          speed: '0.05s',
          reliability: '99.8%'
        }
      },
      {
        name: 'Learning Agent',
        status: 'active',
        description: 'Improves from interactions',
        last_used: '45 seconds ago',
        performance_metrics: {
          accuracy: '87%',
          speed: '2.1s',
          reliability: '96.2%'
        }
      }
    ];

    return NextResponse.json({
      agents,
      system_status: 'operational',
      uptime: '99.9%',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Error fetching agent status:', error);
    return NextResponse.json(
      { error: 'Failed to fetch agent status' },
      { status: 500 }
    );
  }
}
