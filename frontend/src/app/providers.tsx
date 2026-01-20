'use client';

import { createContext, useContext, ReactNode } from 'react';
import {  signIn, signOut, signUp, useSession, getSession } from '@/lib/auth';
import { User } from '@/types/auth';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<{ success: boolean; user?: User | null; error?: string }>;
  logout: () => Promise<{ success: boolean; error?: string }>;
  register: (email: string, password: string, name?: string) => Promise<{ success: boolean; user?: User | null; error?: string }>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const { data: session, isPending } = useSession();
  const betterUser = session?.user;
  const loading = isPending; // Use the isPending state from the hook
  const isAuthenticated = !!betterUser;

  // Wrap the Better Auth functions to match the expected return types
  const wrappedLogin = async (email: string, password: string) => {
    try {
      const result = await signIn?.email({
        email,
        password,
        callbackURL: '/dashboard',
      });

      // Check if login was successful based on result structure
      if (result && !('error' in result)) {
        // Get updated session after login
        const updatedSession = await getSession();
        // Check if session is valid and contains user data
        if (updatedSession && !('error' in updatedSession) && updatedSession) {
          // Safe check to access user property
          const sessionWithUser = updatedSession as any;
          if (sessionWithUser && sessionWithUser.user) {
            const user = sessionWithUser.user;
            return { success: true, user: user as User };
          }
        }
        return { success: false, error: 'Login failed - could not retrieve user session' };
      } else {
        // Handle error case
        return { success: false, error: 'Login failed' };
      }
    } catch (_error) {
      return { success: false, error: 'Login failed' };
    }
  };

  const wrappedLogout = async () => {
    try {
      await signOut?.();
      return { success: true };
    } catch (_error) {
      return { success: false, error: 'Logout failed' };
    }
  };

  const wrappedRegister = async (email: string, password: string, name?: string) => {
    try {
      const result = await signUp?.email({
        email,
        password,
        name: name || email.split('@')[0],
      });

      // Check if registration was successful based on result structure
      if (result && !('error' in result)) {
        // Get updated session after registration
        const updatedSession = await getSession();
        // Check if session is valid and contains user data
        if (updatedSession && !('error' in updatedSession) && updatedSession) {
          // Safe check to access user property
          const sessionWithUser = updatedSession as any;
          if (sessionWithUser && sessionWithUser.user) {
            const user = sessionWithUser.user;
            return { success: true, user: user as User };
          }
        }
        return { success: false, error: 'Registration failed - could not retrieve user session' };
      } else {
        // Handle error case
        return { success: false, error: 'Registration failed' };
      }
    } catch (_error) {
      return { success: false, error: 'Registration failed' };
    }
  };

  const contextValue: AuthContextType = {
    user: betterUser as User | null,
    loading,
    isAuthenticated,
    login: wrappedLogin,
    logout: wrappedLogout,
    register: wrappedRegister
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
}

export function useCustomAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useCustomAuth must be used within an AuthProvider');
  }
  return context;
}