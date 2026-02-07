'use client';

import { useState, useEffect } from 'react';
import { Task } from '../../types';
import { fetchTasks, createTask, updateTask, deleteTask, toggleTaskCompletion } from '../../services/tasks';
import TaskList from '../components/TaskList';
import TaskForm from '../components/TaskForm';
import ProtectedRoute from '../components/ProtectedRoute';

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'completed' | 'pending'>('all');

  // Load tasks
  useEffect(() => {
    const loadTasks = async () => {
      try {
        const tasksData = await fetchTasks();
        setTasks(tasksData);
      } catch (err) {
        setError('Failed to load tasks');
        console.error('Error loading tasks:', err);
      } finally {
        setLoading(false);
      }
    };

    loadTasks();
  }, []);

  const handleCreateTask = async (taskData: { title: string; description?: string }) => {
    try {
      const newTask = await createTask(taskData);
      setTasks([...tasks, newTask]);
    } catch (err) {
      setError('Failed to create task');
      console.error('Error creating task:', err);
    }
  };

  const handleUpdateTask = async (updatedTask: Task) => {
    try {
      const task = await updateTask(updatedTask.id, {
        title: updatedTask.title,
        description: updatedTask.description,
        completed: updatedTask.completed
      });

      setTasks(tasks.map(t => t.id === task.id ? task : t));
    } catch (err) {
      setError('Failed to update task');
      console.error('Error updating task:', err);
    }
  };

  const handleDeleteTask = async (id: number) => {
    try {
      await deleteTask(id);
      setTasks(tasks.filter(task => task.id !== id));
    } catch (err) {
      setError('Failed to delete task');
      console.error('Error deleting task:', err);
    }
  };

  const handleToggleTask = async (id: number, completed: boolean) => {
    try {
      const task = await toggleTaskCompletion(id, completed);
      setTasks(tasks.map(t => t.id === id ? task : t));
    } catch (err) {
      setError('Failed to update task status');
      console.error('Error toggling task:', err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/3 mb-6"></div>
            <div className="bg-white shadow rounded-lg">
              <div className="p-4 border-b border-gray-200">
                <div className="h-4 bg-gray-200 rounded w-1/4"></div>
              </div>
              <div className="p-4">
                <div className="space-y-4">
                  {[1, 2, 3].map(i => (
                    <div key={i} className="p-4 bg-gray-100 rounded-lg">
                      <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                      <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">My Tasks</h1>

          {error && (
            <div className="mb-4 p-4 bg-red-50 text-red-700 rounded-md">
              {error}
            </div>
          )}

          <TaskForm onCreateTask={handleCreateTask} isLoading={loading} />

          <div className="mt-8">
            <TaskList
              tasks={tasks}
              onToggle={handleToggleTask}
              onEdit={handleUpdateTask}
              onDelete={handleDeleteTask}
              filter={filter}
              setFilter={setFilter}
              isLoading={loading}
            />
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}