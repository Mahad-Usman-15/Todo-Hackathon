'use client';

import { useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { useCustomAuth } from '@/app/providers';

interface AuthGuardProps {
  children: ReactNode;
  requireAuth?: boolean; // If true, requires authentication; if false, redirects away if logged in
}

export default function AuthGuard({
  children,
  requireAuth = true
}: AuthGuardProps) {
  const { isAuthenticated, loading } = useCustomAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading) {
      if (requireAuth && !isAuthenticated) {
        // Redirect to login if authentication is required but user is not authenticated
        router.push('/login');
      } else if (!requireAuth && isAuthenticated) {
        // Redirect away if user is logged in but page requires unauthenticated access
        router.push('/dashboard');
      }
    }
  }, [isAuthenticated, loading, requireAuth, router]);

  // Show loading state while checking authentication
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  // If authentication requirement is satisfied, render children
  if ((requireAuth && isAuthenticated) || (!requireAuth && !isAuthenticated)) {
    return <>{children}</>;
  }

  // Otherwise, don't render anything while redirecting
  return null;
}