import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './pages/Login';
import Register from './pages/Register';
import CitizenDashboard from './pages/CitizenDashboard';
import OfficerDashboard from './pages/OfficerDashboard';
import AdminDashboard from './pages/AdminDashboard';
import ComplaintForm from './pages/ComplaintForm';
import Sidebar from './components/Sidebar';
import './App.css';

function AppContent() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading...</div>
      </div>
    );
  }

  const ProtectedRoute = ({ children, allowedRoles = [] }) => {
    if (!user) {
      return <Navigate to="/login" replace />;
    }

    // For now, allow all authenticated users
    // In a real app, you'd check the user's role from the JWT
    return children;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {user && <Sidebar />}
      <div className={user ? 'ml-64' : ''}>
        <Routes>
          <Route path="/login" element={!user ? <Login /> : <Navigate to="/dashboard" replace />} />
          <Route path="/register" element={!user ? <Register /> : <Navigate to="/dashboard" replace />} />
          <Route path="/complaint-form" element={
            <ProtectedRoute allowedRoles={['citizen']}>
              <ComplaintForm />
            </ProtectedRoute>
          } />
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <CitizenDashboard />
            </ProtectedRoute>
          } />
          <Route path="/officer-dashboard" element={
            <ProtectedRoute allowedRoles={['officer']}>
              <OfficerDashboard />
            </ProtectedRoute>
          } />
          <Route path="/admin-dashboard" element={
            <ProtectedRoute allowedRoles={['admin']}>
              <AdminDashboard />
            </ProtectedRoute>
          } />
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </div>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;