'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { UserData, getCurrentUser } from '../../services/tasks';

interface AuthContextType {
  user: UserData | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (userData: UserData) => void;
  logout: () => void;
  checkAuthStatus: () => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<UserData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check auth status on component mount
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async (): Promise<boolean> => {
    setLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      if (token) {
        // Verify token by fetching user data
        const userData = await getCurrentUser();
        setUser(userData);
        setLoading(false);
        return true;
      } else {
        setLoading(false);
        return false;
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      // Clear invalid token if API call fails
      localStorage.removeItem('access_token');
      setUser(null);
      setLoading(false);
      return false;
    }
  };

  const login = (userData: UserData) => {
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
  };

  const value: AuthContextType = {
    user,
    loading,
    isAuthenticated: !!user,
    login,
    logout,
    checkAuthStatus,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}