'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from './context/AuthContext';

export default function HomePage() {
  const { loading, isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading) {
      if (isAuthenticated) {
        // Redirect to tasks page if user is authenticated
        router.push('/tasks');
      } else {
        // Redirect to login page if user is not authenticated
        router.push('/auth/login');
      }
    }
  }, [isAuthenticated, loading, router]);

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mb-4"></div>
        <p className="text-lg text-gray-600">Redirecting...</p>
      </div>
    </div>
  );
}