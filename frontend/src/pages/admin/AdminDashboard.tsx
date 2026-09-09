/**
 * Admin Dashboard — main overview page with real-time analytics.
 *
 * Consumes Person 6's analytics endpoints via TanStack Query.
 * Renders four metric cards: overview, food, logistics, social.
 * Auto-refreshes every 30s via query hooks.
 */

import { Activity, TrendingUp, Truck, Users } from 'lucide-react';
import {
  useAnalyticsOverview,
  useFoodMetrics,
  useLogisticsMetrics,
  useSocialMetrics,
} from '../../hooks/useAnalytics';

export function AdminDashboard() {
  const { data: overview, isLoading: overviewLoading } = useAnalyticsOverview();
  const { data: food, isLoading: foodLoading } = useFoodMetrics();
  const { data: logistics, isLoading: logisticsLoading } = useLogisticsMetrics();
  const { data: social, isLoading: socialLoading } = useSocialMetrics();

  if (overviewLoading || foodLoading || logisticsLoading || socialLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-lg text-gray-600">Loading analytics...</div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">Admin Dashboard</h1>

      {/* System Overview */}
      <section className="mb-8">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Activity size={24} />
          System Overview
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
          <MetricCard label="Total Donations" value={overview?.total_donations ?? 0} />
          <MetricCard label="Active Donations" value={overview?.active_donations ?? 0} />
          <MetricCard label="Active Deliveries" value={overview?.active_deliveries ?? 0} />
          <MetricCard label="Available Drivers" value={overview?.available_drivers ?? 0} />
          <MetricCard label="Registered NGOs" value={overview?.registered_ngos ?? 0} />
          <MetricCard label="Registered Donors" value={overview?.registered_donors ?? 0} />
        </div>
      </section>

      {/* Food Rescue Metrics */}
      <section className="mb-8">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <TrendingUp size={24} />
          Food Rescue Impact
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <MetricCard
            label="Food Rescued (kg)"
            value={food?.kg_diverted?.toFixed(1) ?? '0.0'}
            suffix=" kg"
          />
          <MetricCard
            label="Meals Recovered"
            value={food?.meals_recovered ?? 0}
            description="Estimate: 0.5 kg = 1 meal"
          />
          <MetricCard
            label="Total Food Rescued (kg)"
            value={overview?.total_food_rescued_kg?.toFixed(1) ?? '0.0'}
            suffix=" kg"
          />
        </div>
      </section>

      {/* Logistics Efficiency */}
      <section className="mb-8">
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Truck size={24} />
          Logistics Efficiency
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            label="Delivery Success Rate"
            value={((logistics?.delivery_success_rate ?? 0) * 100).toFixed(0)}
            suffix="%"
          />
          <MetricCard
            label="Avg Matching Time"
            value={logistics?.avg_matching_time_sec?.toFixed(1) ?? '0.0'}
            suffix=" sec"
          />
          <MetricCard
            label="Avg Delivery Time"
            value={logistics?.avg_delivery_time_min?.toFixed(1) ?? '0.0'}
            suffix=" min"
          />
          <MetricCard
            label="Route Distance Saved"
            value={logistics?.route_distance_saved_km?.toFixed(1) ?? '0.0'}
            suffix=" km"
            description="vs. naive nearest-NGO baseline"
          />
        </div>
      </section>

      {/* Social Impact */}
      <section>
        <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
          <Users size={24} />
          Social Impact
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <MetricCard label="Organisations Served" value={social?.organisations_served ?? 0} />
          <MetricCard
            label="Beneficiaries Reached"
            value={social?.beneficiaries_reached ?? 0}
            description="Estimate only — real tracking pending"
          />
        </div>
      </section>
    </div>
  );
}

interface MetricCardProps {
  label: string;
  value: number | string;
  suffix?: string;
  description?: string;
}

function MetricCard({ label, value, suffix = '', description }: MetricCardProps) {
  return (
    <div className="bg-white p-6 rounded-lg shadow border border-gray-200">
      <div className="text-sm text-gray-600 mb-2">{label}</div>
      <div className="text-3xl font-bold text-gray-900">
        {value}
        {suffix}
      </div>
      {description && <div className="text-xs text-gray-500 mt-2">{description}</div>}
    </div>
  );
}
