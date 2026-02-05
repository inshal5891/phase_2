'use client';

import React, { useState, useEffect } from 'react';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';
import FilterButtons from './components/FilterButtons';
import { Task } from '../../../shared/types';
import { fetchTasks } from './api/tasks';

const HomePage = () => {
  // Using a fixed user ID for this spec (authentication deferred to Spec 2)
  const userId = 1;
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filter, setFilter] = useState<'all' | 'completed' | 'pending'>('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load tasks when component mounts or filter changes
  useEffect(() => {
    const loadTasks = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch tasks based on the current filter
        // We'll fetch all tasks and filter client-side for now
        const allTasks = await fetchTasks(userId);
        setTasks(allTasks);
      } catch (err) {
        console.error('Error loading tasks:', err);
        setError('Failed to load tasks. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    loadTasks();
  }, [userId]); // Reload tasks when userId changes

  const handleTaskCreated = (newTask: Task) => {
    setTasks([newTask, ...tasks]);
  };

  const handleTaskUpdated = (updatedTask: Task) => {
    setTasks(tasks.map(task => task.id === updatedTask.id ? updatedTask : task));
  };

  const handleTaskDeleted = (deletedTaskId: number) => {
    setTasks(tasks.filter(task => task.id !== deletedTaskId));
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mb-4"></div>
          <p className="text-lg text-gray-600">Loading tasks...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md p-6 bg-white rounded-lg shadow text-center">
          <div className="text-red-500 text-2xl mb-4">⚠️</div>
          <h2 className="text-xl font-bold text-gray-800 mb-2">Error Loading Tasks</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <header className="mb-12 text-center">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-800 mb-2">
            Todo Web Application
          </h1>
          <p className="text-gray-600">
            Manage your tasks efficiently with our full-stack todo application
          </p>
        </header>

        <main>
          <TaskForm onTaskCreated={handleTaskCreated} userId={userId} />

          <div className="bg-white rounded-lg shadow p-6">
            <FilterButtons
              currentFilter={filter}
              onFilterChange={setFilter}
            />

            <TaskList
              tasks={tasks}
              onUpdate={handleTaskUpdated}
              onDelete={handleTaskDeleted}
              userId={userId}
              filter={filter}
            />
          </div>
        </main>

        <footer className="mt-12 text-center text-gray-500 text-sm">
          <p>© {new Date().getFullYear()} Todo Web Application. All rights reserved.</p>
        </footer>
      </div>
    </div>
  );
};

export default HomePage;