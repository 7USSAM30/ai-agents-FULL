"use client";

import { useState, useEffect } from 'react';

interface Agent {
  name: string;
  status: string;
  description: string;
  last_used?: string;
  performance_metrics?: Record<string, unknown>;
}

export default function AgentStatus() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchAgentStatus();
  }, []);

  const fetchAgentStatus = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/agents/status`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json() as { agents: Record<string, { status: string; description: string; last_used?: string; performance_metrics?: Record<string, unknown> }> };
      // Convert object to array with name property
      const agentsArray = Object.entries(data.agents).map(([name, agentData]) => ({
        name,
        status: agentData.status,
        description: agentData.description,
        last_used: agentData.last_used,
        performance_metrics: agentData.performance_metrics
      }));
      setAgents(agentsArray);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch agent status');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-900/50 text-green-300 border border-green-500/30';
      case 'limited_mode':
        return 'bg-blue-900/50 text-blue-300 border border-blue-500/30';
      case 'inactive':
        return 'bg-gray-800/50 text-gray-300 border border-gray-500/30';
      case 'error':
        return 'bg-red-900/50 text-red-300 border border-red-500/30';
      case 'not_implemented':
        return 'bg-yellow-900/50 text-yellow-300 border border-yellow-500/30';
      case 'unknown':
        return 'bg-gray-800/50 text-gray-300 border border-gray-500/30';
      default:
        return 'bg-gray-800/50 text-gray-300 border border-gray-500/30';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return (
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
        );
      case 'limited_mode':
        return (
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
          </svg>
        );
      case 'error':
        return (
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
          </svg>
        );
      case 'unknown':
        return (
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
          </svg>
        );
      default:
        return (
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
          </svg>
        );
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-cyan-300">Agent Status</h2>
        <div className="flex items-center justify-center py-12">
          <svg className="animate-spin h-8 w-8 text-cyan-400" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <h2 className="text-2xl font-bold text-cyan-300">Agent Status</h2>
        <div className="bg-red-900/50 border border-red-500/30 rounded-xl p-6 backdrop-blur-sm">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-6 w-6 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-semibold text-red-300">Error loading agent status</h3>
              <div className="mt-2 text-red-200">
                <p>{error}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-cyan-300">Agent Status</h2>
        <button
          onClick={fetchAgentStatus}
          className="text-sm text-cyan-400 hover:text-cyan-300 transition-all duration-300 font-medium"
        >
          Refresh
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agents.map((agent, index) => (
          <div key={index} className="bg-black/50 border border-cyan-500/20 rounded-xl p-6 backdrop-blur-sm shadow-lg">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-cyan-200 capitalize text-lg">
                {agent.name?.replace('_', ' ') || 'Unknown Agent'}
              </h3>
              <span className={`inline-flex items-center px-3 py-1.5 rounded-lg text-xs font-medium ${getStatusColor(agent.status || 'unknown')}`}>
                {getStatusIcon(agent.status || 'unknown')}
                <span className="ml-2 capitalize">{(agent.status || 'unknown').replace('_', ' ')}</span>
              </span>
            </div>
            <p className="text-sm text-cyan-100/80 mb-4 leading-relaxed">{agent.description || 'No description available'}</p>
            {agent.last_used && (
              <div className="text-xs text-cyan-300/60 font-medium">
                Last used: {new Date(agent.last_used).toLocaleString()}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="text-sm text-cyan-300/70 text-center">
        <p>🧠 Learning Agent automatically learns from technology queries and builds knowledge over time</p>
        <p className="mt-2">All agents are active and ready to help with your technology questions!</p>
      </div>
    </div>
  );
}
