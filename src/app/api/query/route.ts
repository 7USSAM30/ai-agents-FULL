import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { query, user_id = 'anonymous', use_orchestrator = false } = body;

    if (!query || typeof query !== 'string') {
      return NextResponse.json(
        { error: 'Query is required and must be a string' },
        { status: 400 }
      );
    }

    // Simple AI agent logic
    let agents_used = [];
    let result = {};

    // Check if it's a news-related query
    if (query.toLowerCase().includes('news') || query.toLowerCase().includes('latest')) {
      agents_used.push('news_agent');
      
      // Mock news response (you can integrate real NewsAPI later)
      result = {
        type: 'news_response',
        data: `Here are the latest AI news updates based on your query: "${query}"`,
        articles: [
          {
            title: "AI Breakthrough in Natural Language Processing",
            summary: "Recent advances in transformer models show significant improvements in understanding context and nuance.",
            source: "TechNews",
            publishedAt: new Date().toISOString()
          },
          {
            title: "Machine Learning Applications in Healthcare",
            summary: "New AI systems are helping doctors diagnose diseases with 95% accuracy.",
            source: "HealthTech",
            publishedAt: new Date().toISOString()
          }
        ],
        formatted: {
          component_type: 'news_cards',
          formatted_data: {
            title: 'Latest AI News',
            articles: [
              {
                title: "AI Breakthrough in Natural Language Processing",
                summary: "Recent advances in transformer models show significant improvements in understanding context and nuance.",
                source: "TechNews",
                publishedAt: new Date().toISOString()
              },
              {
                title: "Machine Learning Applications in Healthcare", 
                summary: "New AI systems are helping doctors diagnose diseases with 95% accuracy.",
                source: "HealthTech",
                publishedAt: new Date().toISOString()
              }
            ]
          },
          ui_props: {
            theme: 'cyberpunk',
            animation: 'fadeIn'
          },
          metadata: {
            source: 'news_agent',
            confidence: 0.92
          }
        }
      };
    } 
    // Check if it's a sentiment analysis query
    else if (query.toLowerCase().includes('sentiment') || query.toLowerCase().includes('feeling') || query.toLowerCase().includes('emotion')) {
      agents_used.push('sentiment_agent');
      
      result = {
        type: 'sentiment_analysis',
        sentiment: 'positive',
        confidence: 0.85,
        data: `Sentiment analysis completed for: "${query}"`,
        formatted: {
          component_type: 'sentiment_display',
          formatted_data: {
            title: 'Sentiment Analysis Result',
            sentiment: 'positive',
            confidence: 0.85,
            explanation: 'The text shows positive sentiment with high confidence.'
          },
          ui_props: {
            theme: 'cyberpunk',
            animation: 'pulse'
          },
          metadata: {
            source: 'sentiment_agent',
            confidence: 0.85
          }
        }
      };
    }
    // Default research response
    else {
      agents_used.push('research_agent');
      
      result = {
        type: 'research_response',
        data: `Research completed for: "${query}". Here's what I found:`,
        summary: `Based on your query "${query}", I can provide comprehensive information about this topic. The research shows that this is an important area of study with many recent developments.`,
        formatted: {
          component_type: 'research_cards',
          formatted_data: {
            title: 'Research Results',
            summary: `Based on your query "${query}", I can provide comprehensive information about this topic. The research shows that this is an important area of study with many recent developments.`,
            sources: ['Knowledge Base', 'Research Database'],
            confidence: 0.88
          },
          ui_props: {
            theme: 'cyberpunk',
            animation: 'slideIn'
          },
          metadata: {
            source: 'research_agent',
            confidence: 0.88
          }
        }
      };
    }

    const response = {
      query,
      agents_used,
      processing_time: 0.5 + Math.random() * 0.5, // Simulate processing time
      timestamp: new Date().toISOString(),
      result,
      cached: false
    };

    return NextResponse.json(response);
  } catch (error) {
    console.error('Query processing error:', error);
    console.error('Error details:', {
      message: error instanceof Error ? error.message : 'Unknown error',
      stack: error instanceof Error ? error.stack : undefined,
      query: request.body
    });
    
    return NextResponse.json(
      { 
        error: 'Internal server error',
        details: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    message: 'Query endpoint is ready',
    status: 'operational',
    timestamp: new Date().toISOString()
  });
}
