"use client";

interface ResultsDisplayProps {
  results: any;
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

    const { type, data } = results.result;

    switch (type) {
      case 'sentiment_analysis':
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900">Sentiment Analysis</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {data.positive && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div className="text-2xl font-bold text-green-600">{data.positive}</div>
                  <div className="text-sm text-green-700">Positive</div>
                </div>
              )}
              {data.negative && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <div className="text-2xl font-bold text-red-600">{data.negative}</div>
                  <div className="text-sm text-red-700">Negative</div>
                </div>
              )}
              {data.neutral && (
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                  <div className="text-2xl font-bold text-gray-600">{data.neutral}</div>
                  <div className="text-sm text-gray-700">Neutral</div>
                </div>
              )}
            </div>
          </div>
        );

      case 'news_summary':
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900">News Summary</h3>
            <div className="space-y-3">
              {data.articles?.map((article: any, index: number) => (
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
          </div>
        );

      case 'document_answer':
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900">Research Results</h3>
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <p className="text-gray-800">{data.answer}</p>
            </div>
            {data.sources && data.sources.length > 0 && (
              <div>
                <h4 className="font-medium text-gray-900 mb-2">Sources:</h4>
                <ul className="space-y-1">
                  {data.sources.map((source: any, index: number) => (
                    <li key={index} className="text-sm text-gray-600">
                      • {source.title} (Confidence: {Math.round(source.confidence * 100)}%)
                    </li>
                  ))}
                </ul>
              </div>
            )}
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
            <p className="text-gray-600">{data}</p>
          </div>
        );

      default:
        return (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900">Results</h3>
            <pre className="bg-gray-50 border border-gray-200 rounded-lg p-4 overflow-x-auto">
              {JSON.stringify(data, null, 2)}
            </pre>
          </div>
        );
    }
  };

  return (
    <div className="space-y-6">
      {/* Query Info */}
      <div className="border-b border-gray-200 pb-4">
        <h2 className="text-xl font-semibold text-gray-900 mb-2">Query Results</h2>
        <div className="flex items-center justify-between text-sm text-gray-600">
          <span className="font-medium">Query:</span>
          <span className="italic">"{results.query}"</span>
        </div>
        {results.agents_used && results.agents_used.length > 0 && (
          <div className="flex items-center justify-between text-sm text-gray-600 mt-1">
            <span className="font-medium">Agents Used:</span>
            <span>{results.agents_used.join(', ')}</span>
          </div>
        )}
        {results.processing_time && (
          <div className="flex items-center justify-between text-sm text-gray-600 mt-1">
            <span className="font-medium">Processing Time:</span>
            <span>{results.processing_time.toFixed(2)}s</span>
          </div>
        )}
        {results.timestamp && (
          <div className="flex items-center justify-between text-sm text-gray-600 mt-1">
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
