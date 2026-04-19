import React, { useState } from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import JobDetail from './pages/JobDetail';
import Search from './pages/Search';
import Settings from './pages/Settings';
import { Menu, X } from 'lucide-react';
import './index.css';

function App() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Navigation */}
      <nav className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="text-2xl font-bold text-blue-600">
              🤖 Job Bot
            </Link>
            
            {/* Desktop Menu */}
            <div className="hidden md:flex items-center space-x-8">
              <Link to="/" className="text-gray-700 hover:text-blue-600 font-medium">Dashboard</Link>
              <Link to="/search" className="text-gray-700 hover:text-blue-600 font-medium">Search</Link>
              <Link to="/settings" className="text-gray-700 hover:text-blue-600 font-medium">Settings</Link>
            </div>

            {/* Mobile Menu Button */}
            <button 
              className="md:hidden p-2"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

          {/* Mobile Menu */}
          {mobileMenuOpen && (
            <div className="md:hidden pb-4 space-y-2 border-t border-gray-200 pt-4">
              <Link to="/" className="block text-gray-700 hover:text-blue-600 py-2 font-medium">Dashboard</Link>
              <Link to="/search" className="block text-gray-700 hover:text-blue-600 py-2 font-medium">Search</Link>
              <Link to="/settings" className="block text-gray-700 hover:text-blue-600 py-2 font-medium">Settings</Link>
            </div>
          )}
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/job/:jobId" element={<JobDetail />} />
          <Route path="/search" element={<Search />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>

      {/* Footer */}
      <footer className="bg-gray-100 border-t border-gray-200 mt-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-gray-600 text-sm">
            <p>Job Bot v1.0 - AI-powered job search automation</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
