import api from '../lib/api';
import { Task, TaskUpdateRequest } from '../types';

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