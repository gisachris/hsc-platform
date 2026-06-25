import React from 'react';

export const SettingsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold font-heading">Settings</h1>
        <p className="text-muted-foreground text-sm">
          System wide parameters, Webhook integrations, and JWT parameters.
        </p>
      </div>
      <div className="border-2 border-dashed border-border rounded-2xl h-80 flex flex-col items-center justify-center text-muted-foreground space-y-2">
        <p className="text-lg font-medium">Standard settings config</p>
        <p className="text-sm text-center max-w-sm">
          Parameters relating to video streaming, cloud logging, and transcription parameters.
        </p>
      </div>
    </div>
  );
};
export default SettingsPage;
