/**
 * NGO Verification Queue — admin workflow for approving/rejecting NGO registrations.
 *
 * Per Section C: state machine PENDING → APPROVED/REJECTED.
 * Shows pending NGOs with their submitted verification documents.
 * Admin provides a reason (required) and chooses status.
 */

import { useState } from 'react';
import { CheckCircle, XCircle, FileText } from 'lucide-react';
import { usePendingNGOs, useVerifyNGO } from '../../hooks/useAdmin';
import type { NGO } from '../../types/api';

export function NGOVerificationQueue() {
  const { data: pendingNGOs, isLoading } = usePendingNGOs();
  const verifyMutation = useVerifyNGO();

  const [selectedNGO, setSelectedNGO] = useState<NGO | null>(null);
  const [reason, setReason] = useState('');

  const handleVerify = async (status: 'APPROVED' | 'REJECTED') => {
    if (!selectedNGO || !reason.trim()) {
      alert('Please provide a reason for your decision.');
      return;
    }

    try {
      await verifyMutation.mutateAsync({
        ngoId: selectedNGO.id,
        request: { status, reason: reason.trim() },
      });
      alert(`NGO ${status.toLowerCase()} successfully.`);
      setSelectedNGO(null);
      setReason('');
    } catch (error: any) {
      alert(`Failed to verify NGO: ${error.response?.data?.error?.message || error.message}`);
    }
  };

  if (isLoading) {
    return <div className="p-6">Loading pending NGOs...</div>;
  }

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">NGO Verification Queue</h1>

      {!pendingNGOs || pendingNGOs.length === 0 ? (
        <div className="bg-white p-8 rounded-lg shadow text-center text-gray-500">
          No pending NGO verifications.
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* NGO List */}
          <div className="space-y-4">
            <h2 className="text-xl font-semibold">Pending Verifications ({pendingNGOs.length})</h2>
            {pendingNGOs.map((ngo) => (
              <div
                key={ngo.id}
                className={`p-4 border rounded-lg cursor-pointer transition ${
                  selectedNGO?.id === ngo.id
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 bg-white hover:border-gray-400'
                }`}
                onClick={() => setSelectedNGO(ngo)}
              >
                <h3 className="font-semibold text-lg">{ngo.organisation_name}</h3>
                <p className="text-sm text-gray-600">{ngo.address}</p>
                <div className="mt-2 flex gap-4 text-sm text-gray-700">
                  <span>Capacity: {ngo.storage_capacity_kg} kg</span>
                  <span>Available: {ngo.available_capacity_kg} kg</span>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  Registered: {new Date(ngo.created_at).toLocaleString()}
                </p>
              </div>
            ))}
          </div>

          {/* Verification Panel */}
          <div className="bg-white p-6 rounded-lg shadow border border-gray-200 sticky top-6">
            {!selectedNGO ? (
              <div className="text-center text-gray-500 py-12">
                Select an NGO from the list to review.
              </div>
            ) : (
              <>
                <h2 className="text-2xl font-bold mb-4">{selectedNGO.organisation_name}</h2>

                <div className="space-y-3 mb-6">
                  <DetailRow label="Address" value={selectedNGO.address} />
                  <DetailRow label="Storage Capacity" value={`${selectedNGO.storage_capacity_kg} kg`} />
                  <DetailRow label="Available Capacity" value={`${selectedNGO.available_capacity_kg} kg`} />
                  <DetailRow
                    label="Registered"
                    value={new Date(selectedNGO.created_at).toLocaleString()}
                  />
                </div>

                {/* Verification Documents Section */}
                <div className="mb-6">
                  <h3 className="font-semibold mb-2 flex items-center gap-2">
                    <FileText size={18} />
                    Verification Documents
                  </h3>
                  <p className="text-sm text-gray-600">
                    Check documents via Person 3's NGO module or external links.
                  </p>
                  {/* TODO: fetch and render ngo_verification_documents if Person 1/3 provide endpoint */}
                </div>

                {/* Decision Form */}
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">
                      Reason (required) <span className="text-red-500">*</span>
                    </label>
                    <textarea
                      className="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      rows={4}
                      placeholder="E.g., 'Registration certificate verified. FSSAI Alliance membership confirmed.'"
                      value={reason}
                      onChange={(e) => setReason(e.target.value)}
                    />
                  </div>

                  <div className="flex gap-4">
                    <button
                      className="flex-1 bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700 transition flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                      onClick={() => handleVerify('APPROVED')}
                      disabled={!reason.trim() || verifyMutation.isPending}
                    >
                      <CheckCircle size={20} />
                      Approve
                    </button>
                    <button
                      className="flex-1 bg-red-600 text-white py-3 rounded-lg font-semibold hover:bg-red-700 transition flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                      onClick={() => handleVerify('REJECTED')}
                      disabled={!reason.trim() || verifyMutation.isPending}
                    >
                      <XCircle size={20} />
                      Reject
                    </button>
                  </div>

                  {verifyMutation.isPending && (
                    <p className="text-center text-sm text-gray-600">Processing...</p>
                  )}
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function DetailRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between text-sm">
      <span className="text-gray-600">{label}:</span>
      <span className="font-medium">{value}</span>
    </div>
  );
}
