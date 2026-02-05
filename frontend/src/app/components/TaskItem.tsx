'use client';

import React, { useState } from 'react';
import { Task, TaskUpdateRequest } from '../../../../shared/types';
import { updateTask, deleteTask, toggleTaskCompletion } from '../api/tasks';

interface TaskItemProps {
  task: Task;
  onUpdate: (updatedTask: Task) => void;
  onDelete: (taskId: number) => void;
  userId: number;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onUpdate, onDelete, userId }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');
  const [isLoading, setIsLoading] = useState(false);

  const handleToggleComplete = async () => {
    setIsLoading(true);
    try {
      const updatedTask = await toggleTaskCompletion(task.id, userId, !task.completed);
      onUpdate(updatedTask);
    } catch (error) {
      console.error('Error toggling task completion:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
    setTitle(task.title);
    setDescription(task.description || '');
  };

  const handleSave = async () => {
    setIsLoading(true);
    try {
      const updateData: TaskUpdateRequest = {
        title,
        description: description || undefined,
      };

      const updatedTask = await updateTask(task.id, userId, updateData);
      onUpdate(updatedTask);
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating task:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    setIsEditing(false);
    setTitle(task.title);
    setDescription(task.description || '');
  };

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete "${task.title}"?`)) {
      setIsLoading(true);
      try {
        await deleteTask(task.id, userId);
        onDelete(task.id);
      } catch (error) {
        console.error('Error deleting task:', error);
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className={`p-4 mb-2 rounded-lg shadow ${
      task.completed ? 'bg-green-50 border-l-4 border-green-500' : 'bg-white border-l-4 border-blue-500'
    }`}>
      <div className="flex items-start">
        <input
          type="checkbox"
          checked={task.completed}
          onChange={handleToggleComplete}
          disabled={isLoading}
          className="mt-1 mr-3 h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
        />

        {isEditing ? (
          <div className="flex-1">
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full p-2 border rounded mb-2"
              placeholder="Task title"
            />
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full p-2 border rounded"
              placeholder="Task description (optional)"
              rows={2}
            />
            <div className="flex mt-2 space-x-2">
              <button
                onClick={handleSave}
                disabled={isLoading}
                className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
              >
                Save
              </button>
              <button
                onClick={handleCancel}
                disabled={isLoading}
                className="px-3 py-1 bg-gray-300 rounded hover:bg-gray-400 disabled:opacity-50"
              >
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <div className="flex-1">
            <h3 className={`text-lg ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
              {task.title}
            </h3>
            {task.description && (
              <p className={`mt-1 ${task.completed ? 'line-through text-gray-500' : 'text-gray-600'}`}>
                {task.description}
              </p>
            )}
            <p className="text-xs text-gray-500 mt-2">
              Created: {new Date(task.created_at).toLocaleString()}
            </p>
          </div>
        )}

        <div className="flex space-x-2 ml-4">
          {!isEditing && (
            <button
              onClick={handleEdit}
              disabled={isLoading}
              className="p-2 text-blue-500 hover:text-blue-700 disabled:opacity-50"
              title="Edit task"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
              </svg>
            </button>
          )}
          <button
            onClick={handleDelete}
            disabled={isLoading}
            className="p-2 text-red-500 hover:text-red-700 disabled:opacity-50"
            title="Delete task"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default TaskItem;