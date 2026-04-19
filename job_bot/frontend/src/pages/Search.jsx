import React, { useState, useEffect } from 'react';
import { jobBotApi } from '../services/api';
import { Loader, AlertCircle, Play } from 'lucide-react';

export default function Search() {
  const [query, setQuery] = useState('');
  const [numResults, setNumResults] = useState(5);
  const [searching, setSearching] = useState(false);
  const [progress, setProgress] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (searching) {
      const interval = setInterval(async () => {
        try {
          const response = await jobBotApi.getSearchProgress();
          setProgress(response.data);
          if (!response.data.is_running) {
            setSearching(false);
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
      setSearching(true);
      setProgress(null);
      await jobBotApi.search(query, numResults);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start search');
      setSearching(false);
    }
  };

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-8">New Job Search</h1>
      <div className="bg-white rounded-lg shadow-sm p-8 mb-8">
        <form onSubmit={handleSearch} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Search Query</label>
            <input 
              type="text" 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., Python developer internship"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg"
              disabled={searching}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Number of Results</label>
            <input 
              type="number" 
              value={numResults}
              onChange={(e) => setNumResults(parseInt(e.target.value))}
              min="1" max="20"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg"
              disabled={searching}
            />
          </div>
          {error && <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-800">{error}</div>}
          <button 
            type="submit"
            disabled={searching}
            className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg disabled:bg-gray-400 font-medium flex items-center justify-center gap-2"
          >
            {searching ? <><Loader className="w-5 h-5 animate-spin" /> Searching...</> : <><Play className="w-5 h-5" /> Start Search</>}
          </button>
        </form>
      </div>
      {progress && searching && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-8">
          <h2 className="text-lg font-semibold mb-4">Search in Progress</h2>
          <div className="space-y-4">
            <div>
              <div className="w-full bg-blue-200 rounded-full h-2">
                <div className="bg-blue-600 h-2 rounded-full" style={{width: progress.total > 0 ? `${(progress.progress / progress.total) * 100}%` : '0%'}}></div>
              </div>
              <p className="text-xs text-blue-700 mt-2">{progress.progress} / {progress.total}</p>
            </div>
            <p className="text-blue-600">{progress.status}</p>
            {progress.current_job && <p className="text-blue-600 truncate">{progress.current_job}</p>}
          </div>
        </div>
      )}
    </div>
  );
}
