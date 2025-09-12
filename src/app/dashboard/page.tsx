"use client";

import { useState, useEffect } from 'react';
import Header from '@/components/Header';
import LetterGlitch from '@/components/LetterGlitch';

export default function Dashboard() {
  const [stats, setStats] = useState({
    totalQueries: 0,
    activeAgents: 9,
    systemUptime: '99.9%',
    responseTime: '0.87s'
  });

  const [recentQueries, setRecentQueries] = useState([
    { id: 1, query: "tell me about AI", agent: "research_agent", timestamp: "2 minutes ago" },
    { id: 2, query: "latest AI news", agent: "news_agent", timestamp: "5 minutes ago" },
    { id: 3, query: "sentiment of AI", agent: "sentiment_agent", timestamp: "8 minutes ago" },
    { id: 4, query: "machine learning", agent: "research_agent", timestamp: "12 minutes ago" },
    { id: 5, query: "AI ethics", agent: "research_agent", timestamp: "15 minutes ago" }
  ]);

  const agents = [
    { name: "News Agent", status: "active", description: "Fetches latest news and articles", usage: "15%" },
    { name: "Research Agent", status: "active", description: "Provides comprehensive research", usage: "35%" },
    { name: "Sentiment Agent", status: "active", description: "Analyzes text sentiment", usage: "10%" },
    { name: "Summarizer Agent", status: "active", description: "Creates intelligent summaries", usage: "20%" },
    { name: "Decision Agent", status: "active", description: "Makes strategic decisions", usage: "5%" },
    { name: "Frontend Agent", status: "active", description: "Handles UI optimization", usage: "8%" },
    { name: "Documentation Agent", status: "active", description: "Generates documentation", usage: "3%" },
    { name: "Caching Agent", status: "active", description: "Manages performance cache", usage: "2%" },
    { name: "Learning Agent", status: "active", description: "Improves from interactions", usage: "2%" }
  ];

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
                  System Dashboard
                </h1>
                <p className="text-lg text-white drop-shadow-lg font-medium">
                  Real-time monitoring and analytics for the Multi-Agent AI System
                </p>
              </div>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-black/80 backdrop-blur-md rounded-xl p-6 border border-cyan-500/20 shadow-2xl">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-cyan-300 text-sm font-medium">Total Queries</p>
                    <p className="text-3xl font-bold text-white">{stats.totalQueries}</p>
                  </div>
                  <div className="w-12 h-12 bg-cyan-600/20 rounded-xl flex items-center justify-center">
                    <svg className="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                    </svg>
                  </div>
                </div>
              </div>

              <div className="bg-black/80 backdrop-blur-md rounded-xl p-6 border border-cyan-500/20 shadow-2xl">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-cyan-300 text-sm font-medium">Active Agents</p>
                    <p className="text-3xl font-bold text-white">{stats.activeAgents}</p>
                  </div>
                  <div className="w-12 h-12 bg-green-600/20 rounded-xl flex items-center justify-center">
                    <svg className="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                </div>
              </div>

              <div className="bg-black/80 backdrop-blur-md rounded-xl p-6 border border-cyan-500/20 shadow-2xl">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-cyan-300 text-sm font-medium">System Uptime</p>
                    <p className="text-3xl font-bold text-white">{stats.systemUptime}</p>
                  </div>
                  <div className="w-12 h-12 bg-blue-600/20 rounded-xl flex items-center justify-center">
                    <svg className="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                </div>
              </div>

              <div className="bg-black/80 backdrop-blur-md rounded-xl p-6 border border-cyan-500/20 shadow-2xl">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-cyan-300 text-sm font-medium">Avg Response</p>
                    <p className="text-3xl font-bold text-white">{stats.responseTime}</p>
                  </div>
                  <div className="w-12 h-12 bg-purple-600/20 rounded-xl flex items-center justify-center">
                    <svg className="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>

            {/* Recent Queries and Agent Status */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Recent Queries */}
              <div className="bg-black/80 backdrop-blur-md rounded-xl p-6 border border-cyan-500/20 shadow-2xl">
                <h3 className="text-xl font-bold text-white mb-6">Recent Queries</h3>
                <div className="space-y-4">
                  {recentQueries.map((query) => (
                    <div key={query.id} className="flex items-center justify-between p-4 bg-black/50 rounded-lg border border-cyan-500/10">
                      <div className="flex-1">
                        <p className="text-white font-medium">{query.query}</p>
                        <p className="text-cyan-300 text-sm">{query.agent}</p>
                      </div>
                      <div className="text-cyan-300/70 text-sm">{query.timestamp}</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Agent Status */}
              <div className="bg-black/80 backdrop-blur-md rounded-xl p-6 border border-cyan-500/20 shadow-2xl">
                <h3 className="text-xl font-bold text-white mb-6">Agent Performance</h3>
                <div className="space-y-4">
                  {agents.map((agent, index) => (
                    <div key={index} className="flex items-center justify-between p-4 bg-black/50 rounded-lg border border-cyan-500/10">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3">
                          <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                          <p className="text-white font-medium">{agent.name}</p>
                        </div>
                        <p className="text-cyan-300 text-sm mt-1">{agent.description}</p>
                      </div>
                      <div className="text-cyan-300 font-medium">{agent.usage}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
