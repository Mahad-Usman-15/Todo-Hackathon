'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function CalendarPage() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to dashboard since calendar view is not implemented yet
    router.push('/dashboard');
  }, [router]);

  return null; // Render nothing since we're redirecting
}