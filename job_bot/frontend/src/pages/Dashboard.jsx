import React, { useState, useEffect } from 'react';
import { jobBotApi } from '../services/api';
import { Loader, AlertCircle, BarChart3, CheckCircle, Clock, Trash2 } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Dashboard() {
  const [jobs, setJobs] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchResults();
    fetchStats();
    const interval = setInterval(() => {
      fetchResults();
      fetchStats();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchResults = async () => {
    try {
      const response = await jobBotApi.getResults();
      let sorted = response.data.results || [];
      sorted.sort((a, b) => (b.fit_score || 0) - (a.fit_score || 0));
      setJobs(sorted);
    } catch (err) {
      setError('Failed to load jobs');
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await jobBotApi.getStats();
      setStats(response.data);
    } catch (err) {
      console.error('Failed to fetch stats');
    }
  };

  const handleDelete = async (jobId) => {
    if (!window.confirm('Delete this job from your list?')) return;
    try {
      await jobBotApi.deleteResult(jobId);
      setJobs(jobs.filter(j => j.id !== jobId));
    } catch (err) {
      alert('Failed to delete job');
    }
  };

  const getFitColor = (score) => {
    if (score >= 80) return 'text-green-600 bg-green-50 border-green-200';
    if (score >= 65) return 'text-blue-600 bg-blue-50 border-blue-200';
    if (score >= 50) return 'text-amber-600 bg-amber-50 border-amber-200';
    return 'text-gray-600 bg-gray-50 border-gray-200';
  };

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">Your job search overview</p>
      </div>

      {stats && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm font-medium">Total Jobs</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{stats.total_jobs}</p>
              </div>
              <BarChart3 className="w-10 h-10 text-blue-600 opacity-20" />
            </div>
          </div>

          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm font-medium">High Fit (80%+)</p>
                <p className="text-3xl font-bold text-green-600 mt-2">{stats.high_fit_count || 0}</p>
              </div>
              <CheckCircle className="w-10 h-10 text-green-600 opacity-20" />
            </div>
          </div>

          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm font-medium">Applied</p>
                <p className="text-3xl font-bold text-blue-600 mt-2">{stats.applied_count || 0}</p>
              </div>
              <CheckCircle className="w-10 h-10 text-blue-600 opacity-20" />
            </div>
          </div>

          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm font-medium">Pending</p>
                <p className="text-3xl font-bold text-amber-600 mt-2">{stats.pending_count || 0}</p>
              </div>
              <Clock className="w-10 h-10 text-amber-600 opacity-20" />
            </div>
          </div>
        </div>
      )}

      <div>
        <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Jobs</h2>
        
        {loading ? (
          <div className="flex justify-center py-12">
            <Loader className="w-8 h-8 text-blue-600 animate-spin" />
          </div>
        ) : jobs.length === 0 ? (
          <div className="bg-gray-50 rounded-lg border border-gray-200 p-8 text-center">
            <AlertCircle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No jobs found. Start a search to get started.</p>
            <Link to="/search" className="inline-block mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              Start Search
            </Link>
          </div>
        ) : (
          <div className="space-y-3">
            {jobs.map((job) => (
              <Link key={job.id} to={`/job/${job.id}`}>
                <div className="bg-white rounded-lg border border-gray-200 p-4 hover:border-blue-300 hover:shadow-md transition-all">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900">{job.title}</h3>
                      <p className="text-sm text-gray-600 mt-1 line-clamp-2">{job.snippet}</p>
                      <p className="text-xs text-gray-500 mt-2">
                        {job.url ? new URL(job.url).hostname : 'Unknown source'}
                      </p>
                    </div>
                    
                    <div className="flex items-center gap-2 flex-shrink-0">
                      <div className={`px-3 py-1 rounded-full text-sm font-semibold border ${getFitColor(job.fit_score)}`}>
                        {job.fit_score}%
                      </div>
                      <button
                        onClick={(e) => {
                          e.preventDefault();
                          handleDelete(job.id);
                        }}
                        className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
