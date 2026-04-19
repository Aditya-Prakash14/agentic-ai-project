import React, { useState, useEffect } from 'react';
import { jobBotApi } from '../services/api';
import { Loader, AlertCircle } from 'lucide-react';

export default function Settings() {
  const [config, setConfig] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchConfig();
  }, []);

  const fetchConfig = async () => {
    try {
      const response = await jobBotApi.getConfig();
      setConfig(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load configuration from backend');
      console.error('Config error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <Loader className="w-8 h-8 text-blue-600 animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600 mt-1">Job Bot configuration</p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
          <AlertCircle className="text-red-600 w-5 h-5 mt-0.5 flex-shrink-0" />
          <div>
            <h3 className="font-semibold text-red-900">Error</h3>
            <p className="text-red-800 text-sm">{error}</p>
          </div>
        </div>
      )}

      {config && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Fit Score Threshold */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="font-semibold text-gray-900 mb-2">Fit Score Threshold</h3>
            <p className="text-sm text-gray-600 mb-4">
              Only analyze jobs scoring at least this percentage
            </p>
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <p className="text-3xl font-bold text-blue-600">{config.fit_score_threshold}%</p>
            </div>
          </div>

          {/* Max Results */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="font-semibold text-gray-900 mb-2">Max Results Per Query</h3>
            <p className="text-sm text-gray-600 mb-4">
              Maximum job listings to process per search
            </p>
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <p className="text-3xl font-bold text-blue-600">{config.max_results}</p>
            </div>
          </div>

          {/* Enable Apply */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="font-semibold text-gray-900 mb-2">Auto Apply Enabled</h3>
            <p className="text-sm text-gray-600 mb-4">
              Automatically submit Easy Apply applications
            </p>
            <div className={`rounded-lg p-4 ${config.enable_apply ? 'bg-green-50 border border-green-200' : 'bg-gray-50 border border-gray-200'}`}>
              <p className={`text-lg font-bold ${config.enable_apply ? 'text-green-600' : 'text-gray-600'}`}>
                {config.enable_apply ? '✓ Enabled' : '✗ Disabled'}
              </p>
            </div>
          </div>

          {/* Auto Apply */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="font-semibold text-gray-900 mb-2">Auto Submit</h3>
            <p className="text-sm text-gray-600 mb-4">
              Automatically submit without confirmation
            </p>
            <div className={`rounded-lg p-4 ${config.auto_apply ? 'bg-amber-50 border border-amber-200' : 'bg-green-50 border border-green-200'}`}>
              <p className={`text-lg font-bold ${config.auto_apply ? 'text-amber-600' : 'text-green-600'}`}>
                {config.auto_apply ? '⚠️ Auto-submit (RISKY)' : '✓ Require confirmation (SAFE)'}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 mb-3">Configuration</h3>
        <p className="text-blue-800 text-sm mb-3">
          Settings are loaded from the backend environment. To change them, edit the <code className="bg-blue-100 px-1.5 py-0.5 rounded text-xs">.env</code> file and restart the backend server.
        </p>
        <pre className="bg-blue-100 p-3 rounded text-xs text-blue-900 overflow-x-auto">
{`FIT_SCORE_THRESHOLD=65
MAX_RESULTS_PER_QUERY=5
ENABLE_APPLY=true
AUTO_APPLY=false`}
        </pre>
      </div>
    </div>
  );
}
