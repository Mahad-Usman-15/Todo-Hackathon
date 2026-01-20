'use client';

import { useTask } from '@/hooks/use-task';
import TaskList from '@/components/task/task-list';
import Header from '@/components/layout/header';
import { Button } from '@/components/ui/button';
import { Plus } from 'lucide-react';
import Link from 'next/link';
import { Toaster } from '@/components/ui/sonner';
import { useRouter } from 'next/navigation';
import AuthGuard from '@/components/auth/auth-guard';

export default function DashboardPage() {
  const { tasks, loading, error, toggleTaskCompletion, deleteTask } = useTask();
  const router = useRouter();

  return (
    <AuthGuard requireAuth={true}>
      <div className="flex flex-col min-h-screen">
        <Header />

        <main className="flex-1 container py-6 px-4 md:px-6">
          <div className="flex flex-col space-y-6">
            <div className="flex items-center justify-between">
              <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
              <Button asChild>
                <Link href="/tasks/create">
                  <Plus className="mr-2 h-4 w-4" />
                  New Task
                </Link>
              </Button>
            </div>

            {error && (
              <div className="bg-destructive/10 border border-destructive text-destructive p-4 rounded-md">
                {error}
              </div>
            )}

            <TaskList
              tasks={tasks}
              loading={loading}
              onTaskToggle={toggleTaskCompletion}
              onTaskEdit={(id) => router.push(`/tasks/${id}/edit`)}
              onTaskDelete={async (id) => {
                if (confirm('Are you sure you want to delete this task?')) {
                  await deleteTask(id);
                }
              }}
            />
          </div>
        </main>

        <Toaster />
      </div>
    </AuthGuard>
  );
}