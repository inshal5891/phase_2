import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import TaskForm from '../../src/app/components/TaskForm';

describe('TaskForm', () => {
  const mockOnTaskCreated = jest.fn();
  const userId = 1;

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders form elements correctly', () => {
    render(
      <TaskForm onTaskCreated={mockOnTaskCreated} userId={userId} />
    );

    expect(screen.getByLabelText(/Title \*/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Description \(Optional\)/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Add Task/i })).toBeInTheDocument();
  });

  test('validates required title field', async () => {
    render(
      <TaskForm onTaskCreated={mockOnTaskCreated} userId={userId} />
    );

    const submitButton = screen.getByRole('button', { name: /Add Task/i });
    fireEvent.click(submitButton);

    expect(await screen.findByText(/Title is required/i)).toBeInTheDocument();
  });

  test('allows task submission with valid input', () => {
    render(
      <TaskForm onTaskCreated={mockOnTaskCreated} userId={userId} />
    );

    const titleInput = screen.getByLabelText(/Title \*/i);
    const descriptionInput = screen.getByLabelText(/Description \(Optional\)/i);
    const submitButton = screen.getByRole('button', { name: /Add Task/i });

    fireEvent.change(titleInput, { target: { value: 'Test Task' } });
    fireEvent.change(descriptionInput, { target: { value: 'Test Description' } });
    fireEvent.click(submitButton);

    expect(mockOnTaskCreated).toHaveBeenCalledWith(
      expect.objectContaining({
        title: 'Test Task',
        description: 'Test Description'
      })
    );
  });

  test('shows error for title exceeding character limit', () => {
    render(
      <TaskForm onTaskCreated={mockOnTaskCreated} userId={userId} />
    );

    const titleInput = screen.getByLabelText(/Title \*/i);
    const submitButton = screen.getByRole('button', { name: /Add Task/i });

    fireEvent.change(titleInput, { target: { value: 'A'.repeat(256) } }); // Over the 255 char limit
    fireEvent.click(submitButton);

    expect(screen.getByText(/Title must be 255 characters or less/i)).toBeInTheDocument();
  });
});