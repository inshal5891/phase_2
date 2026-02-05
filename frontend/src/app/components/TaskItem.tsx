import { useState } from 'react';
import { Task } from '../../types';

interface TaskItemProps {
  task: Task;
  onToggle: (id: number, completed: boolean) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: number) => void;
  isLoading?: boolean;
}

export default function TaskItem({ task, onToggle, onEdit, onDelete, isLoading }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || '');

  const handleSaveEdit = () => {
    // Validation
    if (!editTitle.trim()) {
      alert('Title is required');
      return;
    }

    // Call parent onEdit with updated task data
    onEdit({ ...task, title: editTitle.trim(), description: editDescription.trim() });
    setIsEditing(false);
  };

  const handleCancelEdit = () => {
    // Reset to original values
    setEditTitle(task.title);
    setEditDescription(task.description || '');
    setIsEditing(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSaveEdit();
    } else if (e.key === 'Escape') {
      handleCancelEdit();
    }
  };

  return (
    <li className={`p-4 mb-2 ${task.completed ? 'bg-green-50' : 'bg-white'} shadow rounded-lg`}>
      {isEditing ? (
        <div className="space-y-3">
          <div>
            <input
              type="text"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isLoading}
              className="block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm disabled:bg-gray-100"
              placeholder="Task title"
              autoFocus
            />
          </div>
          <div>
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isLoading}
              rows={2}
              className="block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm disabled:bg-gray-100"
              placeholder="Task description (optional)"
            />
          </div>
          <div className="flex space-x-2">
            <button
              onClick={handleSaveEdit}
              disabled={isLoading}
              className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              Save
            </button>
            <button
              onClick={handleCancelEdit}
              disabled={isLoading}
              className="inline-flex items-center px-3 py-1.5 border border-gray-300 text-xs font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <>
          <div className="flex items-start">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={(e) => onToggle(task.id, e.target.checked)}
              disabled={isLoading}
              className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded mt-1"
            />
            <div className="ml-3 flex-1 min-w-0">
              <p className={`text-sm font-medium ${task.completed ? 'text-gray-500 line-through' : 'text-gray-900'}`}>
                {task.title}
              </p>
              {task.description && (
                <p className={`text-sm ${task.completed ? 'text-gray-400' : 'text-gray-500'} mt-1`}>
                  {task.description}
                </p>
              )}
              <p className="text-xs text-gray-400 mt-1">
                Created: {new Date(task.created_at).toLocaleDateString()}
              </p>
            </div>
          </div>

          <div className="flex justify-end space-x-2 mt-2">
            <button
              onClick={() => setIsEditing(true)}
              disabled={isLoading}
              className="inline-flex items-center p-1.5 border border-gray-300 text-xs font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
              Edit
            </button>
            <button
              onClick={() => onDelete(task.id)}
              disabled={isLoading}
              className="inline-flex items-center p-1.5 border border-transparent text-xs font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50"
            >
              Delete
            </button>
          </div>
        </>
      )}
    </li>
  );
}