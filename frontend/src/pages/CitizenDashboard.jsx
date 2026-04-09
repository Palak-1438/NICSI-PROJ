import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

const CitizenDashboard = () => {
  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchComplaints();
  }, []);

  const fetchComplaints = async () => {
    try {
      const data = await api.getComplaints('/me');
      setComplaints(data);
    } catch (error) {
      setError('Failed to load complaints');
    }
    setLoading(false);
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

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Complaints</h1>
          <Link
            to="/complaint-form"
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          >
            Submit New Complaint
          </Link>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {complaints.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-8 text-center">
            <p className="text-gray-600 mb-4">You haven't submitted any complaints yet.</p>
            <Link
              to="/complaint-form"
              className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
            >
              Submit Your First Complaint
            </Link>
          </div>
        ) : (
          <div className="grid gap-6">
            {complaints.map((complaint) => (
              <div key={complaint.id} className="bg-white rounded-lg shadow p-6">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-xl font-semibold text-gray-900">{complaint.title}</h3>
                  <div className="flex space-x-2">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityBadge(complaint.priority)}`}>
                      {complaint.priority.toUpperCase()}
                    </span>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusBadge(complaint.status)}`}>
                      {complaint.status.replace('_', ' ').toUpperCase()}
                    </span>
                  </div>
                </div>

                <p className="text-gray-600 mb-4">{complaint.description}</p>

                <div className="flex justify-between items-center text-sm text-gray-500">
                  <div>
                    <span className="font-medium">Category:</span> {complaint.category}
                    {complaint.location && (
                      <>
                        <span className="mx-2">•</span>
                        <span className="font-medium">Location:</span> {complaint.location}
                      </>
                    )}
                  </div>
                  <div>
                    {new Date(complaint.created_at).toLocaleDateString()}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default CitizenDashboard;