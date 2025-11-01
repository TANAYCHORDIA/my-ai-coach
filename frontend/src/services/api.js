import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';

// Create axios instance with timeout
const axiosInstance = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
});

export const chatAPI = {
  sendQuery: async (text, userId, mode) => {
    try {
      const response = await axiosInstance.post('/api/chat', {
        text,
        user_id: userId,
        mode: mode // 'quick-tip' or 'in-depth'
      });
      return response.data;
    } catch (error) {
      console.error('API Error:', error);
      throw new Error(error.response?.data?.detail || 'Failed to get response from Coach Carter');
    }
  },
  
  healthCheck: async () => {
    try {
      const response = await axiosInstance.get('/api/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      return null;
    }
  }
};
