"use client";

import { useState } from 'react';
import Header from '@/components/Header';
import LetterGlitch from '@/components/LetterGlitch';

export default function Agents() {
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);

  const agents = [
    {
      id: 'news_agent',
      name: 'News Agent',
      description: 'Fetches and analyzes the latest news articles from various sources',
      capabilities: ['Real-time news fetching', 'Article summarization', 'Source verification', 'Trend analysis'],
      status: 'active',
      usage: '15%',
      lastUsed: '2 minutes ago',
      performance: { accuracy: '94%', speed: '0.3s', reliability: '99.2%' }
    },
    {
      id: 'research_agent',
      name: 'Research Agent',
      description: 'Provides comprehensive research and knowledge retrieval using advanced search',
      capabilities: ['Deep web search', 'Academic papers', 'Technical documentation', 'Fact verification'],
      status: 'active',
      usage: '35%',
      lastUsed: '1 minute ago',
      performance: { accuracy: '96%', speed: '0.8s', reliability: '98.8%' }
    },
    {
      id: 'sentiment_agent',
      name: 'Sentiment Agent',
      description: 'Analyzes text sentiment and emotional tone with high accuracy',
      capabilities: ['Emotion detection', 'Sentiment scoring', 'Context analysis', 'Multi-language support'],
      status: 'active',
      usage: '10%',
      lastUsed: '5 minutes ago',
      performance: { accuracy: '92%', speed: '0.2s', reliability: '99.5%' }
    },
    {
      id: 'summarizer_agent',
      name: 'Summarizer Agent',
      description: 'Creates intelligent summaries of complex content and documents',
      capabilities: ['Content summarization', 'Key point extraction', 'Multi-format support', 'Length optimization'],
      status: 'active',
      usage: '20%',
      lastUsed: '3 minutes ago',
      performance: { accuracy: '93%', speed: '0.5s', reliability: '99.1%' }
    },
    {
      id: 'decision_agent',
      name: 'Decision Agent',
      description: 'Makes strategic decisions based on data analysis and reasoning',
      capabilities: ['Strategic planning', 'Risk assessment', 'Option evaluation', 'Decision trees'],
      status: 'active',
      usage: '5%',
      lastUsed: '10 minutes ago',
      performance: { accuracy: '89%', speed: '1.2s', reliability: '97.8%' }
    },
    {
      id: 'frontend_agent',
      name: 'Frontend Agent',
      description: 'Optimizes user interface and user experience dynamically',
      capabilities: ['UI optimization', 'Layout adaptation', 'Performance tuning', 'Accessibility enhancement'],
      status: 'active',
      usage: '8%',
      lastUsed: '1 minute ago',
      performance: { accuracy: '95%', speed: '0.1s', reliability: '99.9%' }
    },
    {
      id: 'documentation_agent',
      name: 'Documentation Agent',
      description: 'Generates and maintains comprehensive documentation',
      capabilities: ['Auto-documentation', 'Code comments', 'API docs', 'User guides'],
      status: 'active',
      usage: '3%',
      lastUsed: '15 minutes ago',
      performance: { accuracy: '91%', speed: '0.7s', reliability: '98.5%' }
    },
    {
      id: 'caching_agent',
      name: 'Caching Agent',
      description: 'Manages intelligent caching for optimal performance',
      capabilities: ['Smart caching', 'Cache invalidation', 'Performance optimization', 'Memory management'],
      status: 'active',
      usage: '2%',
      lastUsed: '30 seconds ago',
      performance: { accuracy: '98%', speed: '0.05s', reliability: '99.8%' }
    },
    {
      id: 'learning_agent',
      name: 'Learning Agent',
      description: 'Continuously learns and improves from user interactions',
      capabilities: ['Pattern recognition', 'Behavior analysis', 'Model updates', 'Adaptive learning'],
      status: 'active',
      usage: '2%',
      lastUsed: '45 seconds ago',
      performance: { accuracy: '87%', speed: '2.1s', reliability: '96.2%' }
    }
  ];

  const selectedAgentData = agents.find(agent => agent.id === selectedAgent);

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
                  AI Agents
                </h1>
                <p className="text-lg text-white drop-shadow-lg font-medium">
                  Specialized AI agents working together to provide intelligent responses
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Agents List */}
              <div className="lg:col-span-2">
                <div className="bg-black/80 backdrop-blur-md rounded-xl p-6 border border-cyan-500/20 shadow-2xl">
                  <h3 className="text-xl font-bold text-white mb-6">Available Agents</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {agents.map((agent) => (
                      <div
                        key={agent.id}
                        onClick={() => setSelectedAgent(agent.id)}
                        className={`p-4 rounded-lg border cursor-pointer transition-all duration-300 ${
                          selectedAgent === agent.id
                            ? 'bg-cyan-600/20 border-cyan-500/50 shadow-lg shadow-cyan-500/25'
                            : 'bg-black/50 border-cyan-500/20 hover:border-cyan-500/40 hover:bg-black/60'
                        }`}
                      >
                        <div className="flex items-center justify-between mb-3">
                          <div className="flex items-center space-x-3">
                            <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                            <h4 className="text-white font-semibold">{agent.name}</h4>
                          </div>
                          <span className="text-cyan-300 text-sm font-medium">{agent.usage}</span>
                        </div>
                        <p className="text-cyan-200 text-sm mb-2">{agent.description}</p>
                        <div className="flex items-center justify-between text-xs text-cyan-300/70">
                          <span>Last used: {agent.lastUsed}</span>
                          <span className="px-2 py-1 bg-green-600/20 text-green-300 rounded-full">
                            {agent.status}
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Agent Details */}
              <div className="lg:col-span-1">
                <div className="bg-black/80 backdrop-blur-md rounded-xl p-6 border border-cyan-500/20 shadow-2xl">
                  {selectedAgentData ? (
                    <>
                      <h3 className="text-xl font-bold text-white mb-6">Agent Details</h3>
                      
                      <div className="space-y-6">
                        <div>
                          <h4 className="text-lg font-semibold text-cyan-300 mb-2">{selectedAgentData.name}</h4>
                          <p className="text-white text-sm">{selectedAgentData.description}</p>
                        </div>

                        <div>
                          <h5 className="text-cyan-300 font-medium mb-3">Capabilities</h5>
                          <div className="space-y-2">
                            {selectedAgentData.capabilities.map((capability, index) => (
                              <div key={index} className="flex items-center space-x-2">
                                <div className="w-2 h-2 bg-cyan-400 rounded-full"></div>
                                <span className="text-white text-sm">{capability}</span>
                              </div>
                            ))}
                          </div>
                        </div>

                        <div>
                          <h5 className="text-cyan-300 font-medium mb-3">Performance Metrics</h5>
                          <div className="space-y-3">
                            <div className="flex justify-between items-center">
                              <span className="text-white text-sm">Accuracy</span>
                              <span className="text-cyan-300 font-medium">{selectedAgentData.performance.accuracy}</span>
                            </div>
                            <div className="flex justify-between items-center">
                              <span className="text-white text-sm">Speed</span>
                              <span className="text-cyan-300 font-medium">{selectedAgentData.performance.speed}</span>
                            </div>
                            <div className="flex justify-between items-center">
                              <span className="text-white text-sm">Reliability</span>
                              <span className="text-cyan-300 font-medium">{selectedAgentData.performance.reliability}</span>
                            </div>
                          </div>
                        </div>

                        <div className="pt-4 border-t border-cyan-500/20">
                          <div className="flex justify-between items-center mb-2">
                            <span className="text-white text-sm">Usage</span>
                            <span className="text-cyan-300 font-medium">{selectedAgentData.usage}</span>
                          </div>
                          <div className="flex justify-between items-center">
                            <span className="text-white text-sm">Last Used</span>
                            <span className="text-cyan-300 font-medium">{selectedAgentData.lastUsed}</span>
                          </div>
                        </div>
                      </div>
                    </>
                  ) : (
                    <div className="text-center py-12">
                      <div className="text-cyan-300/50 text-6xl mb-4">🤖</div>
                      <h3 className="text-xl font-bold text-white mb-2">Select an Agent</h3>
                      <p className="text-cyan-300/70">Click on any agent to view detailed information</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
