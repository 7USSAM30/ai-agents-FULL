"use client";

interface Article {
  headline: string;
  summary: string;
  source: string;
  published_at: string;
}

interface Source {
  title: string;
  similarity_score: number;
}

interface Document {
  title: string;
  content: string;
  source: string;
  similarity_score: number;
}

interface AgentContribution {
  status: string;
  contribution: string;
}

interface ResultData {
  type: string;
  data?: {
    articles?: Article[];
    documents?: Document[];
    sources?: Source[];
    summary?: string;
    sentiment?: string;
    confidence?: number;
    text?: string;
    error?: string;
    insights?: string[];
    recommendations?: string[];
    agent_contributions?: Record<string, AgentContribution>;
    [key: string]: unknown;
  };
  // Direct properties (for backward compatibility)
  articles?: Article[];
  documents?: Document[];
  sources?: Source[];
  summary?: string;
  sentiment?: string;
  confidence?: number;
  text?: string;
  error?: string;
  insights?: string[];
  recommendations?: string[];
  agent_contributions?: Record<string, AgentContribution>;
  [key: string]: unknown;
}

interface ResultsDisplayProps {
  results: {
    query: string;
    agents_used?: string[];
    processing_time?: number;
    timestamp?: string;
    result: ResultData;
  };
}

