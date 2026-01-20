'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { SignupForm } from '@/components/forms/signup-form';
import { register } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';
import AuthGuard from '@/components/auth/auth-guard';

export default function SignupPage() {
  const router = useRouter();
  const { toast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (formData: { email: string; password: string; name: string }) => {
    setIsSubmitting(true);
    try {
      const result = await register(formData);

      if (result.success) {
        toast({
          title: 'Success',
          description: 'Account created successfully!',
        });
        router.push('/dashboard');
        router.refresh();
      } else {
        throw new Error(result.error || 'Registration failed');
      }
    } catch (error) {
      console.error('Registration error:', error);
      toast({
        title: 'Error',
        description: 'Registration failed. Please try again.',
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
      aria-label="Signup form"
    >
      <Card className="w-full max-w-sm" role="form" aria-labelledby="signup-heading">
        <CardHeader className="space-y-1">
          <CardTitle id="signup-heading" className="text-2xl">Create an account</CardTitle>
          <CardDescription>
            Enter your information to create an account
          </CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4">
          <SignupForm onSubmit={handleSubmit} isSubmitting={isSubmitting} />
        </CardContent>
        <CardFooter className="flex flex-col gap-4">
          <div className="text-center text-sm text-muted-foreground">
            Already have an account?{' '}
            <Link
              href="/login"
              className="underline underline-offset-4 hover:text-primary"
              aria-label="Sign in link"
            >
              Sign in
            </Link>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}