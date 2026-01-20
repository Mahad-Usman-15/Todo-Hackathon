'use client';

import { Task } from '@/types/task';
import TaskCard from './task-card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { EmptyPlaceholder, EmptyPlaceholderIcon, EmptyPlaceholderTitle, EmptyPlaceholderDescription } from '@/components/ui/empty-placeholder';

interface TaskListProps {
  tasks: Task[];
  onTaskToggle?: (id: string) => void;
  onTaskEdit?: (id: string) => void;
  onTaskDelete?: (id: string) => void;
  loading?: boolean;
}

export default function TaskList({
  tasks,
  onTaskToggle,
  onTaskEdit,
  onTaskDelete,
  loading = false
}: TaskListProps) {
  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, index) => (
          <div
            key={index}
            className="h-24 w-full animate-pulse rounded-md border bg-muted"
          />
        ))}
      </div>
    );
  }

  if (!tasks || tasks.length === 0) {
    return (
      <EmptyPlaceholder>
        <EmptyPlaceholderIcon />
        <EmptyPlaceholderTitle>No tasks yet</EmptyPlaceholderTitle>
        <EmptyPlaceholderDescription>
          Get started by creating a new task.
        </EmptyPlaceholderDescription>
      </EmptyPlaceholder>
    );
  }

  return (
    <ScrollArea className="h-[calc(100vh-200px)] pr-4">
      <div className="space-y-4">
        {tasks.map((task) => (
          <TaskCard
            key={task.id}
            task={task}
            onToggle={onTaskToggle}
            onEdit={onTaskEdit}
            onDelete={onTaskDelete}
          />
        ))}
      </div>
    </ScrollArea>
  );
}