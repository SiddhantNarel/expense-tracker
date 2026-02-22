import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const navItems = [
  { path: '/', label: 'Dashboard', icon: '📊' },
  { path: '/expenses', label: 'Expenses', icon: '💸' },
  { path: '/income', label: 'Income', icon: '💰' },
  { path: '/loans', label: 'Loans', icon: '🤝' },
  { path: '/budgets', label: 'Budgets', icon: '🎯' },
  { path: '/reports', label: 'Reports', icon: '📈' },
  { path: '/settings', label: 'Settings', icon: '⚙️' },
];

export default function Sidebar({ open, onClose }) {
  const { pathname } = useLocation();

  return (
    <>
      {/* Overlay for mobile */}
      {open && (
        <div
          className="fixed inset-0 bg-black/50 z-20 lg:hidden"
          onClick={onClose}
        />
      )}
      <aside
        className={`fixed top-0 left-0 h-full w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 z-30 transform transition-transform duration-300 lg:translate-x-0 ${
          open ? 'translate-x-0' : '-translate-x-full'
        } lg:static lg:h-auto`}
      >
        <div className="p-6 border-b border-gray-200 dark:border-gray-700">
          <h1 className="text-xl font-bold text-blue-600 dark:text-blue-400">💰 ExpenseTracker</h1>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Personal Finance Tool</p>
        </div>
        <nav className="p-4 space-y-1">
          {navItems.map(({ path, label, icon }) => (
            <Link
              key={path}
              to={path}
              onClick={onClose}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors duration-200 ${
                pathname === path
                  ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              <span>{icon}</span>
              {label}
            </Link>
          ))}
        </nav>
      </aside>
    </>
  );
}
