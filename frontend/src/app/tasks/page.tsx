'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function TasksPage() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to dashboard since tasks are managed there
    router.push('/dashboard');
  }, [router]);

  return null; // Render nothing since we're redirecting
}