export default function ResultsDisplay({ results }: ResultsDisplayProps) {
  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  const renderResultContent = () => {
    if (!results.result) {
      return (
        <div className="text-gray-500 italic">
          No results to display
        </div>
      );
    }

    const result = results.result;
    const { type } = result;
    // Handle both nested data structure and direct structure
    const data = result.data || result;

    switch (type) {
      case 'sentiment_analysis':
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">Sentiment Analysis</h3>
            <div className="bg-black/50 border border-cyan-500/20 rounded-xl p-6 backdrop-blur-sm shadow-lg">
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium text-cyan-200">Sentiment:</span>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                  (data.sentiment || result.sentiment) === 'positive' ? 'bg-green-900/50 text-green-300 border border-green-500/30' :
                  (data.sentiment || result.sentiment) === 'negative' ? 'bg-red-900/50 text-red-300 border border-red-500/30' :
                  'bg-gray-800/50 text-gray-300 border border-gray-500/30'
                }`}>
                  {(data.sentiment || result.sentiment) ? (data.sentiment || result.sentiment).charAt(0).toUpperCase() + (data.sentiment || result.sentiment).slice(1) : 'Unknown'}
                </span>
              </div>
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium text-cyan-200">Confidence:</span>
                <span className="text-sm text-cyan-300">{Math.round(((data.confidence || result.confidence) || 0) * 100)}%</span>
              </div>
              {(data.text || (typeof result.data === 'string' ? result.data : null)) && (
                <div className="mt-3">
                  <span className="font-medium text-cyan-200">Analyzed Text:</span>
                  <p className="text-sm text-cyan-100/80 mt-1">{data.text || (typeof result.data === 'string' ? result.data : '')}</p>
                </div>
              )}
            </div>
          </div>
        );

      case 'news_summary':
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-bold text-cyan-300">📰 Latest AI News</h3>
              <span className="text-sm text-cyan-400 bg-cyan-900/30 px-3 py-1 rounded-full border border-cyan-500/30">
                {(data.articles || result.articles)?.length || 0} Articles
              </span>
            </div>
            {(data.articles || result.articles) && (data.articles || result.articles).length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {(data.articles || result.articles).map((article: { title?: string; headline?: string; summary: string; source: string; publishedAt?: string; published_at?: string }, index: number) => (
                  <div key={index} className="bg-black/60 border border-cyan-500/30 rounded-xl p-5 backdrop-blur-sm shadow-lg hover:shadow-cyan-500/20 transition-all duration-300 hover:border-cyan-400/50">
                    <div className="flex items-start justify-between mb-3">
                      <span className="text-xs text-cyan-400 bg-cyan-900/40 px-2 py-1 rounded-full border border-cyan-500/30">
                        #{index + 1}
                      </span>
                      <span className="text-xs text-cyan-300/70">
                        {formatTimestamp(article.publishedAt || article.published_at)}
                      </span>
                    </div>
                    <h4 className="font-semibold text-cyan-200 mb-3 leading-tight">{article.title || article.headline}</h4>
                    <p className="text-cyan-100/80 text-sm mb-4 leading-relaxed">{article.summary}</p>
                    <div className="flex items-center justify-between pt-3 border-t border-cyan-500/20">
                      <span className="text-xs text-cyan-400 font-medium">{article.source}</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse"></div>
                        <span className="text-xs text-cyan-300/60">Live</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <div className="text-cyan-300/50 text-6xl mb-4">📰</div>
                <div className="text-cyan-300/70 italic text-lg">No articles found</div>
              </div>
            )}
          </div>
        );

      case 'knowledge_summary':
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900">Research Results</h3>
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="text-gray-800 whitespace-pre-line">{data.summary}</div>
            </div>
            {data.sources && data.sources.length > 0 && (
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Sources:</h4>
                <ul className="space-y-1">
                  {data.sources.map((source: Source, index: number) => (
                    <li key={index} className="text-sm text-gray-600">
                      • {source.title} (Similarity: {Math.round(source.similarity_score * 100)}%)
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        );

      case 'research_results':
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-bold text-cyan-300">🔍 Research Results</h3>
              <span className="text-sm text-cyan-400 bg-cyan-900/30 px-3 py-1 rounded-full border border-cyan-500/30">
                {data.documents?.length || 0} Documents
              </span>
            </div>
            {data.documents && data.documents.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {data.documents.map((doc: Document, index: number) => (
                  <div key={index} className="bg-black/60 border border-cyan-500/30 rounded-xl p-5 backdrop-blur-sm shadow-lg hover:shadow-cyan-500/20 transition-all duration-300 hover:border-cyan-400/50">
                    <div className="flex items-start justify-between mb-3">
                      <span className="text-xs text-cyan-400 bg-cyan-900/40 px-2 py-1 rounded-full border border-cyan-500/30">
                        #{index + 1}
                      </span>
                      <span className="text-xs text-cyan-300/70">
                        {Math.round(doc.similarity_score * 100)}% Match
                      </span>
                    </div>
                    <h4 className="font-semibold text-cyan-200 mb-3 leading-tight">{doc.title}</h4>
                    <p className="text-cyan-100/80 text-sm mb-4 leading-relaxed">{doc.content.substring(0, 200)}...</p>
                    <div className="flex items-center justify-between pt-3 border-t border-cyan-500/20">
                      <span className="text-xs text-cyan-400 font-medium">{doc.source}</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                        <span className="text-xs text-cyan-300/60">Verified</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <div className="text-cyan-300/50 text-6xl mb-4">🔍</div>
                <div className="text-cyan-300/70 italic text-lg">No documents found</div>
              </div>
            )}
          </div>
        );

      case 'comprehensive_summary':
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold text-gray-900">Comprehensive Analysis</h3>
            
            {/* Main Summary */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
              <h4 className="font-medium text-blue-900 mb-3">📋 Summary</h4>
              <div className="text-blue-800 leading-relaxed whitespace-pre-line">
                {data.summary}
              </div>
            </div>

            {/* Key Insights */}
            {data.insights && data.insights.length > 0 && (
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <h4 className="font-medium text-green-900 mb-3">💡 Key Insights</h4>
                <ul className="space-y-2">
                  {data.insights.map((insight: string, index: number) => (
                    <li key={index} className="text-green-800 flex items-start">
                      <span className="mr-2">•</span>
                      <span>{insight}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Agent Contributions */}
            {data.agent_contributions && (
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                <h4 className="font-medium text-gray-900 mb-3">🤖 Agent Contributions</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {Object.entries(data.agent_contributions).map(([agent, info]: [string, AgentContribution]) => (
                    <div key={agent} className="flex items-center justify-between p-2 bg-white rounded border">
                      <span className="font-medium text-gray-700 capitalize">{agent.replace('_', ' ')}</span>
                      <span className={`px-2 py-1 rounded text-xs ${
                        info.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
                      }`}>
                        {info.contribution}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        );

      case 'learning_result':
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900">Learning Progress</h3>
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium">Articles Fetched:</span>
                <span className="text-sm font-bold text-green-800">{String(data.articles_fetched || 0)}</span>
              </div>
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium">Articles Stored:</span>
                <span className="text-sm font-bold text-green-800">{String(data.articles_stored || 0)}</span>
              </div>
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium">Learning Status:</span>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                  data.learning_successful ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {data.learning_successful ? 'Successful' : 'In Progress'}
                </span>
              </div>
              {data.reason ? (
                <div className="mt-3">
                  <span className="font-medium">Note:</span>
                  <p className="text-sm text-gray-600 mt-1">{String(data.reason)}</p>
                </div>
              ) : null}
            </div>
          </div>
        );

      case 'placeholder':
        return (
          <div className="text-center py-8">
            <div className="text-gray-400 mb-4">
              <svg className="mx-auto h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">System Initialized</h3>
            <p className="text-gray-600">{String(data)}</p>
          </div>
        );

      default:
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900">Results</h3>
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
              {data.error ? (
                <div className="text-red-600">
                  <strong>Error:</strong> {data.error}
                </div>
              ) : (
                <pre className="overflow-x-auto text-sm">
                  {JSON.stringify(data, null, 2)}
                </pre>
              )}
            </div>
          </div>
        );
    }
  };

  return (
    <div className="space-y-6">
      {/* Query Info */}
      <div className="border-b border-gray-200 dark:border-gray-700 pb-4">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">Query Results</h2>
        <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400">
          <span className="font-medium">Query:</span>
          <span className="italic">&ldquo;{results.query}&rdquo;</span>
        </div>
        {results.agents_used && results.agents_used.length > 0 && (
          <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400 mt-1">
            <span className="font-medium">Agents Used:</span>
            <span>{results.agents_used.join(', ')}</span>
          </div>
        )}
        {results.processing_time && (
          <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400 mt-1">
            <span className="font-medium">Processing Time:</span>
            <span>{results.processing_time.toFixed(2)}s</span>
          </div>
        )}
        {results.timestamp && (
          <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400 mt-1">
            <span className="font-medium">Timestamp:</span>
            <span>{formatTimestamp(results.timestamp)}</span>
          </div>
        )}
      </div>

      {/* Results Content */}
      <div>
        {renderResultContent()}
      </div>
    </div>
  );
}
