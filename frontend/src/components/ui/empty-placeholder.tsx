import * as React from "react";

import { cn } from "@/lib/utils";

const EmptyPlaceholder = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, children, ...props }, ref) => {
  return (
    <div
      ref={ref}
      className={cn(
        "flex min-h-[400px] flex-col items-center justify-center rounded-md border border-dashed p-8 text-center",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
});
EmptyPlaceholder.displayName = "EmptyPlaceholder";

interface EmptyPlaceholderIconProps extends React.HTMLAttributes<HTMLDivElement> {
  icon?: React.ComponentType<React.SVGProps<SVGSVGElement>>;
}

const EmptyPlaceholderIcon = React.forwardRef<
  HTMLDivElement,
  EmptyPlaceholderIconProps
>(({ className, icon: Icon = null, ...props }, ref) => {
  return (
    <div
      ref={ref}
      className={cn("mb-4 rounded-full bg-muted p-4", className)}
      {...props}
    >
      {Icon && <Icon className="h-10 w-10 text-muted-foreground" />}
    </div>
  );
});
EmptyPlaceholderIcon.displayName = "EmptyPlaceholderIcon";

const EmptyPlaceholderTitle = React.forwardRef<
  HTMLHeadingElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => {
  return (
    <h3
      ref={ref}
      className={cn("mb-1.5 text-lg font-semibold", className)}
      {...props}
    />
  );
});
EmptyPlaceholderTitle.displayName = "EmptyPlaceholderTitle";

const EmptyPlaceholderDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => {
  return (
    <p
      ref={ref}
      className={cn("mb-4 text-sm text-muted-foreground", className)}
      {...props}
    />
  );
});
EmptyPlaceholderDescription.displayName = "EmptyPlaceholderDescription";

export {
  EmptyPlaceholder,
  EmptyPlaceholderIcon,
  EmptyPlaceholderTitle,
  EmptyPlaceholderDescription,
};