import React from 'react';
import { Outlet } from 'react-router-dom';

export const AuthLayout: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4 sm:px-6 lg:px-8 py-12">
      <div className="max-w-md w-full space-y-8 bg-card p-8 rounded-2xl border border-border shadow-xl">
        <div className="text-center">
          <div className="mx-auto h-12 w-12 rounded-xl bg-primary flex items-center justify-center text-primary-foreground font-extrabold text-2xl shadow-lg shadow-primary/20">
            S
          </div>
          <h2 className="mt-6 text-3xl font-bold font-heading text-foreground">
            SHC Platform
          </h2>
          <p className="mt-2 text-sm text-muted-foreground">
            Smart Hybrid Conference Management
          </p>
        </div>
        <Outlet />
      </div>
    </div>
  );
};
export default AuthLayout;
