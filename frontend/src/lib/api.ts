'use client';

import { Task, CreateTaskData, UpdateTaskData } from '@/types/task';
import { LoginCredentials, RegisterCredentials, AuthResponse, User } from '@/types/auth';
import { ApiResponse } from '@/types/api';
import { authClient } from './better-auth-client';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${API_BASE_URL}${endpoint}`;

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    // Get JWT token using Better Auth's token method (requires jwtClient plugin)
    try {
      const tokenResult = await authClient.token();
      if (tokenResult && !tokenResult.error && tokenResult.data && tokenResult.data.token) {
        headers['Authorization'] = `Bearer ${tokenResult.data.token}`;
      }
    } catch (error) {
      // If getting token fails, continue without it - some endpoints might be public
      console.warn('Could not retrieve JWT token:', error);
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
        // Include credentials to send cookies with requests
        // Use 'include' to send cookies for same-site and cross-site requests
        credentials: 'include'
      });

      // If 401, the session might be invalid
      if (response.status === 401) {
        // Optionally, try to refresh the session or clear local state
        console.warn('Unauthorized access - session may have expired');
      }

      const data = await response.json().catch(() => null);

      if (!response.ok) {
        // Transform generic error messages to user-friendly ones
        let errorMessage = data?.detail || 'An error occurred';
        let userFriendlyMessage = errorMessage;

        // Map technical error messages to user-friendly ones
        if (errorMessage.includes('Could not validate credentials')) {
          userFriendlyMessage = 'Your session has expired. Please log in again.';
        } else if (errorMessage.includes('User not found')) {
          userFriendlyMessage = 'Account not found. Please check your credentials.';
        } else if (errorMessage.includes('Invalid email or password')) {
          userFriendlyMessage = 'Invalid email or password. Please try again.';
        } else if (errorMessage.includes('Email already registered')) {
          userFriendlyMessage = 'This email is already registered. Please use a different email or try logging in.';
        } else if (response.status === 401) {
          userFriendlyMessage = 'Authentication required. Please log in to continue.';
        } else if (response.status === 403) {
          userFriendlyMessage = 'Access denied. You do not have permission to perform this action.';
        } else if (response.status === 404) {
          userFriendlyMessage = 'Requested resource not found.';
        } else if (response.status >= 500) {
          userFriendlyMessage = 'Server error. Please try again later.';
        }

        return {
          success: false,
          error: errorMessage,
          message: userFriendlyMessage,
        };
      }

      return {
        success: true,
        data,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Network error',
        message: 'Failed to connect to the server',
      };
    }
  }

  // Auth - These methods will now use Better Auth's client-side methods
  async login(credentials: LoginCredentials): Promise<ApiResponse<AuthResponse>> {
    // Use Better Auth's login method instead of backend call
    try {
      const result = await authClient.signIn?.email({
        email: credentials.email,
        password: credentials.password,
        callbackURL: '/dashboard',
      });

      if (result?.error) {
        return {
          success: false,
          error: result.error.message || 'Login failed',
          message: result.error.message || 'Login failed',
        };
      }

      // Get the session after successful login
      const sessionResult = await authClient.getSession();
      if (sessionResult?.error || !sessionResult?.data || !sessionResult?.data.user) {
        return {
          success: false,
          error: 'Failed to establish session after login',
          message: 'Failed to establish session after login',
        };
      }

      const session = sessionResult.data;
      const user: User = {
        id: session.user.id,
        email: session.user.email,
        name: session.user.name || session.user.email?.split('@')[0] || '',
        createdAt: session.user.createdAt || new Date(),
        updatedAt: session.user.updatedAt || new Date(),
      };

      return {
        success: true,
        data: {
          access_token: session.session?.token || '', // JWT token from Better Auth
          refreshToken: '', // Better Auth manages refresh internally
          user: user,
        },
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Login failed',
        message: 'Login failed',
      };
    }
  }

  async register(credentials: RegisterCredentials): Promise<ApiResponse<AuthResponse>> {
    // Use Better Auth's register method
    try {
      const result = await authClient.signUp?.email({
        email: credentials.email,
        password: credentials.password,
        name: credentials.name || credentials.email.split('@')[0],
      });

      if (result?.error) {
        return {
          success: false,
          error: result.error.message || 'Registration failed',
          message: result.error.message || 'Registration failed',
        };
      }

      // Get the session after successful registration
      const sessionResult = await authClient.getSession();
      if (sessionResult?.error || !sessionResult?.data || !sessionResult?.data.user) {
        return {
          success: false,
          error: 'Failed to establish session after registration',
          message: 'Failed to establish session after registration',
        };
      }

      const session = sessionResult.data;
      const user: User = {
        id: session.user.id,
        email: session.user.email,
        name: session.user.name || session.user.email?.split('@')[0] || '',
        createdAt: session.user.createdAt || new Date(),
        updatedAt: session.user.updatedAt || new Date(),
      };

      // The backend will automatically sync the user when the first authenticated request is made
      // The get_current_user function in backend handles creating the user in the backend database
      // with the same ID as Better Auth when the JWT token is validated

      return {
        success: true,
        data: {
          access_token: session.session?.token || '', // JWT token from Better Auth
          refreshToken: '', // Better Auth manages refresh internally
          user: user,
        },
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Registration failed',
        message: 'Registration failed',
      };
    }
  }

  async logout(): Promise<ApiResponse<null>> {
    // Call Better Auth's signout method
    try {
      await authClient.signOut();

      return {
        success: true,
        data: null,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Logout failed',
        message: 'Logout failed',
      };
    }
  }

  // Get profile information using Better Auth session instead of backend call
  async getProfile(): Promise<ApiResponse<User>> {
    try {
      const sessionResult = await authClient.getSession();

      if (!sessionResult || sessionResult.error || !sessionResult.data || !sessionResult.data.user) {
        return {
          success: false,
          error: 'User not authenticated',
          message: 'User not authenticated'
        };
      }

      const sessionData = sessionResult.data;

      // Map Better Auth user to our User type
      const user: User = {
        id: sessionData.user.id,
        email: sessionData.user.email,
        name: sessionData.user.name || sessionData.user.email?.split('@')[0] || '',
        createdAt: sessionData.user.createdAt || new Date(),
        updatedAt: sessionData.user.updatedAt || new Date(),
      };

      return {
        success: true,
        data: user,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Failed to get profile',
        message: 'Failed to get profile',
      };
    }
  }

  // Tasks CRUD - Get the user ID from Better Auth session
  private async getCurrentUserId(): Promise<string> {
    const profile = await this.getProfile();
    if (!profile.success || !profile.data) throw new Error('User not logged in');
    return profile.data.id;
  }

  async getTasks(): Promise<ApiResponse<Task[]>> {
    const userId = await this.getCurrentUserId();
    return this.request<Task[]>(`/api/${userId}/tasks`);
  }

  async getTaskById(id: string): Promise<ApiResponse<Task>> {
    const userId = await this.getCurrentUserId();
    return this.request<Task>(`/api/${userId}/tasks/${id}`);
  }

  async createTask(taskData: CreateTaskData): Promise<ApiResponse<Task>> {
    const userId = await this.getCurrentUserId();

    // Format dates to ISO string for backend compatibility
    const formattedTaskData = {
      ...taskData,
      due_date: taskData.due_date ? (typeof taskData.due_date === 'string' ? taskData.due_date : (taskData.due_date && typeof taskData.due_date === 'object' && 'toISOString' in taskData.due_date && typeof (taskData.due_date as any).toISOString === 'function' ? (taskData.due_date as Date).toISOString() : undefined)) : undefined
    };

    return this.request<Task>(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(formattedTaskData),
    });
  }

  async updateTask(id: string, taskData: UpdateTaskData): Promise<ApiResponse<Task>> {
    const userId = await this.getCurrentUserId();

    // Format dates to ISO string for backend compatibility
    const formattedTaskData = {
      ...taskData,
      due_date: taskData.due_date ? (typeof taskData.due_date === 'string' ? taskData.due_date : (taskData.due_date && typeof taskData.due_date === 'object' && 'toISOString' in taskData.due_date && typeof (taskData.due_date as any).toISOString === 'function' ? (taskData.due_date as Date).toISOString() : undefined)) : undefined
    };

    return this.request<Task>(`/api/${userId}/tasks/${id}`, {
      method: 'PUT',
      body: JSON.stringify(formattedTaskData),
    });
  }

  async deleteTask(id: string): Promise<ApiResponse<null>> {
    const userId = await this.getCurrentUserId();
    return this.request<null>(`/api/${userId}/tasks/${id}`, {
      method: 'DELETE',
    });
  }

  async toggleTaskCompletion(id: string, completed: boolean): Promise<ApiResponse<Task>> {
    const userId = await this.getCurrentUserId();
    return this.request<Task>(`/api/${userId}/tasks/${id}/complete`, {
      method: 'PATCH',
      body: JSON.stringify({ completed }),
    });
  }
}

export const apiClient = new ApiClient();

// Export individual methods as standalone functions for ease of use
export const getTaskById = apiClient.getTaskById.bind(apiClient);
export const updateTask = apiClient.updateTask.bind(apiClient);
export const deleteTask = apiClient.deleteTask.bind(apiClient);
export const getTasks = apiClient.getTasks.bind(apiClient);
export const createTask = apiClient.createTask.bind(apiClient);
export const toggleTaskCompletion = apiClient.toggleTaskCompletion.bind(apiClient);
export const login = apiClient.login.bind(apiClient);
export const register = apiClient.register.bind(apiClient);
export const logout = apiClient.logout.bind(apiClient);
export const getProfile = apiClient.getProfile.bind(apiClient);

