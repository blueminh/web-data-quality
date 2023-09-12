// axiosConfig.js
import axios from 'axios';
import serverUrl from '../config';

const API_BASE_URL = serverUrl;

const instance = axios.create({
  // Set your base URL and other configurations here
  baseURL: API_BASE_URL,
});

// Add a response interceptor to handle 403 status code
instance.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      // Redirect to the login page
      localStorage.setItem('authData', JSON.stringify({
        isLoggedIn: false,
      }))
      window.location.href = '/login'; // Replace with your login page URL
    }

    if (error.response && error.response.status === 403) {
        console.log("insufficient permission")
    }
    
    return Promise.reject(error);
  }
);

export default instance;