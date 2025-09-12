"use client";

import { useState } from 'react';

interface QueryInputProps {
  onQuery: (query: string) => void;
  loading: boolean;
  placeholder?: string;
}

export default function QueryInput({ onQuery, loading, placeholder }: QueryInputProps) {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !loading) {
      onQuery(inputValue.trim());
      setInputValue('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="w-full">
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="relative">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={placeholder || "Ask a question..."}
            className="w-full px-6 py-4 bg-black/50 border border-cyan-500/30 rounded-xl focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/50 resize-none text-white placeholder-cyan-300/70 backdrop-blur-sm shadow-lg"
            rows={4}
            disabled={loading}
          />
          <div className="absolute bottom-4 right-4 text-sm text-cyan-300/70 font-medium">
            {inputValue.length}/1000
          </div>
        </div>
        
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-6 text-sm text-cyan-300/80">
            <span className="font-medium">Press Enter to submit</span>
            <span>•</span>
            <span className="font-medium">Shift + Enter for new line</span>
          </div>
          
          <button
            type="submit"
            disabled={!inputValue.trim() || loading}
            className="bg-cyan-600 text-white px-8 py-3 rounded-xl hover:bg-cyan-700 disabled:bg-gray-600 disabled:cursor-not-allowed transition-all duration-300 flex items-center space-x-3 font-medium shadow-lg hover:shadow-cyan-500/25"
          >
            {loading ? (
              <>
                <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Processing...</span>
              </>
            ) : (
              <>
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
                <span>Submit Query</span>
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
