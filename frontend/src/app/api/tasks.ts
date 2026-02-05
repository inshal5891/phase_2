import axios from 'axios';
import { Task, TaskCreateRequest, TaskUpdateRequest } from '../../../../shared/types';

// Base API URL from environment - defaults to backend on port 8000 during development
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Fetch all tasks for a user
 */
export const fetchTasks = async (userId: number, completed?: boolean): Promise<Task[]> => {
  try {
    const params: { user_id: number; completed?: boolean } = { user_id: userId };
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
export const createTask = async (taskData: TaskCreateRequest): Promise<Task> => {
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
export const fetchTaskById = async (taskId: number, userId: number): Promise<Task> => {
  try {
    const response = await api.get<Task>(`/tasks/${taskId}`, {
      params: { user_id: userId }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching task by ID:', error);
    throw error;
  }
};

/**
 * Update a task
 */
export const updateTask = async (taskId: number, userId: number, taskData: TaskUpdateRequest): Promise<Task> => {
  try {
    const response = await api.put<Task>(`/tasks/${taskId}`, taskData, {
      params: { user_id: userId }
    });
    return response.data;
  } catch (error) {
    console.error('Error updating task:', error);
    throw error;
  }
};

/**
 * Delete a task
 */
export const deleteTask = async (taskId: number, userId: number): Promise<void> => {
  try {
    await api.delete(`/tasks/${taskId}`, {
      params: { user_id: userId }
    });
  } catch (error) {
    console.error('Error deleting task:', error);
    throw error;
  }
};

/**
 * Toggle task completion status
 */
export const toggleTaskCompletion = async (taskId: number, userId: number, completed: boolean): Promise<Task> => {
  try {
    const response = await api.patch<Task>(`/tasks/${taskId}/complete`,
      { completed },
      { params: { user_id: userId } }
    );
    return response.data;
  } catch (error) {
    console.error('Error toggling task completion:', error);
    throw error;
  }
};