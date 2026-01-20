import { toast as sonnerToast } from "sonner";

// Wrapper to maintain the same API as the original toast hook but use Sonner
const toast = ({
  title,
  description,
  variant,
  ...rest
}: {
  title?: string;
  description?: string;
  variant?: "default" | "destructive";
} & Omit<Parameters<typeof sonnerToast>[1], "className">) => {
  const toastOptions = {
    ...rest,
    className: variant === "destructive" ? "bg-destructive text-destructive-foreground" : "",
  };

  if (title && description) {
    return sonnerToast(title, { description, ...toastOptions });
  } else if (title) {
    return sonnerToast(title, toastOptions);
  } else {
    return sonnerToast(description || "Notification", toastOptions);
  }
};

// Mock useToast hook to maintain compatibility with existing code
function useToast() {
  return {
    toast,
    toasts: [], // Sonner doesn't maintain a list of toasts in the same way
    dismiss: () => {}, // Sonner handles dismissal internally
  };
}

export { toast, useToast };