import axios from 'axios';

// Create a central axios instance pointing to your FastAPI backend
const api = axios.create({
  baseURL: 'http://localhost:8000', // Ensure this matches your backend port
});

// Add a request interceptor
api.interceptors.request.use(
  (config) => {
    // Check if we have a token in local storage
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;