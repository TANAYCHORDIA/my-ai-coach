import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';

const axiosInstance = axios.create({
  baseURL: API_BASE,
  timeout: 300000,  // 5 minutes instead of 1 minute
});
export const chatAPI = {
  // Send query to AI backend
  sendQuery: async (text, userId, mode) => {
    try {
      console.log('📤 Sending query:', { text, userId, mode });
      
      const response = await axiosInstance.post('/api/chat', {
        text: text,
        user_id: userId,
        mode: mode || 'in-depth'
      });
      
      console.log('📥 Response received:', response.data);
      
      // Ensure response has required fields
      return {
        response_text: response.data.response_text || '',
        risk_scores: response.data.risk_scores || [],
        youtube_links: response.data.youtube_links || []
      };
    } catch (error) {
      console.error('❌ sendQuery error:', error.response?.data || error.message);
      throw new Error(
        error.response?.data?.detail || 
        error.message || 
        'Failed to get response from Coach Carter'
      );
    }
  },

  // Health check
  healthCheck: async () => {
    try {
      const response = await axiosInstance.get('/api/health');
      console.log('✅ Health check passed:', response.data);
      return response.data;
    } catch (error) {
      console.error('❌ Health check failed:', error.message);
      return null;
    }
  },

  // Get athlete profile
  getProfile: async (userId) => {
    try {
      const response = await axiosInstance.get(`/api/profile/${userId}`);
      return response.data;
    } catch (error) {
      console.error('❌ Get profile error:', error.message);
      return null;
    }
  }
};
