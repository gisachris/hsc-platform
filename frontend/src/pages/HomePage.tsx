import React from 'react';
import { Link } from 'react-router-dom';
import { Video, Calendar, ShieldCheck, Users, BarChart3, MessageSquare } from 'lucide-react';

export const HomePage: React.FC = () => {
  const features = [
    { name: 'Hybrid Conferences', desc: 'Seamless integration of in-person and digital channels.', icon: Video },
    { name: 'Scheduling Engine', desc: 'Manage multi-track agendas and slot allocations.', icon: Calendar },
    { name: 'Secure Access', desc: 'JWT-driven authentication and fine-grained authorization.', icon: ShieldCheck },
    { name: 'User Directory', desc: 'Manage roles for organizers, speakers, and attendees.', icon: Users },
    { name: 'Interactive Engagement', desc: 'Q&As, live chats, and instant polling integrations.', icon: MessageSquare },
    { name: 'Advanced Analytics', desc: 'Track attendance patterns and feedback in real-time.', icon: BarChart3 },
  ];

  return (
    <div className="space-y-24 py-10">
      {/* Hero Section */}
      <section className="text-center max-w-4xl mx-auto space-y-8">
        <h1 className="text-5xl sm:text-6xl font-extrabold font-heading tracking-tight bg-gradient-to-r from-primary via-indigo-500 to-purple-600 bg-clip-text text-transparent">
          Next-Generation Hybrid Conferences
        </h1>
        <p className="text-lg sm:text-xl text-muted-foreground max-w-2xl mx-auto">
          Manage, schedule, stream, and analyze physical and virtual events under a single, cohesive, production-grade command center.
        </p>
        <div className="flex flex-wrap items-center justify-center gap-4">
          <Link
            to="/auth/login"
            className="px-8 py-3.5 bg-primary text-primary-foreground font-semibold rounded-xl hover:bg-primary/95 transition-all shadow-xl shadow-primary/20 hover:scale-[1.02]"
          >
            Access Platform
          </Link>
          <a
            href="#features"
            className="px-8 py-3.5 bg-secondary text-secondary-foreground font-semibold rounded-xl hover:bg-secondary/80 transition-all border border-border hover:scale-[1.02]"
          >
            Explore Infrastructure
          </a>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="space-y-12">
        <div className="text-center space-y-4">
          <h2 className="text-3xl sm:text-4xl font-bold font-heading">
            Architecture Blueprint
          </h2>
          <p className="text-muted-foreground max-w-xl mx-auto">
            Engineered to support extreme scalability, low latency, and robust event coordination.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feat) => {
            const Icon = feat.icon;
            return (
              <div
                key={feat.name}
                className="bg-card p-6 rounded-2xl border border-border hover:border-primary/35 hover:shadow-lg transition-all duration-300 group"
              >
                <div className="w-12 h-12 rounded-xl bg-primary/10 text-primary flex items-center justify-center mb-6 group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                  <Icon className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-semibold mb-2">{feat.name}</h3>
                <p className="text-muted-foreground text-sm leading-relaxed">{feat.desc}</p>
              </div>
            );
          })}
        </div>
      </section>
    </div>
  );
};
export default HomePage;
