import React from 'react';
import { Link } from 'react-router-dom';

export const NotFoundPage: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-background text-foreground px-6 text-center space-y-6">
      <h1 className="text-9xl font-extrabold font-heading text-primary animate-pulse">404</h1>
      <h2 className="text-3xl font-bold tracking-tight">Page Not Found</h2>
      <p className="text-muted-foreground max-w-md">
        The page you are looking for does not exist, has been removed, or is temporarily unavailable.
      </p>
      <Link
        to="/"
        className="inline-flex items-center justify-center px-6 py-3 bg-primary text-primary-foreground font-medium rounded-lg hover:bg-primary/90 transition-colors shadow-lg shadow-primary/20"
      >
        Go Back Home
      </Link>
    </div>
  );
};
export default NotFoundPage;
