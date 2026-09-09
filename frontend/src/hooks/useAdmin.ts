/**
 * TanStack Query hooks for admin operations.
 *
 * Includes NGO verification workflow mutations.
 */

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import type { SuccessEnvelope, NGO, NGOVerificationResult, VerifyNGORequest } from '../types/api';

export function usePendingNGOs() {
  return useQuery({
    queryKey: ['admin', 'ngos', 'pending'],
    queryFn: async () => {
      // This endpoint would be provided by Person 3's NGO module
      // For now, stub with /api/v1/ngos?verification_status=PENDING
      const { data } = await apiClient.get<SuccessEnvelope<NGO[]>>(
        '/api/v1/ngos?verification_status=PENDING'
      );
      return data.data;
    },
    refetchInterval: 15000, // refresh pending queue every 15s
  });
}

export function useVerifyNGO() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ ngoId, request }: { ngoId: string; request: VerifyNGORequest }) => {
      const { data } = await apiClient.patch<SuccessEnvelope<NGOVerificationResult>>(
        `/api/v1/admin/ngos/${ngoId}/verify`,
        request
      );
      return data.data;
    },
    onSuccess: () => {
      // Invalidate pending NGOs query to refresh the table
      queryClient.invalidateQueries({ queryKey: ['admin', 'ngos', 'pending'] });
      // Invalidate overview analytics (registered_ngos count may have changed if this was first approval)
      queryClient.invalidateQueries({ queryKey: ['analytics', 'overview'] });
    },
  });
}
