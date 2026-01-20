'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { TaskForm } from '@/components/forms/task-form';
import { getTaskById, updateTask, deleteTask } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';
import { Task, UpdateTaskData, CreateTaskData } from '@/types/task';
import Link from 'next/link';
import AuthGuard from '@/components/auth/auth-guard';

export default function TaskEditPage() {
  const { id } = useParams();
  const router = useRouter();
  const { toast } = useToast();
  const [task, setTask] = useState<Omit<Task, 'created_at' | 'updated_at'> | null>(null);
  const [loading, setLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    const fetchTask = async () => {
      try {
        if (typeof id === 'string') {
          const response = await getTaskById(id);

          if (response.success && response.data) {
            // Remove created_at and updated_at from the task data to match the form requirements
            const { created_at: _createdAt, updated_at: _updatedAt, ...taskWithoutTimestamps } = response.data;
            setTask(taskWithoutTimestamps);
          } else {
            throw new Error(response.error || 'Failed to fetch task');
          }
        }
      } catch (error) {
        console.error('Failed to fetch task:', error);
        toast({
          title: 'Error',
          description: 'Failed to load task details.',
          variant: 'destructive',
        });
        router.push(`/dashboard`);
      } finally {
        setLoading(false);
      }
    };

    fetchTask();
  }, [id, toast, router]);

  const handleSubmit = async (taskData: { title: string; description?: string; dueDate?: Date }) => {
    if (!task || typeof id !== 'string') return;

    setIsSubmitting(true);
    try {
      // Convert the form data to the correct format for updateTask
      const updateData: UpdateTaskData = {
        title: taskData.title,
        description: taskData.description,
        due_date: taskData.dueDate ? taskData.dueDate.toISOString() : undefined,
      };

      await updateTask(id as string, updateData);
      toast({
        title: 'Success',
        description: 'Task updated successfully.',
      });
      router.push(`/tasks/${id}`);
      router.refresh();
    } catch (error) {
      console.error('Failed to update task:', error);
      toast({
        title: 'Error',
        description: 'Failed to update task. Please try again.',
        variant: 'destructive',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto py-8">
        <Card>
          <CardHeader>
            <CardTitle>Loading...</CardTitle>
          </CardHeader>
          <CardContent>
            <p>Loading task details...</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!task) {
    return (
      <div className="container mx-auto py-8">
        <Card>
          <CardHeader>
            <CardTitle>Task Not Found</CardTitle>
          </CardHeader>
          <CardContent>
            <p>The requested task could not be found.</p>
            <Button asChild className="mt-4">
              <Link href="/dashboard">Back to Dashboard</Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const handleDelete = async () => {
    if (!task) return;

    if (!confirm(`Are you sure you want to delete "${task.title}"?`)) {
      return;
    }

    try {
      await deleteTask(id as string);
      toast({
        title: 'Success',
        description: 'Task deleted successfully.',
      });
      router.push('/dashboard');
      router.refresh();
    } catch (error) {
      console.error('Failed to delete task:', error);
      toast({
        title: 'Error',
        description: 'Failed to delete task. Please try again.',
        variant: 'destructive',
      });
    }
  };

  return (
    <AuthGuard requireAuth={true}>
      <div className="container mx-auto py-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <div>
              <CardTitle>Edit Task</CardTitle>
              <CardDescription>Modify the details of your task</CardDescription>
            </div>
          </CardHeader>
          <CardContent>
            <TaskForm
              defaultValues={task ? {
                title: task.title,
                description: task.description || '',
                dueDate: task.due_date || undefined,
              } : {}}
              onSubmit={handleSubmit}
              onCancel={() => router.push(`/tasks/${id}`)}
              isSubmitting={isSubmitting}
            />
            <div className="mt-4">
              <Button
                variant="destructive"
                onClick={handleDelete}
                className="mt-4"
              >
                Delete Task
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </AuthGuard>
  );
}