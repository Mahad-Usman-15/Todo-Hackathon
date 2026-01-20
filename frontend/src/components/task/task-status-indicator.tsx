import { Task } from '@/types/task';
import { Badge } from '@/components/ui/badge';
import { CheckCircle2, Circle, Clock, AlertCircle } from 'lucide-react';

type TaskStatus = 'completed' | 'pending' | 'overdue';

interface TaskStatusIndicatorProps {
  task?: Task;
  status?: TaskStatus;
  className?: string;
}

export default function TaskStatusIndicator({ task, status, className }: TaskStatusIndicatorProps) {
  // If task is provided, calculate status from task, otherwise use provided status
  let finalStatus: TaskStatus;
  if (task) {
    const isOverdue = task.due_date && new Date(task.due_date) < new Date() && !task.completed;
    const isCompleted = task.completed;

    if (isCompleted) {
      finalStatus = "completed";
    } else if (isOverdue) {
      finalStatus = "overdue";
    } else {
      finalStatus = "pending";
    }
  } else if (status) {
    finalStatus = status;
  } else {
    finalStatus = "pending";
  }

  let variant: "default" | "destructive" | "outline" = "outline";
  let Icon = Circle;
  let text = "Pending";

  if (finalStatus === "completed") {
    variant = "default";
    Icon = CheckCircle2;
    text = "Completed";
  } else if (finalStatus === "overdue") {
    variant = "destructive";
    Icon = AlertCircle;
    text = "Overdue";
  } else {
    variant = "outline";
    Icon = Clock;
    text = "Pending";
  }

  return (
    <Badge variant={variant} className={className}>
      <Icon className="h-3 w-3 mr-1" />
      {text}
    </Badge>
  );
}