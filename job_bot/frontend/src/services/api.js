import axios from 'axios';

const API_BASE = '/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  }
});

export const jobBotApi = {
  health: () => api.get('/health'),
  getConfig: () => api.get('/config'),
  search: (query, numResults = 5) => api.post('/search', { query, num_results: numResults }),
  getSearchProgress: () => api.get('/search/progress'),
  getResults: (skip = 0, limit = 50) => api.get('/results', { params: { skip, limit } }),
  getResultDetail: (jobId) => api.get(`/results/${jobId}`),
  getCoverLetter: (jobId) => api.get(`/results/${jobId}/cover-letter`),
  applyToJob: (jobId) => api.post(`/results/${jobId}/apply`),
  deleteResult: (jobId) => api.delete(`/results/${jobId}`),
  getStats: () => api.get('/stats'),
  resetTracker: () => api.post('/reset'),
};

export default api;
