export interface Task {
  id: number | string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: Date;
  updated_at: Date;
  due_date?: Date;
  user_id: string;
}

export interface CreateTaskData {
  title: string;
  description?: string;
  due_date?: string; // Backend expects ISO string format
}

export interface UpdateTaskData {
  title?: string;
  description?: string;
  completed?: boolean;
  due_date?: string; // Backend expects ISO string format
}