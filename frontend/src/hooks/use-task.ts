'use client';

import { useState, useEffect, useCallback } from 'react';
import { apiClient } from '@/lib/api';
import { Task, CreateTaskData, UpdateTaskData } from '@/types/task';
import { useToast } from './use-toast';

export function useTask() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { toast } = useToast();

  const fetchTasks = useCallback(async () => {
    try {
      setLoading(true);
      const response = await apiClient.getTasks();

      if (response.success && response.data) {
        // Transform backend response to frontend format for each task
        const transformedTasks = response.data.map(task => ({
          ...task,
          id: String(task.id),
          created_at: new Date(task.created_at),
          updated_at: new Date(task.updated_at),
          due_date: task.due_date ? new Date(task.due_date) : undefined
        }));

        setTasks(transformedTasks);
      } else {
        setError(response.error || 'Failed to fetch tasks');
        toast({
          title: 'Error',
          description: response.error || 'Failed to fetch tasks',
          variant: 'destructive',
        });
      }
    } catch (err) {
      setError('An unexpected error occurred');
      toast({
        title: 'Error',
        description: 'An unexpected error occurred',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  }, [setLoading, setTasks, setError, toast]);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

 

  const createTask = async (taskData: CreateTaskData) => {
    try {
      setLoading(true);

      // Transform frontend format to backend format
      const transformedData = {
        ...taskData,
        due_date: taskData.due_date ? new Date(taskData.due_date).toISOString() : undefined
      };

      const response = await apiClient.createTask(transformedData);

      if (response.success && response.data) {
        // Transform backend response to frontend format
        const transformedResponse = {
          ...response.data,
          id: String(response.data.id),
          created_at: new Date(response.data.created_at),
          updated_at: new Date(response.data.updated_at),
          due_date: response.data.due_date ? new Date(response.data.due_date) : undefined
        };

        setTasks(prev => [transformedResponse as Task, ...prev]);
        toast({
          title: 'Success',
          description: 'Task created successfully',
        });
        return transformedResponse;
      } else {
        setError(response.error || 'Failed to create task');
        toast({
          title: 'Error',
          description: response.error || 'Failed to create task',
          variant: 'destructive',
        });
        return null;
      }
    } catch (err) {
      setError('An unexpected error occurred');
      toast({
        title: 'Error',
        description: 'An unexpected error occurred',
        variant: 'destructive',
      });
      return null;
    } finally {
      setLoading(false);
    }
  };

  const updateTask = async (id: string, taskData: UpdateTaskData) => {
    try {
      setLoading(true);

      // Transform frontend format to backend format
      const transformedData = {
        ...taskData,
        due_date: taskData.due_date ? new Date(taskData.due_date).toISOString() : undefined
      };

      const response = await apiClient.updateTask(id, transformedData);

      if (response.success && response.data) {
        // Transform backend response to frontend format
        const transformedResponse = {
          ...response.data,
          id: String(response.data.id),
          created_at: new Date(response.data.created_at),
          updated_at: new Date(response.data.updated_at),
          due_date: response.data.due_date ? new Date(response.data.due_date) : undefined
        };

        setTasks(prev => prev.map(task => task.id === id ? transformedResponse as Task : task));
        toast({
          title: 'Success',
          description: 'Task updated successfully',
        });
        return transformedResponse;
      } else {
        setError(response.error || 'Failed to update task');
        toast({
          title: 'Error',
          description: response.error || 'Failed to update task',
          variant: 'destructive',
        });
        return null;
      }
    } catch (err) {
      setError('An unexpected error occurred');
      toast({
        title: 'Error',
        description: 'An unexpected error occurred',
        variant: 'destructive',
      });
      return null;
    } finally {
      setLoading(false);
    }
  };

  const deleteTask = async (id: string) => {
    try {
      setLoading(true);
      const response = await apiClient.deleteTask(id);

      if (response.success) {
        setTasks(prev => prev.filter(task => String(task.id) !== id));
        toast({
          title: 'Success',
          description: 'Task deleted successfully',
        });
        return true;
      } else {
        setError(response.error || 'Failed to delete task');
        toast({
          title: 'Error',
          description: response.error || 'Failed to delete task',
          variant: 'destructive',
        });
        return false;
      }
    } catch (err) {
      setError('An unexpected error occurred');
      toast({
        title: 'Error',
        description: 'An unexpected error occurred',
        variant: 'destructive',
      });
      return false;
    } finally {
      setLoading(false);
    }
  };

  const toggleTaskCompletion = async (id: string) => {
    try {
      const task = tasks.find(t => String(t.id) === id);
      if (!task) return null;

      // Toggle the completion status - if it was completed, set to incomplete, otherwise set to completed
      const newCompletedStatus = !task.completed;
      const response = await apiClient.toggleTaskCompletion(id, newCompletedStatus);

      if (response.success && response.data) {
        // Transform backend response to frontend format
        const transformedResponse = {
          ...response.data,
          id: String(response.data.id),
          created_at: new Date(response.data.created_at),
          updated_at: new Date(response.data.updated_at),
          due_date: response.data.due_date ? new Date(response.data.due_date) : undefined
        };

        setTasks(prev => prev.map(t => String(t.id) === id ? transformedResponse as Task : t));
        toast({
          title: newCompletedStatus ? 'Task marked as complete' : 'Task marked as incomplete',
          description: newCompletedStatus ? 'Task marked as complete' : 'Task marked as incomplete',
        });
        return transformedResponse;
      } else {
        setError(response.error || 'Failed to update task status');
        toast({
          title: 'Error',
          description: response.error || 'Failed to update task status',
          variant: 'destructive',
        });
        return null;
      }
    } catch (err) {
      setError('An unexpected error occurred');
      toast({
        title: 'Error',
        description: 'An unexpected error occurred',
        variant: 'destructive',
      });
      return null;
    }
  };

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
  };
}