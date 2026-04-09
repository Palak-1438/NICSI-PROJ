import React, { useState, useEffect } from 'react';
import api from '../services/api';

const AdminDashboard = () => {
  const [complaints, setComplaints] = useState([]);
  const [officers, setOfficers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedComplaint, setSelectedComplaint] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [complaintsData] = await Promise.all([
        api.getComplaints(),
        // In a real app, you'd have an endpoint to get officers
      ]);
      setComplaints(complaintsData);
      // Mock officers data - in real app, fetch from API
      setOfficers([
        { id: 'officer1', full_name: 'John Smith' },
        { id: 'officer2', full_name: 'Jane Doe' },
        { id: 'officer3', full_name: 'Bob Johnson' }
      ]);
    } catch (error) {
      setError('Failed to load data');
    }
    setLoading(false);
  };

  const assignOfficer = async (complaintId, officerId) => {
    try {
      await api.assignComplaint(complaintId, officerId);
      fetchData(); // Refresh the list
      setSelectedComplaint(null);
    } catch (error) {
      setError('Failed to assign officer');
    }
  };

  const getStatusBadge = (status) => {
    const statusClasses = {
      pending: 'bg-gray-100 text-gray-800',
      in_progress: 'bg-orange-100 text-orange-800',
      resolved: 'bg-green-100 text-green-800'
    };
    return statusClasses[status] || 'bg-gray-100 text-gray-800';
  };

  const getPriorityBadge = (priority) => {
    const priorityClasses = {
      high: 'bg-red-100 text-red-800',
      medium: 'bg-yellow-100 text-yellow-800',
      low: 'bg-blue-100 text-blue-800'
    };
    return priorityClasses[priority] || 'bg-gray-100 text-gray-800';
  };

  const getStatusStats = () => {
    const stats = {
      pending: 0,
      in_progress: 0,
      resolved: 0
    };
    complaints.forEach(complaint => {
      stats[complaint.status] = (stats[complaint.status] || 0) + 1;
    });
    return stats;
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  const stats = getStatusStats();

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Admin Dashboard</h1>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Pending</h3>
            <p className="text-3xl font-bold text-gray-600">{stats.pending}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">In Progress</h3>
            <p className="text-3xl font-bold text-orange-600">{stats.in_progress}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Resolved</h3>
            <p className="text-3xl font-bold text-green-600">{stats.resolved}</p>
          </div>
        </div>

        {/* Complaints Table */}
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">All Complaints</h2>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Title
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Category
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Priority
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Assigned Officer
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {complaints.map((complaint) => (
                  <tr key={complaint.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{complaint.title}</div>
                      <div className="text-sm text-gray-500">{complaint.description.substring(0, 50)}...</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-sm text-gray-900">{complaint.category}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityBadge(complaint.priority)}`}>
                        {complaint.priority}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusBadge(complaint.status)}`}>
                        {complaint.status.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {complaint.assigned_officer_id ? 'Assigned' : 'Unassigned'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      {!complaint.assigned_officer_id && (
                        <button
                          onClick={() => setSelectedComplaint(complaint)}
                          className="text-blue-600 hover:text-blue-900"
                        >
                          Assign Officer
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Assignment Modal */}
        {selectedComplaint && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
            <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
              <div className="mt-3">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Assign Officer to Complaint
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  <strong>{selectedComplaint.title}</strong>
                </p>

                <div className="space-y-2">
                  {officers.map((officer) => (
                    <button
                      key={officer.id}
                      onClick={() => assignOfficer(selectedComplaint.id, officer.id)}
                      className="w-full text-left px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50"
                    >
                      {officer.full_name}
                    </button>
                  ))}
                </div>

                <div className="flex justify-end mt-4">
                  <button
                    onClick={() => setSelectedComplaint(null)}
                    className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;