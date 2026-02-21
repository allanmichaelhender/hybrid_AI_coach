import axios from "axios";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "./constants";
// ... rest of your axios logic


const api = axios.create({
  // Vite uses import.meta.env for .env variables
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1",
});

// 1. Request Interceptor: Attach the JWT to every outgoing call
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

// 2. Response Interceptor: Handle 401s (Expired Tokens) automatically
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If we get a 401 and haven't tried to refresh yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      const refreshToken = localStorage.getItem(REFRESH_TOKEN);

      if (!refreshToken) {
        return Promise.reject(error);
      }

      originalRequest._retry = true;

      try {
        // Call your FastAPI /auth/refresh endpoint
        const response = await axios.post(
          `${api.defaults.baseURL}/auth/refresh`,
          { refresh_token: refreshToken } // Matches our Backend schema
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
        window.location.href = "/login"; // Redirect to login
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  },
);

export default api;
