import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { jobBotApi } from '../services/api';
import { ArrowLeft, ExternalLink, Copy, CheckCircle, Loader, AlertCircle } from 'lucide-react';

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
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <Loader className="w-8 h-8 text-blue-600 animate-spin mb-4" />
        <p className="text-slate-600">Loading job details...</p>
      </div>
    );
  }

  if (error || !job) {
    return (
      <div className="space-y-4">
        <button onClick={() => navigate('/')} className="text-blue-600 hover:text-blue-700 flex items-center gap-2 font-medium">
          <ArrowLeft className="w-4 h-4" /> Back to Dashboard
        </button>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-700">{error}</p>
        </div>
      </div>
    );
  }

  const getFitColor = (score) => {
    if (score >= 80) return 'bg-green-50 text-green-700 border-green-200';
    if (score >= 65) return 'bg-blue-50 text-blue-700 border-blue-200';
    if (score >= 50) return 'bg-amber-50 text-amber-700 border-amber-200';
    return 'bg-slate-50 text-slate-700 border-slate-200';
  };

  return (
    <div className="space-y-6">
      {/* Back Button */}
      <button 
        onClick={() => navigate('/')} 
        className="text-blue-600 hover:text-blue-700 flex items-center gap-2 font-medium"
      >
        <ArrowLeft className="w-4 h-4" /> Back to Dashboard
      </button>

      {/* Job Header */}
      <div className="bg-white rounded-lg border border-slate-200 p-8">
        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-6">
          <div className="flex-1">
            <h1 className="text-3xl font-bold text-slate-900">{job.title}</h1>
            <a 
              href={job.url} 
              target="_blank" 
              rel="noopener noreferrer" 
              className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 font-medium mt-3"
            >
              Visit Job Posting
              <ExternalLink className="w-4 h-4" />
            </a>
            {job.snippet && (
              <p className="text-slate-600 mt-4 leading-relaxed">{job.snippet}</p>
            )}
          </div>

          {/* Fit Score */}
          <div className={`flex flex-col items-center gap-4 px-6 py-4 rounded-lg border ${getFitColor(job.fit_score)}`}>
            <p className="text-4xl font-bold">{job.fit_score}%</p>
            <p className="text-sm font-semibold">Match</p>
          </div>
        </div>

        {/* Apply Button */}
        <button 
          onClick={handleApply}
          disabled={applying || job.applied}
          className={`mt-6 px-6 py-2 rounded-lg font-semibold transition-colors flex items-center gap-2 ${
            job.applied
              ? 'bg-green-50 text-green-700 border border-green-200'
              : 'bg-blue-600 text-white hover:bg-blue-700'
          } disabled:opacity-50`}
        >
          {job.applied ? (
            <><CheckCircle className="w-4 h-4" /> Applied</>
          ) : applying ? (
            <><Loader className="w-4 h-4 animate-spin" /> Applying...</>
          ) : (
            'Mark as Applied'
          )}
        </button>
      </div>

      {/* Strengths and Gaps */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Strengths */}
        <div className="bg-white rounded-lg border border-slate-200 p-6">
          <h2 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
            <CheckCircle className="w-5 h-5 text-green-600" />
            Your Strengths
          </h2>
          {job.strengths && job.strengths.length > 0 ? (
            <ul className="space-y-2">
              {job.strengths.map((strength, i) => (
                <li key={i} className="text-slate-700 text-sm">✓ {strength}</li>
              ))}
            </ul>
          ) : (
            <p className="text-slate-600 text-sm italic">No strengths identified</p>
          )}
        </div>

        {/* Gaps */}
        <div className="bg-white rounded-lg border border-slate-200 p-6">
          <h2 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-amber-600" />
            Gaps to Address
          </h2>
          {job.gaps && job.gaps.length > 0 ? (
            <ul className="space-y-2">
              {job.gaps.map((gap, i) => (
                <li key={i} className="text-slate-700 text-sm">! {gap}</li>
              ))}
            </ul>
          ) : (
            <p className="text-slate-600 text-sm italic">No gaps identified</p>
          )}
        </div>
      </div>

      {/* Cover Letter */}
      {job.cover_letter && (
        <div className="bg-white rounded-lg border border-slate-200 p-6">
          <h2 className="text-lg font-bold text-slate-900 mb-4">Generated Cover Letter</h2>
          
          {/* Letter Content */}
          <div className="bg-slate-50 border border-slate-200 rounded-lg p-4 mb-4">
            <pre className="text-slate-700 whitespace-pre-wrap font-sans text-sm leading-relaxed max-h-96 overflow-y-auto">
              {job.cover_letter}
            </pre>
          </div>

          {/* Copy Button */}
          <button 
            onClick={() => handleCopy(job.cover_letter)}
            className="px-4 py-2 bg-slate-700 text-white rounded-lg font-medium hover:bg-slate-800 transition-colors flex items-center gap-2"
          >
            <Copy className="w-4 h-4" /> 
            {copied ? 'Copied!' : 'Copy Cover Letter'}
          </button>
        </div>
      )}
    </div>
  );
}
