import React from 'react';

export const EventsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold font-heading">Event Scheduling</h1>
        <p className="text-muted-foreground text-sm">
          Create, schedule, and configure video meeting integrations.
        </p>
      </div>
      <div className="border-2 border-dashed border-border rounded-2xl h-80 flex flex-col items-center justify-center text-muted-foreground space-y-2">
        <p className="text-lg font-medium">No events configured yet</p>
        <p className="text-sm text-center max-w-sm">
          Future milestones will implement organization-level event listings, schedule builders, and session streams.
        </p>
      </div>
    </div>
  );
};
export default EventsPage;
