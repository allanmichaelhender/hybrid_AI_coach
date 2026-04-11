import axios, { type AxiosInstance, type InternalAxiosRequestConfig, type AxiosError } from 'axios';
import { ACCESS_TOKEN, REFRESH_TOKEN } from './constants';

interface RefreshResponse {
  access_token: string;
}

const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
});

// Extend InternalAxiosRequestConfig to include _retry flag
type ExtendedAxiosRequestConfig = InternalAxiosRequestConfig & {
  _retry?: boolean;
};

// Request Interceptor: Attach the JWT to every outgoing call
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError): Promise<AxiosError> => Promise.reject(error)
);

// Response Interceptor: Handle 401s (Expired Tokens) automatically
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError): Promise<unknown> => {
    const originalRequest = error.config as ExtendedAxiosRequestConfig;

    // If we get a 401 and haven't tried to refresh yet
    if (error.response?.status === 401 && originalRequest && !originalRequest._retry) {
      const refreshToken = localStorage.getItem(REFRESH_TOKEN);

      if (!refreshToken) {
        return Promise.reject(error);
      }

      originalRequest._retry = true;

      try {
        // Call FastAPI /auth/refresh endpoint
        const response = await axios.post<RefreshResponse>(
          `${api.defaults.baseURL}/auth/refresh`,
          { refresh_token: refreshToken }
        );

        if (response.status === 200) {
          const newToken = response.data.access_token;
          localStorage.setItem(ACCESS_TOKEN, newToken);

          // Update the original failed request and retry it
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // If refresh fails, the session is dead. Clear everything.
        localStorage.removeItem(ACCESS_TOKEN);
        localStorage.removeItem(REFRESH_TOKEN);
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
