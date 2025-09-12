import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { query } = body;

    if (!query || typeof query !== 'string') {
      return NextResponse.json(
        { error: 'Query is required and must be a string' },
        { status: 400 }
      );
    }

    // Simple AI agent logic
    const agents_used = [];
    let result = {};

    // Check if it's a news-related query
    if (query.toLowerCase().includes('news') || query.toLowerCase().includes('latest')) {
      agents_used.push('news_agent');
      
      // Mock news response (you can integrate real NewsAPI later)
      result = {
        type: 'news_summary',
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
        type: 'research_results',
        data: {
          summary: `Research completed for: "${query}". Here's what I found:`,
          documents: [
          {
            title: `AI Research: ${query}`,
            content: `Artificial Intelligence (AI) is a rapidly evolving field that encompasses machine learning, deep learning, natural language processing, computer vision, and robotics. Based on your query about "${query}", here's what we found:

AI systems are designed to perform tasks that typically require human intelligence, such as visual perception, speech recognition, decision-making, and language translation. The field has seen tremendous growth in recent years, with applications spanning from healthcare and finance to transportation and entertainment.

Key areas of AI include:
- Machine Learning: Algorithms that improve through experience
- Deep Learning: Neural networks with multiple layers
- Natural Language Processing: Understanding and generating human language
- Computer Vision: Interpreting visual information
- Robotics: Creating intelligent machines that can interact with the physical world

The future of AI holds promise for solving complex global challenges while also raising important questions about ethics, privacy, and the future of work.`,
            source: 'AI Knowledge Base',
            similarity_score: 0.95
          },
          {
            title: 'Current AI Trends and Developments',
            content: `Recent developments in AI include advances in large language models, improved computer vision systems, and breakthroughs in reinforcement learning. These technologies are being applied across various industries to improve efficiency, accuracy, and innovation.

Notable trends include:
- Generative AI and large language models
- AI-powered automation in business processes
- Enhanced natural language understanding
- Improved AI ethics and responsible AI practices
- Integration of AI with IoT and edge computing`,
            source: 'Technology Research Database',
            similarity_score: 0.88
          }
        ]
        },
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
