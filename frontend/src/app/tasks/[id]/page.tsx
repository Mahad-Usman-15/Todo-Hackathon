'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import TaskStatusIndicator from '@/components/task/task-status-indicator';
import { getTaskById, deleteTask, toggleTaskCompletion } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';
import { Task } from '@/types/task';
import Link from 'next/link';

export default function TaskDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const { toast } = useToast();
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const fetchTask = async () => {
      try {
        if (typeof id === 'string') {
          const response = await getTaskById(id);

          if (response.success && response.data) {
            setTask(response.data);
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
      } finally {
        setLoading(false);
      }
    };

    fetchTask();
  }, [id, toast]);

  const handleDelete = async () => {
    if (!task) return;

    if (!confirm(`Are you sure you want to delete "${task.title}"?`)) {
      return;
    }

    setDeleting(true);
    try {
      await deleteTask(String(task.id));
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
    } finally {
      setDeleting(false);
    }
  };

  const handleToggleComplete = async () => {
    if (!task) return;

    try {
      await toggleTaskCompletion(String(task.id), !task.completed);
      setTask(prev => prev ? { ...prev, completed: !prev.completed } : null);
      toast({
        title: 'Success',
        description: `Task ${task.completed ? 'marked as incomplete' : 'marked as complete'}.`,
      });
    } catch (error) {
      console.error('Failed to update task:', error);
      toast({
        title: 'Error',
        description: 'Failed to update task status. Please try again.',
        variant: 'destructive',
      });
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

  return (
    <div className="container mx-auto py-8">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <div>
            <CardTitle className="flex items-center gap-2">
              {task.title}
              <TaskStatusIndicator task={task} />
            </CardTitle>
            <CardDescription>Task details</CardDescription>
          </div>
          <Badge variant={task.completed ? 'default' : 'secondary'}>
            {task.completed ? 'Completed' : 'Pending'}
          </Badge>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {task.description && (
              <div>
                <h3 className="font-medium mb-1">Description</h3>
                <p className="text-sm text-muted-foreground">{task.description}</p>
              </div>
            )}

            <div className="flex flex-wrap gap-4 pt-4">
              <Button onClick={handleToggleComplete}>
                {task.completed ? 'Mark as Incomplete' : 'Mark as Complete'}
              </Button>

              <Button variant="outline" asChild>
                <Link href={`/tasks/${String(task.id)}/edit`}>Edit Task</Link>
              </Button>

              <Button
                variant="destructive"
                onClick={handleDelete}
                disabled={deleting}
              >
                {deleting ? 'Deleting...' : 'Delete Task'}
              </Button>

              <Button variant="outline" asChild>
                <Link href="/dashboard">Back to Dashboard</Link>
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}