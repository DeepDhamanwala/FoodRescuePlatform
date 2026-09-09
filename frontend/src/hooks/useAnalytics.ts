/**
 * TanStack Query hooks for analytics endpoints.
 *
 * All endpoints require ADMIN role — backend enforces via require_admin dependency.
 * Frontend consumes these via the admin dashboard.
 */

import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import type {
  SuccessEnvelope,
  AnalyticsOverview,
  FoodMetrics,
  LogisticsMetrics,
  SocialMetrics,
} from '../types/api';

export function useAnalyticsOverview() {
  return useQuery({
    queryKey: ['analytics', 'overview'],
    queryFn: async () => {
      const { data } = await apiClient.get<SuccessEnvelope<AnalyticsOverview>>(
        '/api/v1/analytics/overview'
      );
      return data.data;
    },
    refetchInterval: 30000, // refetch every 30s for near-real-time dashboard
  });
}

export function useFoodMetrics() {
  return useQuery({
    queryKey: ['analytics', 'food'],
    queryFn: async () => {
      const { data } = await apiClient.get<SuccessEnvelope<FoodMetrics>>('/api/v1/analytics/food');
      return data.data;
    },
    refetchInterval: 30000,
  });
}

export function useLogisticsMetrics() {
  return useQuery({
    queryKey: ['analytics', 'logistics'],
    queryFn: async () => {
      const { data } = await apiClient.get<SuccessEnvelope<LogisticsMetrics>>(
        '/api/v1/analytics/logistics'
      );
      return data.data;
    },
    refetchInterval: 30000,
  });
}

export function useSocialMetrics() {
  return useQuery({
    queryKey: ['analytics', 'social'],
    queryFn: async () => {
      const { data } = await apiClient.get<SuccessEnvelope<SocialMetrics>>(
        '/api/v1/analytics/social'
      );
      return data.data;
    },
    refetchInterval: 30000,
  });
}
