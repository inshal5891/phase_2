import api from '../../lib/api';
import { Task, TaskUpdateRequest } from '../../../shared/types';

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
 * Interface for task creation request (without user_id, which is derived from JWT)
 */
export interface TaskCreateRequest {
  title: string;
  description?: string;
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

/**
 * Fetch all tasks for the authenticated user
 */
export const fetchTasks = async (completed?: boolean): Promise<Task[]> => {
  try {
    const params: { completed?: boolean } = {};
    if (completed !== undefined) {
      params.completed = completed;
    }

    const response = await api.get<Task[]>('/tasks', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching tasks:', error);
    throw error;
  }
};

/**
 * Create a new task
 */
export const createTask = async (taskData: { title: string; description?: string }): Promise<Task> => {
  try {
    const response = await api.post<Task>('/tasks', taskData);
    return response.data;
  } catch (error) {
    console.error('Error creating task:', error);
    throw error;
  }
};

/**
 * Fetch a specific task by ID
 */
export const fetchTaskById = async (taskId: number): Promise<Task> => {
  try {
    const response = await api.get<Task>(`/tasks/${taskId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching task by ID:', error);
    throw error;
  }
};

/**
 * Update a task
 */
export const updateTask = async (taskId: number, taskData: TaskUpdateRequest): Promise<Task> => {
  try {
    const response = await api.put<Task>(`/tasks/${taskId}`, taskData);
    return response.data;
  } catch (error) {
    console.error('Error updating task:', error);
    throw error;
  }
};

/**
 * Delete a task
 */
export const deleteTask = async (taskId: number): Promise<void> => {
  try {
    await api.delete(`/tasks/${taskId}`);
  } catch (error) {
    console.error('Error deleting task:', error);
    throw error;
  }
};

/**
 * Toggle task completion status
 */
export const toggleTaskCompletion = async (taskId: number, completed: boolean): Promise<Task> => {
  try {
    const response = await api.patch<Task>(
      `/tasks/${taskId}/complete`,
      { completed }
    );
    return response.data;
  } catch (error) {
    console.error('Error toggling task completion:', error);
    throw error;
  }
};