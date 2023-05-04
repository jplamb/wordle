import axios from 'axios';

const baseUrl = '/api/';

const api = axios.create({
  baseURL: baseUrl,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${localStorage.getItem('token')}` // If using token authentication
  },
});

export default api;
