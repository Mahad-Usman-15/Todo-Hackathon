'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { TaskForm } from '@/components/forms/task-form';
import { apiClient } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';
import { CreateTaskData } from '@/types/task';
import AuthGuard from '@/components/auth/auth-guard';

export default function TaskCreationPage() {
  const router = useRouter();
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (taskData: CreateTaskData) => {
    setIsSubmitting(true);
    try {
      await apiClient.createTask(taskData);
      toast({
        title: 'Success',
        description: 'Task created successfully.',
      });
      router.push('/dashboard');
      router.refresh();
    } catch (error) {
      console.error('Failed to create task:', error);
      toast({
        title: 'Error',
        description: 'Failed to create task. Please try again.',
        variant: 'destructive',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <AuthGuard requireAuth={true}>
      <div className="container mx-auto py-8">
        <Card>
          <CardHeader>
            <CardTitle>Create New Task</CardTitle>
            <CardDescription>Add a new task to your dashboard</CardDescription>
          </CardHeader>
          <CardContent>
            <TaskForm
              defaultValues={{}}
              onSubmit={handleSubmit}
              onCancel={() => router.back()}
              isSubmitting={isSubmitting}
            />
          </CardContent>
        </Card>
      </div>
    </AuthGuard>
  );
}