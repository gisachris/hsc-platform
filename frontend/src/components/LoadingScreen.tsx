import React from 'react';

export const LoadingScreen: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-background text-foreground space-y-4">
      <div className="relative w-12 h-12">
        <div className="absolute inset-0 rounded-full border-4 border-primary/20"></div>
        <div className="absolute inset-0 rounded-full border-4 border-t-primary animate-spin"></div>
      </div>
      <p className="text-sm font-medium text-muted-foreground animate-pulse">
        Loading conference platform...
      </p>
    </div>
  );
};
export default LoadingScreen;
