import { Task } from '../../types';
import TaskItem from './TaskItem';

interface TaskListProps {
  tasks: Task[];
  onToggle: (id: number, completed: boolean) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: number) => void;
  filter: 'all' | 'completed' | 'pending';
  setFilter: (filter: 'all' | 'completed' | 'pending') => void;
  isLoading?: boolean;
}

export default function TaskList({ tasks, onToggle, onEdit, onDelete, filter, setFilter, isLoading }: TaskListProps) {
  // Filter tasks based on the selected filter
  const filteredTasks = tasks.filter(task => {
    if (filter === 'completed') return task.completed;
    if (filter === 'pending') return !task.completed;
    return true; // 'all' filter
  });

  return (
    <div className="bg-white shadow rounded-lg">
      {/* Filter Controls */}
      <div className="border-b border-gray-200 p-4">
        <div className="flex space-x-2">
          <button
            onClick={() => setFilter('all')}
            className={`px-3 py-1.5 text-sm font-medium rounded-md ${
              filter === 'all'
                ? 'bg-indigo-100 text-indigo-700'
                : 'text-gray-500 hover:bg-gray-100'
            }`}
          >
            All
          </button>
          <button
            onClick={() => setFilter('pending')}
            className={`px-3 py-1.5 text-sm font-medium rounded-md ${
              filter === 'pending'
                ? 'bg-indigo-100 text-indigo-700'
                : 'text-gray-500 hover:bg-gray-100'
            }`}
          >
            Pending
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`px-3 py-1.5 text-sm font-medium rounded-md ${
              filter === 'completed'
                ? 'bg-indigo-100 text-indigo-700'
                : 'text-gray-500 hover:bg-gray-100'
            }`}
          >
            Completed
          </button>
        </div>
      </div>

      {/* Task Count Summary */}
      <div className="p-4 border-b border-gray-200">
        <p className="text-sm text-gray-700">
          Showing <span className="font-medium">{filteredTasks.length}</span> of{' '}
          <span className="font-medium">{tasks.length}</span>{' '}
          {tasks.length === 1 ? 'task' : 'tasks'}
          {filter !== 'all' && (
            <span> ({filter === 'completed' ? 'completed' : 'pending'})</span>
          )}
        </p>
      </div>

      {/* Task List */}
      <ul className="divide-y divide-gray-200">
        {filteredTasks.length > 0 ? (
          filteredTasks.map(task => (
            <TaskItem
              key={task.id}
              task={task}
              onToggle={onToggle}
              onEdit={onEdit}
              onDelete={onDelete}
              isLoading={isLoading}
            />
          ))
        ) : (
          <li className="p-6 text-center">
            <div className="text-gray-500">
              {filter === 'completed'
                ? 'No completed tasks yet.'
                : filter === 'pending'
                  ? 'No pending tasks. Great job!'
                  : 'No tasks yet. Add one to get started!'}
            </div>
          </li>
        )}
      </ul>
    </div>
  );
}