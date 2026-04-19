import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { jobBotApi } from '../services/api';
import { ArrowLeft, ExternalLink, Copy, CheckCircle, Loader } from 'lucide-react';

export default function JobDetail() {
  const { jobId } = useParams();
  const navigate = useNavigate();
  const [job, setJob] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);
  const [applying, setApplying] = useState(false);

  useEffect(() => {
    fetchJobDetail();
  }, [jobId]);

  const fetchJobDetail = async () => {
    try {
      const response = await jobBotApi.getResultDetail(jobId);
      setJob(response.data);
    } catch (err) {
      setError('Failed to load job details');
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleApply = async () => {
    try {
      setApplying(true);
      await jobBotApi.applyToJob(jobId);
      setJob({ ...job, applied: true });
    } catch (err) {
      alert('Failed to mark as applied');
    } finally {
      setApplying(false);
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center py-12"><Loader className="w-8 h-8 text-blue-600 animate-spin" /></div>;
  }

  if (error || !job) {
    return (
      <div>
        <button onClick={() => navigate('/')} className="text-blue-600 mb-6">← Back</button>
        <div className="bg-red-50 p-4 text-red-800">{error}</div>
      </div>
    );
  }

  return (
    <div>
      <button onClick={() => navigate('/')} className="text-blue-600 mb-6 flex items-center gap-2"><ArrowLeft className="w-4 h-4" /> Back</button>
      
      <div className="bg-white rounded-lg shadow-sm p-8 mb-6">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{job.title}</h1>
            <a href={job.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline flex items-center gap-2">
              {job.url} <ExternalLink className="w-4 h-4" />
            </a>
          </div>
          <div className="text-4xl font-bold text-blue-600">{job.fit_score}%</div>
        </div>

        <button 
          onClick={handleApply}
          disabled={applying || job.applied}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg disabled:bg-gray-400 flex items-center gap-2"
        >
          {job.applied ? <><CheckCircle className="w-4 h-4" /> Applied</> : 
           applying ? <><Loader className="w-4 h-4 animate-spin" /> Applying...</> :
           'Mark as Applied'}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="bg-green-50 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-green-900 mb-4">Strengths</h2>
          {job.strengths?.length > 0 ? (
            <ul className="space-y-2">
              {job.strengths.map((s, i) => <li key={i} className="text-green-800">✓ {s}</li>)}
            </ul>
          ) : <p className="text-green-700">No strengths</p>}
        </div>
        <div className="bg-red-50 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-red-900 mb-4">Gaps</h2>
          {job.gaps?.length > 0 ? (
            <ul className="space-y-2">
              {job.gaps.map((g, i) => <li key={i} className="text-red-800">✗ {g}</li>)}
            </ul>
          ) : <p className="text-red-700">No gaps</p>}
        </div>
      </div>

      {job.cover_letter && (
        <div className="bg-white rounded-lg shadow-sm p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Cover Letter</h2>
          <div className="bg-gray-50 p-6 rounded-lg mb-4 text-gray-800 whitespace-pre-wrap max-h-96 overflow-y-auto">
            {job.cover_letter}
          </div>
          <button 
            onClick={() => handleCopy(job.cover_letter)}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg flex items-center gap-2"
          >
            <Copy className="w-4 h-4" /> {copied ? 'Copied!' : 'Copy Letter'}
          </button>
        </div>
      )}
    </div>
  );
}
