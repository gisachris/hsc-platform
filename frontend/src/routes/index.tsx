import { createBrowserRouter, Navigate } from 'react-router-dom';
import PublicLayout from '../layouts/PublicLayout';
import AuthLayout from '../layouts/AuthLayout';
import DashboardLayout from '../layouts/DashboardLayout';
import HomePage from '../pages/HomePage';
import LoginPage from '../pages/LoginPage';
import DashboardHome from '../pages/DashboardHome';
import EventsPage from '../pages/EventsPage';
import OrganizationsPage from '../pages/OrganizationsPage';
import SettingsPage from '../pages/SettingsPage';
import NotFoundPage from '../pages/NotFoundPage';
import ProtectedRoute from '../components/ProtectedRoute';

export const router = createBrowserRouter([
  // Public Routes
  {
    path: '/',
    element: <PublicLayout />,
    children: [
      { index: true, element: <HomePage /> },
    ],
  },
  // Auth Routes
  {
    path: '/auth',
    element: <AuthLayout />,
    children: [
      { path: 'login', element: <LoginPage /> },
      { path: '', element: <Navigate to="/auth/login" replace /> },
    ],
  },
  // Protected Admin Routes
  {
    path: '/dashboard',
    element: (
      <ProtectedRoute>
        <DashboardLayout />
      </ProtectedRoute>
    ),
    children: [
      { index: true, element: <DashboardHome /> },
      { path: 'events', element: <EventsPage /> },
      { path: 'organizations', element: <OrganizationsPage /> },
      { path: 'settings', element: <SettingsPage /> },
    ],
  },
  // 404 Route
  {
    path: '*',
    element: <NotFoundPage />,
  },
]);

export default router;
