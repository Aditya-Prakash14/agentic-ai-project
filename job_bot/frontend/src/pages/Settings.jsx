import React, { useState, useEffect } from 'react';
import { jobBotApi } from '../services/api';
import { Loader, AlertCircle } from 'lucide-react';

export default function Settings() {
  const [config, setConfig] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchConfig();
  }, []);

  const fetchConfig = async () => {
    try {
      const response = await jobBotApi.getConfig();
      setConfig(response.data);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center py-12"><Loader className="w-8 h-8 text-blue-600 animate-spin" /></div>;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Settings</h1>
      <div className="bg-white rounded-lg shadow-sm p-8">
        {config && (
          <div className="space-y-6">
            <div className="border-b pb-6">
              <h3 className="font-semibold text-gray-900 mb-2">Fit Score Threshold</h3>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-3xl font-bold text-blue-600">{config.fit_score_threshold}</p>
              </div>
            </div>
            <div className="border-b pb-6">
              <h3 className="font-semibold text-gray-900 mb-2">Max Results Per Query</h3>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-3xl font-bold text-blue-600">{config.max_results}</p>
              </div>
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">Automated Applications</h3>
              <div className="space-y-3">
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm font-medium">Enable Apply: {config.enable_apply ? '✓' : '✗'}</p>
                </div>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm font-medium">Auto Apply: {config.auto_apply ? '✓' : '✗'}</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
