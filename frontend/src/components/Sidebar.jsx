import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  Home,
  FileText,
  Users,
  Settings,
  LogOut,
  UserCheck,
  BarChart3
} from 'lucide-react';

const Sidebar = () => {
  const { logout, getUserRole } = useAuth();
  const location = useLocation();
  const userRole = getUserRole();

  const menuItems = [
    {
      name: 'Dashboard',
      path: '/dashboard',
      icon: Home,
      roles: ['citizen']
    },
    {
      name: 'Submit Complaint',
      path: '/complaint-form',
      icon: FileText,
      roles: ['citizen']
    },
    {
      name: 'Officer Dashboard',
      path: '/officer-dashboard',
      icon: UserCheck,
      roles: ['officer']
    },
    {
      name: 'Admin Dashboard',
      path: '/admin-dashboard',
      icon: BarChart3,
      roles: ['admin']
    }
  ];

  const filteredMenuItems = menuItems.filter(item =>
    item.roles.includes(userRole)
  );

  return (
    <div className="fixed left-0 top-0 h-full w-64 bg-white shadow-lg border-r border-gray-200">
      <div className="p-6 border-b border-gray-200">
        <h1 className="text-2xl font-bold text-gray-800">Complaint System</h1>
        <p className="text-sm text-gray-600 mt-1 capitalize">{userRole} Portal</p>
      </div>

      <nav className="p-4">
        <ul className="space-y-2">
          {filteredMenuItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;

            return (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={`flex items-center px-4 py-3 rounded-lg transition-colors ${
                    isActive
                      ? 'bg-blue-50 text-blue-700 border-r-4 border-blue-700'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <Icon className="w-5 h-5 mr-3" />
                  {item.name}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200">
        <button
          onClick={logout}
          className="flex items-center w-full px-4 py-3 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <LogOut className="w-5 h-5 mr-3" />
          Logout
        </button>
      </div>
    </div>
  );
};

export default Sidebar;