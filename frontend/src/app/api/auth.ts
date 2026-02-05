import axios from 'axios';

// Base API URL from environment - defaults to backend on port 8000 during development
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid, redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/auth/login';
    }
    return Promise.reject(error);
  }
);

/**
 * Interface for user registration data
 */
export interface UserRegistrationData {
  email: string;
  password: string;
}

/**
 * Interface for user login data
 */
export interface UserLoginData {
  email: string;
  password: string;
}

/**
 * Interface for user data returned from API
 */
export interface UserData {
  id: number;
  email: string;
  is_active: boolean;
  email_verified: boolean;
  created_at: string; // ISO date string
}

/**
 * Interface for login response
 */
export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: UserData;
}

/**
 * Register a new user
 */
export const registerUser = async (userData: UserRegistrationData): Promise<UserData> => {
  try {
    const response = await api.post<UserData>('/auth/register', userData);
    return response.data;
  } catch (error) {
    console.error('Error registering user:', error);
    throw error;
  }
};

/**
 * Log in a user and return JWT token
 */
export const loginUser = async (credentials: UserLoginData): Promise<LoginResponse> => {
  try {
    const response = await api.post<LoginResponse>('/auth/login', credentials);

    // Store the access token in localStorage
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
    }

    return response.data;
  } catch (error) {
    console.error('Error logging in user:', error);
    throw error;
  }
};

/**
 * Log out the current user
 */
export const logoutUser = (): void => {
  // Remove the access token from localStorage
  localStorage.removeItem('access_token');

  // Redirect to login page
  window.location.href = '/auth/login';
};

/**
 * Get the current user's information
 */
export const getCurrentUser = async (): Promise<UserData> => {
  try {
    const response = await api.get<UserData>('/auth/me');
    return response.data;
  } catch (error) {
    console.error('Error fetching current user:', error);
    throw error;
  }
};

/**
 * Check if a user is currently authenticated
 */
export const isAuthenticated = (): boolean => {
  const token = localStorage.getItem('access_token');
  return !!token;
};

/**
 * Get the current access token
 */
export const getAccessToken = (): string | null => {
  return localStorage.getItem('access_token');
};