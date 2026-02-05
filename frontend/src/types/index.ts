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

export interface User {
  id: number;
  email: string;
  is_active: boolean;
  email_verified: boolean;
  created_at: string; // ISO date string
  last_login?: string; // ISO date string (optional)
}

export interface UserRegistrationData {
  email: string;
  password: string;
}

export interface UserLoginData {
  email: string;
  password: string;
}

export interface UserPublic {
  id: number;
  email: string;
  is_active: boolean;
  email_verified: boolean;
  created_at: string;
}

export interface TaskFormData {
  title: string;
  description?: string;
}