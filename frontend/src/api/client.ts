import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';

const API_TIMEOUT = 10000;

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api/v1',
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor: Inject JWT token into headers
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response Interceptor: Handle errors globally
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // Standard response structure is: { success: false, message: "...", errors: ... }
    const responseData = error.response?.data as { message?: string } | undefined;
    const errorMessage = responseData?.message || error.message || 'An unexpected error occurred';

    if (error.response?.status === 401) {
      // Clear credentials on unauthorized response
      localStorage.removeItem('token');
      // Redirect or raise event to auth provider
    }

    return Promise.reject(new Error(errorMessage));
  }
);
export default apiClient;
