import React, { useState, useEffect } from 'react';
import { jobBotApi } from '../services/api';
import { Loader, AlertCircle, Briefcase, TrendingUp, CheckCircle, Clock } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Dashboard() {
  const [jobs, setJobs] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchResults();
    fetchStats();
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
    try {
      await jobBotApi.deleteResult(jobId);
      setJobs(jobs.filter(j => j.id !== jobId));
    } catch (err) {
      alert('Failed to delete job');
    }
  };

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
        <AlertCircle className="text-red-600 w-5 h-5 mt-1" />
        <div>
          <h3 className="font-semibold text-red-900">Connection Error</h3>
          <p className="text-red-800 text-sm">{error}</p>
          <p className="text-red-700 text-xs mt-2">Make sure the backend is running: <code className="bg-red-100 px-2 py-1">python backend/app.py</code></p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Job Dashboard</h1>

      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-blue-50 p-6 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm opacity-75">Total Jobs</p>
                <p className="text-2xl font-bold">{stats.total_jobs}</p>
              </div>
              <Briefcase className="w-8 h-8 opacity-50" />
            </div>
          </div>
          <div className="bg-green-50 p-6 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm opacity-75">High Fit</p>
                <p className="text-2xl font-bold">{stats.high_fit_jobs}</p>
              </div>
              <TrendingUp className="w-8 h-8 opacity-50" />
            </div>
          </div>
          <div className="bg-purple-50 p-6 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm opacity-75">Applied</p>
                <p className="text-2xl font-bold">{stats.applied}</p>
              </div>
              <CheckCircle className="w-8 h-8 opacity-50" />
            </div>
          </div>
          <div className="bg-yellow-50 p-6 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm opacity-75">Pending</p>
                <p className="text-2xl font-bold">{stats.pending}</p>
              </div>
              <Clock className="w-8 h-8 opacity-50" />
            </div>
          </div>
        </div>
      )}

      {loading ? (
        <div className="flex justify-center items-center py-12">
          <Loader className="w-8 h-8 text-blue-600 animate-spin" />
        </div>
      ) : jobs.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg mb-4">No job results yet</p>
          <a href="/search" className="text-blue-600 hover:underline">Start a new search →</a>
        </div>
      ) : (
        <div>
          {jobs.map(job => (
            <div key={job.id} className="bg-white rounded-lg shadow-sm p-6 mb-4">
              <div className="flex justify-between items-start mb-3">
                <div>
                  <Link to={`/job/${job.id}`}>
                    <h3 className="text-lg font-semibold text-blue-600 hover:underline">{job.title}</h3>
                  </Link>
                  <a href={job.url} target="_blank" rel="noopener noreferrer" className="text-sm text-gray-500 hover:underline">View Job</a>
                </div>
                <div className="px-4 py-2 rounded-lg font-bold text-lg bg-blue-100">{job.fit_score}</div>
              </div>
              <div className="flex justify-between items-center">
                <Link to={`/job/${job.id}`} className="text-blue-600 hover:underline">View Details →</Link>
                <button onClick={() => handleDelete(job.id)} className="text-red-500">Delete</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
