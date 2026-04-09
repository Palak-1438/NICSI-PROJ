import axios from 'axios';

const API_BASE_URL = '/api';

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor to include auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor to handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async login(credentials) {
    const response = await this.client.post('/login', credentials);
    return response.data;
  }

  async register(userData) {
    const response = await this.client.post('/register', userData);
    return response.data;
  }

  // Complaint endpoints
  async getComplaints(endpoint = '') {
    const response = await this.client.get(`/complaints${endpoint}`);
    return response.data;
  }

  async createComplaint(complaintData) {
    const response = await this.client.post('/complaints', complaintData);
    return response.data;
  }

  async updateComplaintStatus(complaintId, status) {
    const response = await this.client.put(`/complaints/${complaintId}/status`, { status });
    return response.data;
  }

  async assignComplaint(complaintId, officerId) {
    const response = await this.client.put(`/complaints/${complaintId}/assign`, {
      assigned_officer_id: officerId
    });
    return response.data;
  }
}

export default new ApiService();