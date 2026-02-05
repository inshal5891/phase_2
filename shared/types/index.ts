export interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string; // ISO date string
  user_id: number;
}

export interface TaskCreateRequest {
  title: string;
  description?: string;
}

export interface TaskUpdateRequest {
  title?: string;
  description?: string;
  completed?: boolean;
}