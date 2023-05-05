import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
});

api.defaults.headers.common['Authorization'] = `Token ${process.env.REACT_APP_APPLICATION_TOKEN}`;

export default api;
