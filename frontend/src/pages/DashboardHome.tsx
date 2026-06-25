import React from 'react';
import { Calendar, Users, Building, Activity } from 'lucide-react';

export const DashboardHome: React.FC = () => {
  const stats = [
    { name: 'Active Conferences', value: '0', change: 'No sessions running', icon: Calendar },
    { name: 'Registrations', value: '0', change: 'Registration closed', icon: Users },
    { name: 'Organizations', value: '0', change: '0 total partners', icon: Building },
    { name: 'System Status', value: '99.9%', change: 'All components online', icon: Activity },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold font-heading">Dashboard Overview</h1>
        <p className="text-muted-foreground text-sm">
          Real-time diagnostics and operations monitoring.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.name} className="bg-card p-6 rounded-2xl border border-border shadow-sm">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  {stat.name}
                </span>
                <div className="w-8 h-8 rounded-lg bg-primary/10 text-primary flex items-center justify-center">
                  <Icon className="w-4 h-4" />
                </div>
              </div>
              <div className="mt-4">
                <span className="text-3xl font-bold font-heading tracking-tight">{stat.value}</span>
                <p className="text-xs text-muted-foreground mt-1.5 font-medium">{stat.change}</p>
              </div>
            </div>
          );
        })}
      </div>

      <div className="bg-card rounded-2xl border border-border p-6 shadow-sm">
        <h2 className="text-lg font-semibold font-heading mb-4">Milestone Foundation Status</h2>
        <div className="space-y-4">
          <div className="flex justify-between items-center py-3 border-b border-border">
            <span className="text-sm font-medium">FastAPI Server Connection</span>
            <span className="text-xs px-2.5 py-1 bg-green-500/10 text-green-500 font-semibold rounded-full">
              Configured
            </span>
          </div>
          <div className="flex justify-between items-center py-3 border-b border-border">
            <span className="text-sm font-medium">SQLAlchemy 2.0 Async Client</span>
            <span className="text-xs px-2.5 py-1 bg-green-500/10 text-green-500 font-semibold rounded-full">
              Configured
            </span>
          </div>
          <div className="flex justify-between items-center py-3 border-b border-border">
            <span className="text-sm font-medium">Alembic Migration Engines</span>
            <span className="text-xs px-2.5 py-1 bg-green-500/10 text-green-500 font-semibold rounded-full">
              Configured
            </span>
          </div>
          <div className="flex justify-between items-center py-3">
            <span className="text-sm font-medium">Standard Response Middlewares</span>
            <span className="text-xs px-2.5 py-1 bg-green-500/10 text-green-500 font-semibold rounded-full">
              Configured
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
export default DashboardHome;
