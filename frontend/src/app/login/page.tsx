'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { LoginForm } from '@/components/forms/login-form';
// import { login } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';
import { apiClient } from '@/lib/api';
export default function LoginPage() {
  const router = useRouter();
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (formData: { email: string; password: string }) => {
    setIsSubmitting(true);
    try {
      const result = await apiClient.login(formData);

      if (result.success) {
        toast({
          title: 'Success',
          description: 'Successfully logged in!',
        });
        router.push('/dashboard');
        router.refresh();
      } else {
        throw new Error(result.error || 'Login failed');
      }
    } catch (error) {
      console.error('Login error:', error);
      toast({
        title: 'Error',
        description: 'Invalid email or password. Please try again.',
        variant: 'destructive',
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div
      className="container flex h-screen w-screen flex-col items-center justify-center"
      role="main"
      aria-label="Login form"
    >
      <Card className="w-full max-w-sm" role="form" aria-labelledby="login-heading">
        <CardHeader className="space-y-1">
          <CardTitle id="login-heading" className="text-2xl">Welcome back</CardTitle>
          <CardDescription>
            Enter your email below to sign in to your account
          </CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4">
          <LoginForm onSubmit={handleSubmit} isSubmitting={isSubmitting} />
        </CardContent>
        <CardFooter className="flex flex-col gap-4">
          <div className="text-center text-sm text-muted-foreground">
            Don&apos;t have an account?{' '}
            <Link
              href="/signup"
              className="underline underline-offset-4 hover:text-primary"
              aria-label="Sign up link"
            >
              Sign up
            </Link>
          </div>
          <div className="text-center text-sm text-muted-foreground">
            <Link
              href="/dashboard"
              className="underline underline-offset-4 hover:text-primary"
              aria-label="Continue as guest link"
            >
              Continue as guest
            </Link>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}