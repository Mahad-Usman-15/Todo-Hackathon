'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';
import { authUtils } from '@/lib/auth';
import { User } from '@/types/auth';

export function useAuthHook() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const checkAuthStatus = async () => {
      setLoading(true);
      const authenticated = await authUtils.isAuthenticated();
      setIsAuthenticated(authenticated);

      if (authenticated) {
        const currentUser = await authUtils.getCurrentUser();
        setUser(currentUser);
      }

      setLoading(false);
    };

    checkAuthStatus();
  }, []);

  const login = async (email: string, password: string) => {
    setLoading(true);
    try {
      const response = await apiClient.login({ email, password });

      if (response.success && response.data) {
        const userData = await authUtils.getCurrentUser();
        setUser(userData);
        setIsAuthenticated(true);
        return { success: true, user: userData };
      } else {
        return { success: false, error: response.error };
      }
    } catch (_error) {
      return { success: false, error: 'Login failed' };
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    setLoading(true);
    try {
      await authUtils.logout();
      setUser(null);
      setIsAuthenticated(false);
      return { success: true };
    } catch (_error) {
      return { success: false, error: 'Logout failed' };
    } finally {
      setLoading(false);
    }
  };

  const register = async (email: string, password: string, name?: string) => {
    setLoading(true);
    try {
      // In a real implementation, you would call the register API
      // For now, we'll simulate a login after registration
      const response = await apiClient.register({ email, password, name });

      if (response.success && response.data) {
        const userData = await authUtils.getCurrentUser();
        setUser(userData);
        setIsAuthenticated(true);
        return { success: true, user: userData };
      } else {
        return { success: false, error: response.error };
      }
    } catch (_error) {
      return { success: false, error: 'Registration failed' };
    } finally {
      setLoading(false);
    }
  };

  return {
    user,
    loading,
    isAuthenticated,
    login,
    logout,
    register
  };
}