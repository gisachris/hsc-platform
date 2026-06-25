import React from 'react';

export const OrganizationsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold font-heading">Organizations & Teams</h1>
        <p className="text-muted-foreground text-sm">
          Manage partner configurations and branding overrides.
        </p>
      </div>
      <div className="border-2 border-dashed border-border rounded-2xl h-80 flex flex-col items-center justify-center text-muted-foreground space-y-2">
        <p className="text-lg font-medium">No organizations configured</p>
        <p className="text-sm text-center max-w-sm">
          Future milestones will implement creation and configuration of multitenant tenant hierarchies.
        </p>
      </div>
    </div>
  );
};
export default OrganizationsPage;
