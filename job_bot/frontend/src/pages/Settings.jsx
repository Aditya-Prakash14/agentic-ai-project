import React, { useState, useEffect } from 'react';
import { jobBotApi } from '../services/api';
import { Loader, AlertCircle, CheckCircle } from 'lucide-react';

export default function Settings() {
  const [config, setConfig] = useState(null);
  const [llmConfig, setLlmConfig] = useState(null);
  const [loading, setLoading] = useState(true);
  const [llmLoading, setLlmLoading] = useState(true);
  const [selectedProvider, setSelectedProvider] = useState(null);
  const [apiKey, setApiKey] = useState('');
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    fetchConfig();
    fetchLlmConfig();
  }, []);

  const fetchConfig = async () => {
    try {
      const response = await jobBotApi.getConfig();
      setConfig(response.data);
    } finally {
      setLoading(false);
    }
  };

  const fetchLlmConfig = async () => {
    try {
      const response = await jobBotApi.getLlmConfig();
      setLlmConfig(response.data);
      setSelectedProvider(response.data.active_provider);
    } finally {
      setLlmLoading(false);
    }
  };

  const handleSetProvider = async (e) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);

    try {
      const payload = {
        provider: selectedProvider,
        api_key: apiKey || null
      };
      
      await jobBotApi.setLlmProvider(payload);
      setMessage({ type: 'success', text: `LLM provider set to ${selectedProvider}` });
      setApiKey('');
      await fetchLlmConfig();
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: error.response?.data?.detail || 'Failed to set LLM provider' 
      });
    } finally {
      setSaving(false);
    }
  };

  if (loading || llmLoading) {
    return <div className="flex justify-center items-center py-12"><Loader className="w-8 h-8 text-blue-600 animate-spin" /></div>;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Settings</h1>
      
      {/* LLM Provider Configuration */}
      <div className="bg-white rounded-lg shadow-sm p-8 mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">LLM Provider Configuration</h2>
        
        {message && (
          <div className={`mb-6 p-4 rounded-lg flex items-start gap-3 ${
            message.type === 'success' ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
          }`}>
            {message.type === 'success' ? (
              <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
            ) : (
              <AlertCircle className="w-5 h-5 text-red-600 mt-0.5" />
            )}
            <p className={`text-sm ${message.type === 'success' ? 'text-green-800' : 'text-red-800'}`}>
              {message.text}
            </p>
          </div>
        )}

        {llmConfig && (
          <>
            <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-sm text-blue-800">
                <strong>Active Provider:</strong> {llmConfig.available_providers.find(p => p.name === llmConfig.active_provider)?.display_name}
              </p>
            </div>

            <form onSubmit={handleSetProvider} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-3">
                  Select LLM Provider
                </label>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {llmConfig.available_providers.map((provider) => (
                    <div
                      key={provider.name}
                      onClick={() => setSelectedProvider(provider.name)}
                      className={`p-4 rounded-lg border-2 cursor-pointer transition ${
                        selectedProvider === provider.name
                          ? 'border-blue-600 bg-blue-50'
                          : 'border-gray-200 bg-white hover:border-gray-300'
                      } ${!provider.installed ? 'opacity-50' : ''}`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <p className="font-medium text-gray-900">{provider.display_name}</p>
                          <p className="text-xs text-gray-600 mt-1">
                            {provider.installed ? '✓ Installed' : '⚠ Not installed (pip required)'}
                          </p>
                        </div>
                        <div className={`w-5 h-5 rounded border-2 mt-1 ${
                          selectedProvider === provider.name
                            ? 'bg-blue-600 border-blue-600'
                            : 'border-gray-300'
                        }`} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {selectedProvider !== 'ollama' && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    API Key
                  </label>
                  <input
                    type="password"
                    placeholder="Enter API key (leave empty to keep existing)"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-transparent"
                  />
                  <p className="text-xs text-gray-600 mt-1">
                    {llmConfig.configured_providers.includes(selectedProvider)
                      ? '✓ Already configured'
                      : 'This provider is not yet configured'}
                  </p>
                </div>
              )}

              <button
                type="submit"
                disabled={saving}
                className="w-full bg-blue-600 text-white font-medium py-2 px-4 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition"
              >
                {saving ? 'Saving...' : 'Set Provider'}
              </button>
            </form>

            <div className="mt-8 pt-8 border-t">
              <h3 className="font-semibold text-gray-900 mb-4">Provider Details</h3>
              <div className="space-y-3 text-sm">
                <div>
                  <p className="font-medium text-gray-900">🚀 Recommended:</p>
                  <p className="text-gray-600">Groq - Fast, cheap, and easy to set up</p>
                </div>
                <div>
                  <p className="font-medium text-gray-900">💰 Free Options:</p>
                  <p className="text-gray-600">Ollama (local) - No API key needed</p>
                </div>
              </div>
            </div>
          </>
        )}
      </div>

      {/* Other Settings */}
      <div className="bg-white rounded-lg shadow-sm p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Job Search Settings</h2>
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
