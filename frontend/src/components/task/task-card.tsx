'use client';

import { Task } from '@/types/task';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Badge } from '@/components/ui/badge';
import { Calendar as CalendarIcon, SquarePen as EditIcon, Trash2 as TrashIcon } from 'lucide-react';
import { useState } from 'react';

interface TaskCardProps {
  task: Task;
  onToggle?: (id: string) => void;
  onEdit?: (id: string) => void;
  onDelete?: (id: string) => void;
}

export default function TaskCard({ task, onToggle, onEdit, onDelete }: TaskCardProps) {
  const [isCompleted, setIsCompleted] = useState(task.completed);

  const handleToggle = () => {
    setIsCompleted(!isCompleted);
    if (onToggle) {
      onToggle(String(task.id));
    }
  };

  const formatDate = (date: Date) => {
    return new Date(date).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  return (
    <Card
      className={`transition-all duration-200 ${isCompleted ? 'opacity-70' : ''}`}
      role="article"
      aria-label={`Task: ${task.title}`}
      aria-describedby={`task-${task.id}-description`}
    >
      <CardHeader className="pb-2">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3 flex-1">
            <Checkbox
              checked={isCompleted}
              onCheckedChange={handleToggle}
              className="mt-1"
              id={`task-${task.id}-checkbox`}
              aria-label={`Mark task ${task.title} as ${isCompleted ? 'incomplete' : 'complete'}`}
            />
            <div className="flex-1">
              <CardTitle
                className={`text-lg ${isCompleted ? 'line-through text-muted-foreground' : ''}`}
                id={`task-${task.id}-title`}
              >
                {task.title}
              </CardTitle>
              {task.description && (
                <p
                  className="text-sm text-muted-foreground mt-1"
                  id={`task-${task.id}-description`}
                >
                  {task.description}
                </p>
              )}
            </div>
          </div>
          <div className="flex items-center gap-2 ml-2">
            {task.due_date && (
              <div
                className="flex items-center text-xs text-muted-foreground"
                aria-label={`Due date: ${formatDate(new Date(task.due_date))}`}
              >
                <CalendarIcon className="h-3 w-3 mr-1" aria-hidden="true" />
                {formatDate(new Date(task.due_date))}
              </div>
            )}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onEdit && onEdit(String(task.id))}
              className="h-8 w-8 p-0"
              aria-label={`Edit task ${task.title}`}
            >
              <EditIcon className="h-4 w-4" aria-hidden="true" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onDelete && onDelete(String(task.id))}
              className="h-8 w-8 p-0"
              aria-label={`Delete task ${task.title}`}
            >
              <TrashIcon className="h-4 w-4" aria-hidden="true" />
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent className="pt-0">
        <div className="flex items-center justify-between">
          <div className="flex gap-2">
            <Badge variant={isCompleted ? 'default' : 'outline'}>
              {isCompleted ? 'Completed' : 'Pending'}
            </Badge>
            {task.due_date && new Date(task.due_date) < new Date() && !isCompleted && (
              <Badge variant="destructive">Overdue</Badge>
            )}
          </div>
          <span
            className="text-xs text-muted-foreground"
            aria-label={`Created on ${new Date(task.created_at).toLocaleDateString()}`}
          >
            {new Date(task.created_at).toLocaleDateString()}
          </span>
        </div>
      </CardContent>
    </Card>
  );
}