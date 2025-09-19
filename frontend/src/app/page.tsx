"use client";

import { useState } from 'react';
import QueryInput from '../components/QueryInput';
import ResultsDisplay from '../components/ResultsDisplay';
import AgentStatus from '../components/AgentStatus';
import Header from '../components/Header';
import LetterGlitch from '../components/LetterGlitch';
import { apiClient } from '../lib/api';

export default function Home() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [cacheCleared, setCacheCleared] = useState(false);

  const handleQuery = async (queryText: string) => {
    setLoading(true);
    setError('');

    try {
      const response = await apiClient.query(queryText);
      
      if (response.error) {
        throw new Error(response.error);
      }

      setResults(response.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('Query error:', err);
    } finally {
      setLoading(false);
    }
  };

  const clearCache = async () => {
    try {
      const response = await apiClient.request('/cache/clear', {
        method: 'POST',
      });

      if (!response.error) {
        setCacheCleared(true);
        setTimeout(() => setCacheCleared(false), 3000); // Hide message after 3 seconds
      }
    } catch (err) {
      console.error('Cache clear error:', err);
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
          <div className="max-w-5xl mx-auto space-y-8">
            {/* Hero Section */}
            <div className="text-center mb-16">
              <div className="bg-black/70 backdrop-blur-lg rounded-2xl p-8 border border-cyan-500/30 shadow-2xl">
                <h1 className="text-5xl font-bold text-white mb-6 drop-shadow-2xl tracking-wide bg-gradient-to-r from-white to-cyan-200 bg-clip-text text-transparent">
                  Multi-Agent AI System
                </h1>
                <p className="text-xl text-white mb-8 drop-shadow-lg max-w-2xl mx-auto leading-relaxed font-medium">
                  Ask questions and get intelligent responses from our specialized AI agents. The system learns from every technology-related query!
                </p>
              </div>
            </div>

            {/* Query Input */}
            <div className="bg-black/80 backdrop-blur-md rounded-xl shadow-2xl border border-cyan-500/20 p-8">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-cyan-300">Ask a Question</h2>
                <button
                  onClick={clearCache}
                  className="px-6 py-3 bg-cyan-600 text-white rounded-lg hover:bg-cyan-700 transition-all duration-300 text-sm font-medium shadow-lg hover:shadow-cyan-500/25"
                >
                  Clear Cache
                </button>
              </div>
              {cacheCleared && (
                <div className="mb-6 p-4 bg-green-900/50 border border-green-500/30 rounded-lg backdrop-blur-sm">
                  <p className="text-green-300 text-sm font-medium">✅ Cache cleared successfully!</p>
                </div>
              )}
              <QueryInput 
                onQuery={handleQuery} 
                loading={loading}
                placeholder="Ask about any technology topic - AI, programming, blockchain, gaming, startups, etc. The system learns from every query!"
              />
            </div>

            {/* Error Display */}
            {error && (
              <div className="bg-red-900/50 backdrop-blur-md border border-red-500/30 rounded-xl p-6 shadow-2xl">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg className="h-6 w-6 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-4">
                    <h3 className="text-lg font-semibold text-red-300">Error</h3>
                    <div className="mt-2 text-red-200">
                      <p>{error}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Results Display */}
            {results && (
              <div className="bg-black/80 backdrop-blur-md rounded-xl shadow-2xl border border-cyan-500/20 p-8">
                <ResultsDisplay results={results} />
              </div>
            )}

            {/* Agent Status */}
            <div className="bg-black/80 backdrop-blur-md rounded-xl shadow-2xl border border-cyan-500/20 p-8">
              <AgentStatus />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}