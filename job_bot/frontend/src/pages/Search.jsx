import React, { useState, useEffect } from 'react';
import { jobBotApi } from '../services/api';
import { Loader, AlertCircle, Search as SearchIcon } from 'lucide-react';

export default function Search() {
  const [query, setQuery] = useState('');
  const [numResults, setNumResults] = useState(5);
  const [searching, setSearching] = useState(false);
  const [progress, setProgress] = useState(null);
  const [error, setError] = useState(null);
  const [completed, setCompleted] = useState(false);

  useEffect(() => {
    if (searching) {
      const interval = setInterval(async () => {
        try {
          const response = await jobBotApi.getSearchProgress();
          setProgress(response.data);
          if (!response.data.is_running) {
            setSearching(false);
            setCompleted(true);
          }
        } catch (err) {
          console.error('Failed to get search progress');
        }
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [searching]);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) {
      setError('Please enter a search query');
      return;
    }
    try {
      setError(null);
      setCompleted(false);
      setSearching(true);
      setProgress(null);
      await jobBotApi.search(query, numResults);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start search');
      setSearching(false);
    }
  };

  return (
    <div className="space-y-8 max-w-2xl">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Search Jobs</h1>
        <p className="text-slate-600 mt-1">Find opportunities that match your profile</p>
      </div>

      {/* Search Form */}
      <div className="bg-white rounded-lg border border-slate-200 p-8">
        <form onSubmit={handleSearch} className="space-y-6">
          {/* Query Input */}
          <div>
            <label className="block text-sm font-semibold text-slate-900 mb-2">Search Query</label>
            <div className="relative">
              <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
              <input 
                type="text" 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g., Python developer internship, Backend engineer"
                className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100 text-slate-900 placeholder-slate-400"
                disabled={searching}
              />
            </div>
          </div>

          {/* Number of Results */}
          <div>
            <label className="block text-sm font-semibold text-slate-900 mb-2">Number of Results</label>
            <div className="flex gap-2">
              {[1, 3, 5, 10, 20].map((num) => (
                <button
                  key={num}
                  type="button"
                  onClick={() => setNumResults(num)}
                  disabled={searching}
                  className={`px-4 py-2 rounded-lg font-medium text-sm transition-colors ${
                    numResults === num
                      ? 'bg-blue-600 text-white'
                      : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                  } disabled:opacity-50`}
                >
                  {num}
                </button>
              ))}
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
              <AlertCircle className="text-red-600 w-5 h-5 mt-0.5 flex-shrink-0" />
              <p className="text-red-700 text-sm">{error}</p>
            </div>
          )}

          {/* Submit Button */}
          <button 
            type="submit"
            disabled={searching}
            className="w-full px-6 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
          >
            {searching ? (
              <>
                <Loader className="w-4 h-4 animate-spin" /> 
                Searching...
              </>
            ) : (
              'Start Search'
            )}
          </button>
        </form>
      </div>

      {/* Progress Indicator */}
      {progress && searching && (
        <div className="bg-white rounded-lg border border-slate-200 p-6">
          <h2 className="font-semibold text-slate-900 mb-4">Search Progress</h2>
          <div className="space-y-4">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-slate-600">{progress.progress} of {progress.total}</span>
                <span className="text-sm font-medium text-slate-700">{progress.status}</span>
              </div>
              <div className="w-full h-2 bg-slate-200 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-blue-600 transition-all duration-300"
                  style={{width: progress.total > 0 ? `${(progress.progress / progress.total) * 100}%` : '0%'}}
                />
              </div>
            </div>
            {progress.current_job && (
              <p className="text-sm text-slate-600 truncate">
                Currently: {progress.current_job}
              </p>
            )}
          </div>
        </div>
      )}

      {/* Completion Message */}
      {completed && !searching && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
          <p className="text-green-800 font-semibold">✓ Search completed!</p>
          <p className="text-green-700 text-sm mt-1">Your jobs have been analyzed and added to the dashboard.</p>
          <a href="/" className="inline-block mt-4 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm font-semibold">
            View Results
          </a>
        </div>
      )}
    </div>
  );
}
