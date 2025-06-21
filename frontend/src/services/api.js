import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL;
const API_URL = `${API_BASE_URL}/api`;

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('fixnet_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('fixnet_token');
      localStorage.removeItem('fixnet_admin');
      window.location.href = '/admin/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (email, password) => {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
  },
  
  logout: async () => {
    await api.post('/auth/logout');
    localStorage.removeItem('fixnet_token');
    localStorage.removeItem('fixnet_admin');
  },
  
  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
  
  validateToken: async () => {
    const response = await api.get('/auth/validate-token');
    return response.data;
  }
};

// Repair Requests API
export const repairAPI = {
  createRequest: async (requestData) => {
    const response = await api.post('/repair-requests/', requestData);
    return response.data;
  },
  
  getRequests: async (params = {}) => {
    const response = await api.get('/repair-requests/', { params });
    return response.data;
  },
  
  getRequest: async (ticketId) => {
    const response = await api.get(`/repair-requests/${ticketId}`);
    return response.data;
  },
  
  updateStatus: async (ticketId, status, notes) => {
    const response = await api.put(`/repair-requests/${ticketId}/status`, {
      ticket_id: ticketId,
      status,
      notes
    });
    return response.data;
  },
  
  updateRequest: async (ticketId, updateData) => {
    const response = await api.put(`/repair-requests/${ticketId}`, updateData);
    return response.data;
  },
  
  deleteRequest: async (ticketId) => {
    const response = await api.delete(`/repair-requests/${ticketId}`);
    return response.data;
  },
  
  getDashboardStats: async () => {
    const response = await api.get('/repair-requests/stats/dashboard');
    return response.data;
  }
};

// Contact API
export const contactAPI = {
  sendMessage: async (messageData) => {
    const response = await api.post('/contact/', messageData);
    return response.data;
  },
  
  getMessages: async (params = {}) => {
    const response = await api.get('/contact/', { params });
    return response.data;
  },
  
  markAsRead: async (messageId) => {
    const response = await api.put(`/contact/${messageId}/read`);
    return response.data;
  },
  
  deleteMessage: async (messageId) => {
    const response = await api.delete(`/contact/${messageId}`);
    return response.data;
  }
};

export default api;