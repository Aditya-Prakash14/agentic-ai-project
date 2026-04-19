import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import JobDetail from './pages/JobDetail';
import Search from './pages/Search';
import Settings from './pages/Settings';
import { Menu, X } from 'lucide-react';
import './index.css';

function App() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <Link to="/" className="text-2xl font-bold text-blue-600">🤖 Job Bot</Link>
              <div className="hidden md:flex items-center space-x-8">
                <Link to="/" className="text-gray-700 hover:text-blue-600">Dashboard</Link>
                <Link to="/search" className="text-gray-700 hover:text-blue-600">New Search</Link>
                <Link to="/settings" className="text-gray-700 hover:text-blue-600">Settings</Link>
              </div>
              <button className="md:hidden" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
                {mobileMenuOpen ? <X /> : <Menu />}
              </button>
            </div>
            {mobileMenuOpen && (
              <div className="md:hidden pb-4 space-y-2">
                <Link to="/" className="block text-gray-700 py-2">Dashboard</Link>
                <Link to="/search" className="block text-gray-700 py-2">New Search</Link>
                <Link to="/settings" className="block text-gray-700 py-2">Settings</Link>
              </div>
            )}
          </div>
        </nav>
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/job/:jobId" element={<JobDetail />} />
            <Route path="/search" element={<Search />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
        <footer className="bg-gray-100 mt-12 py-8">
          <div className="max-w-7xl mx-auto px-4 text-center text-gray-600 text-sm">
            <p>Job Bot v1.0 - AI-powered job search automation</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
