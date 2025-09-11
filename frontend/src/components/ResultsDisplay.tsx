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

interface SourceWithDetails {
  title: string;
  source?: string;
  similarity_score?: number;
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
            <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-700 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium text-gray-900 dark:text-gray-100">Sentiment:</span>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                  data.sentiment === 'positive' ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-200' :
                  data.sentiment === 'negative' ? 'bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-200' :
                  'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200'
                }`}>
                  {data.sentiment ? data.sentiment.charAt(0).toUpperCase() + data.sentiment.slice(1) : 'Unknown'}
                </span>
              </div>
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium text-gray-900 dark:text-gray-100">Confidence:</span>
                <span className="text-sm text-gray-700 dark:text-gray-300">{Math.round((data.confidence || 0) * 100)}%</span>
              </div>
              {data.text && (
                <div className="mt-3">
                  <span className="font-medium text-gray-900 dark:text-gray-100">Analyzed Text:</span>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{data.text}</p>
                </div>
              )}
            </div>
          </div>
        );

      case 'news_summary':
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900">News Summary</h3>
            {data.articles && data.articles.length > 0 ? (
              <div className="space-y-3">
                {data.articles.map((article: Article, index: number) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <h4 className="font-medium text-gray-900 mb-2">{article.headline}</h4>
                    <p className="text-gray-600 text-sm mb-2">{article.summary}</p>
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <span>{article.source}</span>
                      <span>{formatTimestamp(article.published_at)}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-gray-500 italic">No articles found</div>
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
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900">Research Results</h3>
            {data.documents && data.documents.length > 0 ? (
              <div className="space-y-3">
                {data.documents.map((doc: Document, index: number) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <h4 className="font-medium text-gray-900 mb-2">{doc.title}</h4>
                    <p className="text-gray-600 text-sm mb-2">{doc.content.substring(0, 200)}...</p>
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <span>{doc.source}</span>
                      <span>Similarity: {Math.round(doc.similarity_score * 100)}%</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-gray-500 italic">No documents found</div>
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

            {/* Recommendations */}
            {data.recommendations && data.recommendations.length > 0 && (
              <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                <h4 className="font-medium text-purple-900 mb-3">🎯 Recommendations</h4>
                <ul className="space-y-2">
                  {data.recommendations.map((recommendation: string, index: number) => (
                    <li key={index} className="text-purple-800 flex items-start">
                      <span className="mr-2">•</span>
                      <span>{recommendation}</span>
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

            {/* Sources */}
            {data.sources && data.sources.length > 0 && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <h4 className="font-medium text-yellow-900 mb-3">📚 Sources</h4>
                <div className="space-y-2">
                  {data.sources.slice(0, 5).map((source: SourceWithDetails, index: number) => (
                    <div key={index} className="text-yellow-800 text-sm">
                      <span className="font-medium">{source.title}</span>
                      {source.source && <span className="text-yellow-600"> - {source.source}</span>}
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
