import { Calendar as CalendarIcon } from 'lucide-react';
import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="border-t bg-background">
      <div className="container py-6 px-4 md:px-6">
        <div className="flex flex-col items-center justify-between md:flex-row">
          <div className="flex items-center space-x-2">
            <CalendarIcon className="h-6 w-6" />
            <span className="text-xl font-bold">TodoApp</span>
          </div>

          <p className="mt-4 md:mt-0 text-center text-sm text-muted-foreground">
            © {new Date().getFullYear()} TodoApp. All rights reserved.
          </p>

          <div className="mt-4 md:mt-0 flex items-center space-x-4">
            <Link href="/privacy" className="text-sm text-muted-foreground hover:text-foreground">
              Privacy
            </Link>
            <Link href="/terms" className="text-sm text-muted-foreground hover:text-foreground">
              Terms
            </Link>
            <Link href="/support" className="text-sm text-muted-foreground hover:text-foreground">
              Support
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
}