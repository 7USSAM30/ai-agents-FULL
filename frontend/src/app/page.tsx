"use client";

import { useState } from 'react';
import QueryInput from '@/components/QueryInput';
import ResultsDisplay from '@/components/ResultsDisplay';
import AgentStatus from '@/components/AgentStatus';
import Header from '@/components/Header';

export default function Home() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [cacheCleared, setCacheCleared] = useState(false);

  const handleQuery = async (queryText: string) => {
    setLoading(true);
    setError('');

    try {
      // Add cache-busting parameter to ensure fresh results
      const timestamp = Date.now();
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/query?t=${timestamp}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Cache-Control': 'no-cache',
          'Pragma': 'no-cache'
        },
        body: JSON.stringify({
          query: queryText,
          user_id: 'demo_user'
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('Query error:', err);
    } finally {
      setLoading(false);
    }
  };

  const clearCache = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/cache/clear`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        setCacheCleared(true);
        setTimeout(() => setCacheCleared(false), 3000); // Hide message after 3 seconds
      }
    } catch (err) {
      console.error('Cache clear error:', err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Multi-Agent AI System
            </h1>
            <p className="text-xl text-gray-600 mb-8">
              Ask questions and get intelligent responses from our specialized AI agents
            </p>
          </div>

          {/* Query Input */}
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Ask a Question</h2>
              <button
                onClick={clearCache}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
              >
                Clear Cache
              </button>
            </div>
            {cacheCleared && (
              <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                <p className="text-green-800 text-sm">✅ Cache cleared successfully!</p>
              </div>
            )}
            <QueryInput 
              onQuery={handleQuery} 
              loading={loading}
              placeholder="Ask about AI news, research documents, or sentiment analysis..."
            />
          </div>

          {/* Error Display */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-8">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-red-800">Error</h3>
                  <div className="mt-2 text-sm text-red-700">
                    <p>{error}</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Results Display */}
          {results && (
            <div className="bg-white rounded-lg shadow-md p-6 mb-8">
              <ResultsDisplay results={results} />
            </div>
          )}

          {/* Agent Status */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <AgentStatus />
          </div>
        </div>
      </main>
    </div>
  );
}