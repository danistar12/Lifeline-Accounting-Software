import axios from 'axios';

const API_BASE = process.env.VUE_APP_API_BASE || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Optional: attach token if present in localStorage
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  // propagate selected company header if present in localStorage
  const selectedCompany = localStorage.getItem('selectedCompanyId');
  if (selectedCompany) {
    config.headers['X-Company-ID'] = selectedCompany;
  }
  // Debug: log outgoing request headers (avoid logging sensitive tokens in production)
  // Useful while diagnosing 401/CORS issues during local development
  // eslint-disable-next-line no-console
  console.debug('[apiClient] Request', config.method?.toUpperCase(), config.url, 'headers:', { ...config.headers });
  return config;
});

apiClient.interceptors.response.use(
  (response) => {
    // eslint-disable-next-line no-console
    console.debug('[apiClient] Response', response.status, response.config.url, response.headers);
    return response;
  },
  (error) => {
    // eslint-disable-next-line no-console
    console.debug('[apiClient] Response Error', error?.response?.status, error?.config?.url, error?.response?.headers);
    return Promise.reject(error);
  }
);

export default apiClient;
