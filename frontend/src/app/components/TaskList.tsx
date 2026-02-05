'use client';

import React from 'react';
import { Task } from '../../../../shared/types';
import TaskItem from './TaskItem';

interface TaskListProps {
  tasks: Task[];
  onUpdate: (updatedTask: Task) => void;
  onDelete: (taskId: number) => void;
  userId: number;
  filter: 'all' | 'completed' | 'pending';
}

const TaskList: React.FC<TaskListProps> = ({ tasks, onUpdate, onDelete, userId, filter }) => {
  // Filter tasks based on the selected filter
  const filteredTasks = tasks.filter(task => {
    if (filter === 'completed') return task.completed;
    if (filter === 'pending') return !task.completed;
    return true; // 'all' filter
  });

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">
        {filter === 'completed' ? 'Completed Tasks' :
         filter === 'pending' ? 'Pending Tasks' : 'All Tasks'}
        <span className="ml-2 text-sm font-normal text-gray-600">({filteredTasks.length})</span>
      </h2>

      {filteredTasks.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          {filter === 'completed'
            ? 'No completed tasks yet.'
            : filter === 'pending'
              ? 'No pending tasks. Great job!'
              : 'No tasks yet. Add one to get started!'}
        </div>
      ) : (
        <div>
          {filteredTasks.map(task => (
            <TaskItem
              key={task.id}
              task={task}
              onUpdate={onUpdate}
              onDelete={onDelete}
              userId={userId}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default TaskList;