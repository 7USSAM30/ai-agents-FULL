"use client";

import { useState } from 'react';
import Header from '../../components/Header';
import LetterGlitch from '../../components/LetterGlitch';

export default function Documentation() {
  const [activeSection, setActiveSection] = useState('overview');

  const sections = [
    { id: 'overview', title: 'Overview', icon: '📋' },
    { id: 'api', title: 'API Reference', icon: '🔌' },
    { id: 'agents', title: 'Agent Guide', icon: '🤖' },
    { id: 'examples', title: 'Examples', icon: '💡' },
    { id: 'troubleshooting', title: 'Troubleshooting', icon: '🔧' }
  ];

  const apiEndpoints = [
    {
      method: 'POST',
      path: '/api/query',
      description: 'Submit a query to the AI system',
      parameters: [
        { name: 'query', type: 'string', required: true, description: 'The question or request' },
        { name: 'user_id', type: 'string', required: false, description: 'User identifier for tracking' }
      ],
      response: {
        type: 'object',
        properties: {
          agents_used: ['string'],
          result: 'object',
          processing_time: 'number',
          timestamp: 'string'
        }
      }
    },
    {
      method: 'GET',
      path: '/api/agents/status',
      description: 'Get the status of all agents',
      parameters: [],
      response: {
        type: 'object',
        properties: {
          agents: 'array',
          system_status: 'string',
          uptime: 'string'
        }
      }
    },
    {
      method: 'POST',
      path: '/api/cache/clear',
      description: 'Clear the system cache',
      parameters: [],
      response: {
        type: 'object',
        properties: {
          success: 'boolean',
          message: 'string'
        }
      }
    }
  ];

  const examples = [
    {
      title: 'Basic Query',
      description: 'Ask a simple question',
      code: `curl -X POST http://localhost:3000/api/query \\
  -H "Content-Type: application/json" \\
  -d '{"query": "What is artificial intelligence?"}'`
    },
    {
      title: 'News Query',
      description: 'Get latest news articles',
      code: `curl -X POST http://localhost:3000/api/query \\
  -H "Content-Type: application/json" \\
  -d '{"query": "latest AI news"}'`
    },
    {
      title: 'Sentiment Analysis',
      description: 'Analyze text sentiment',
      code: `curl -X POST http://localhost:3000/api/query \\
  -H "Content-Type: application/json" \\
  -d '{"query": "What is the sentiment of AI?"}'`
    }
  ];

  const renderContent = () => {
    switch (activeSection) {
      case 'overview':
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-2xl font-bold text-white mb-4">System Overview</h3>
              <p className="text-cyan-200 leading-relaxed">
                The Multi-Agent AI System is a sophisticated platform that combines multiple specialized AI agents 
                to provide comprehensive responses to user queries. Each agent has unique capabilities and works 
                together to deliver intelligent, context-aware answers.
              </p>
            </div>

            <div>
              <h4 className="text-xl font-semibold text-cyan-300 mb-3">Key Features</h4>
              <ul className="space-y-2 text-cyan-200">
                <li className="flex items-start space-x-2">
                  <span className="text-cyan-400 mt-1">•</span>
                  <span>Real-time news aggregation and analysis</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="text-cyan-400 mt-1">•</span>
                  <span>Comprehensive research and knowledge retrieval</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="text-cyan-400 mt-1">•</span>
                  <span>Advanced sentiment analysis and emotion detection</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="text-cyan-400 mt-1">•</span>
                  <span>Intelligent content summarization</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="text-cyan-400 mt-1">•</span>
                  <span>Dynamic UI optimization and personalization</span>
                </li>
                <li className="flex items-start space-x-2">
                  <span className="text-cyan-400 mt-1">•</span>
                  <span>Performance caching and optimization</span>
                </li>
              </ul>
            </div>

            <div>
              <h4 className="text-xl font-semibold text-cyan-300 mb-3">Architecture</h4>
              <p className="text-cyan-200 leading-relaxed">
                The system uses a modular architecture where each agent specializes in specific tasks. 
                The orchestration layer intelligently routes queries to the most appropriate agents, 
                and results are combined to provide comprehensive responses.
              </p>
            </div>
          </div>
        );

      case 'api':
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-2xl font-bold text-white mb-4">API Reference</h3>
              <p className="text-cyan-200 mb-6">
                The Multi-Agent AI System provides a RESTful API for programmatic access to all agent capabilities.
              </p>
            </div>

            {apiEndpoints.map((endpoint, index) => (
              <div key={index} className="bg-black/50 rounded-lg p-6 border border-cyan-500/20">
                <div className="flex items-center space-x-3 mb-4">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    endpoint.method === 'POST' ? 'bg-green-600/20 text-green-300' : 'bg-blue-600/20 text-blue-300'
                  }`}>
                    {endpoint.method}
                  </span>
                  <code className="text-cyan-300 font-mono">{endpoint.path}</code>
                </div>
                
                <p className="text-white mb-4">{endpoint.description}</p>
                
                {endpoint.parameters.length > 0 && (
                  <div className="mb-4">
                    <h5 className="text-cyan-300 font-medium mb-2">Parameters</h5>
                    <div className="space-y-2">
                      {endpoint.parameters.map((param, paramIndex) => (
                        <div key={paramIndex} className="flex items-start space-x-3">
                          <code className="text-cyan-400 font-mono text-sm">{param.name}</code>
                          <span className="text-cyan-200 text-sm">({param.type})</span>
                          {param.required && <span className="text-red-400 text-sm">required</span>}
                          <span className="text-white text-sm">- {param.description}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div>
                  <h5 className="text-cyan-300 font-medium mb-2">Response</h5>
                  <pre className="bg-black/70 p-3 rounded text-cyan-200 text-sm overflow-x-auto">
{JSON.stringify(endpoint.response, null, 2)}
                  </pre>
                </div>
              </div>
            ))}
          </div>
        );

      case 'agents':
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-2xl font-bold text-white mb-4">Agent Guide</h3>
              <p className="text-cyan-200 mb-6">
                Each agent in the system has specific capabilities and use cases. Understanding how to interact 
                with each agent will help you get the most out of the system.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-black/50 rounded-lg p-6 border border-cyan-500/20">
                <h4 className="text-xl font-semibold text-cyan-300 mb-3">News Agent</h4>
                <p className="text-white mb-3">Fetches and analyzes latest news articles</p>
                <div className="space-y-2">
                  <span className="text-cyan-200 text-sm">Keywords: &quot;news&quot;, &quot;latest&quot;, &quot;breaking&quot;</span>
                  <span className="text-cyan-200 text-sm">Returns: 10 news articles with summaries</span>
                </div>
              </div>

              <div className="bg-black/50 rounded-lg p-6 border border-cyan-500/20">
                <h4 className="text-xl font-semibold text-cyan-300 mb-3">Research Agent</h4>
                <p className="text-white mb-3">Provides comprehensive research and knowledge</p>
                <div className="space-y-2">
                  <span className="text-cyan-200 text-sm">Keywords: &quot;tell me about&quot;, &quot;explain&quot;, &quot;research&quot;</span>
                  <span className="text-cyan-200 text-sm">Returns: 10+ detailed documents</span>
                </div>
              </div>

              <div className="bg-black/50 rounded-lg p-6 border border-cyan-500/20">
                <h4 className="text-xl font-semibold text-cyan-300 mb-3">Sentiment Agent</h4>
                <p className="text-white mb-3">Analyzes text sentiment and emotions</p>
                <div className="space-y-2">
                  <span className="text-cyan-200 text-sm">Keywords: &quot;sentiment&quot;, &quot;feeling&quot;, &quot;emotion&quot;</span>
                  <span className="text-cyan-200 text-sm">Returns: Sentiment score and confidence</span>
                </div>
              </div>

              <div className="bg-black/50 rounded-lg p-6 border border-cyan-500/20">
                <h4 className="text-xl font-semibold text-cyan-300 mb-3">Summarizer Agent</h4>
                <p className="text-white mb-3">Creates intelligent summaries</p>
                <div className="space-y-2">
                  <span className="text-cyan-200 text-sm">Keywords: &quot;summarize&quot;, &quot;brief&quot;, &quot;overview&quot;</span>
                  <span className="text-cyan-200 text-sm">Returns: Structured summaries</span>
                </div>
              </div>
            </div>
          </div>
        );

      case 'examples':
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-2xl font-bold text-white mb-4">Code Examples</h3>
              <p className="text-cyan-200 mb-6">
                Here are practical examples of how to interact with the Multi-Agent AI System.
              </p>
            </div>

            {examples.map((example, index) => (
              <div key={index} className="bg-black/50 rounded-lg p-6 border border-cyan-500/20">
                <h4 className="text-xl font-semibold text-cyan-300 mb-2">{example.title}</h4>
                <p className="text-white mb-4">{example.description}</p>
                <pre className="bg-black/70 p-4 rounded text-cyan-200 text-sm overflow-x-auto">
                  <code>{example.code}</code>
                </pre>
              </div>
            ))}
          </div>
        );

      case 'troubleshooting':
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-2xl font-bold text-white mb-4">Troubleshooting</h3>
              <p className="text-cyan-200 mb-6">
                Common issues and their solutions when working with the Multi-Agent AI System.
              </p>
            </div>

            <div className="space-y-4">
              <div className="bg-black/50 rounded-lg p-6 border border-cyan-500/20">
                <h4 className="text-lg font-semibold text-cyan-300 mb-2">Query Not Returning Results</h4>
                <p className="text-white mb-2">If your query isn&apos;t returning expected results:</p>
                <ul className="text-cyan-200 space-y-1">
                  <li>• Check if the query contains relevant keywords</li>
                  <li>• Try rephrasing your question</li>
                  <li>• Ensure the query is specific enough</li>
                  <li>• Check the agent status in the dashboard</li>
                </ul>
              </div>

              <div className="bg-black/50 rounded-lg p-6 border border-cyan-500/20">
                <h4 className="text-lg font-semibold text-cyan-300 mb-2">Slow Response Times</h4>
                <p className="text-white mb-2">If responses are slower than expected:</p>
                <ul className="text-cyan-200 space-y-1">
                  <li>• Check your internet connection</li>
                  <li>• Try clearing the cache</li>
                  <li>• Avoid overly complex queries</li>
                  <li>• Check system status in the dashboard</li>
                </ul>
              </div>

              <div className="bg-black/50 rounded-lg p-6 border border-cyan-500/20">
                <h4 className="text-lg font-semibold text-cyan-300 mb-2">Agent Not Responding</h4>
                <p className="text-white mb-2">If a specific agent isn&apos;t working:</p>
                <ul className="text-cyan-200 space-y-1">
                  <li>• Check agent status in the agents page</li>
                  <li>• Try a different query type</li>
                  <li>• Restart the application</li>
                  <li>• Check the system logs</li>
                </ul>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen relative">
      {/* Letter Glitch Background */}
      <div className="fixed inset-0 z-0">
        <LetterGlitch 
          glitchColors={['#2b4539', '#61dca3', '#61b3dc']}
          glitchSpeed={50}
          centerVignette={false}
          outerVignette={true}
          smooth={true}
          characters="ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$&*()-_+=/[]{};:<>.,0123456789"
        />
      </div>
      
      {/* Content Overlay */}
      <div className="relative z-10">
        <Header />
        
        <main className="container mx-auto px-6 py-12">
          <div className="max-w-7xl mx-auto space-y-8">
            {/* Page Header */}
            <div className="text-center mb-12">
              <div className="bg-black/70 backdrop-blur-lg rounded-2xl p-8 border border-cyan-500/30 shadow-2xl">
                <h1 className="text-4xl font-bold text-white mb-4 drop-shadow-2xl tracking-wide bg-gradient-to-r from-white to-cyan-200 bg-clip-text text-transparent">
                  Documentation
                </h1>
                <p className="text-lg text-white drop-shadow-lg font-medium">
                  Complete guide to using the Multi-Agent AI System
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
              {/* Sidebar Navigation */}
              <div className="lg:col-span-1">
                <div className="bg-black/80 backdrop-blur-md rounded-xl p-6 border border-cyan-500/20 shadow-2xl sticky top-8">
                  <h3 className="text-lg font-bold text-white mb-6">Contents</h3>
                  <nav className="space-y-2">
                    {sections.map((section) => (
                      <button
                        key={section.id}
                        onClick={() => setActiveSection(section.id)}
                        className={`w-full text-left px-4 py-3 rounded-lg transition-all duration-300 ${
                          activeSection === section.id
                            ? 'bg-cyan-600/20 text-cyan-300 border border-cyan-500/50'
                            : 'text-white hover:bg-black/50 hover:text-cyan-300'
                        }`}
                      >
                        <span className="mr-3">{section.icon}</span>
                        {section.title}
                      </button>
                    ))}
                  </nav>
                </div>
              </div>

              {/* Main Content */}
              <div className="lg:col-span-3">
                <div className="bg-black/80 backdrop-blur-md rounded-xl p-8 border border-cyan-500/20 shadow-2xl">
                  {renderContent()}
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
