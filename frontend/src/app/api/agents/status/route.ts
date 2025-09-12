import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    agents: [
      {
        name: 'news_agent',
        status: 'active',
        description: 'Fetches and processes technology news'
      },
      {
        name: 'research_agent',
        status: 'active',
        description: 'Provides RAG-based knowledge retrieval'
      },
      {
        name: 'sentiment_agent',
        status: 'active',
        description: 'Analyzes text sentiment'
      },
      {
        name: 'summarizer_agent',
        status: 'active',
        description: 'Combines results from multiple agents'
      },
      {
        name: 'decision_agent',
        status: 'active',
        description: 'Intelligently routes queries'
      },
      {
        name: 'frontend_agent',
        status: 'active',
        description: 'Formats responses for UI display'
      },
      {
        name: 'documentation_agent',
        status: 'active',
        description: 'Auto-generates system documentation'
      },
      {
        name: 'caching_agent',
        status: 'active',
        description: 'Implements intelligent caching'
      },
      {
        name: 'learning_agent',
        status: 'active',
        description: 'Automatically learns from queries'
      }
    ],
    timestamp: new Date().toISOString(),
    total_agents: 9,
    active_agents: 9
  });
}
