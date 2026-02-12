// frontend/src/pages/LoginPage.js
import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './LoginPage.css';

const LoginPage = () => {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    email: '',
    password: '',
    tenantSubdomain: ''
  });

  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Pre-fill from registration if available
  useEffect(() => {
    const registeredEmail = localStorage.getItem('registeredEmail');
    const registeredSubdomain = localStorage.getItem('registeredSubdomain');
    
    if (registeredEmail) {
      setFormData(prev => ({
        ...prev,
        email: registeredEmail,
        tenantSubdomain: registeredSubdomain || ''
      }));
      // Clear after use
      localStorage.removeItem('registeredEmail');
      localStorage.removeItem('registeredSubdomain');
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // Make sure we have the required fields
      if (!formData.email || !formData.password) {
        setError('Email and password are required');
        setLoading(false);
        return;
      }

      if (!formData.tenantSubdomain.trim()) {
        setError('Organization subdomain is required');
        setLoading(false);
        return;
      }
      
      console.log('Attempting login with:', { 
        email: formData.email, 
        tenantSubdomain: formData.tenantSubdomain 
      });

      const result = await login(
        formData.email, 
        formData.password, 
        formData.tenantSubdomain
      );

      if (result && result.success) {
        navigate('/dashboard');
      } else {
        setError(result?.error || 'Invalid email or password');
      }
    } catch (err) {
      console.error('Login error:', err);
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleTestCredentials = () => {
    setFormData({
      email: 'admin@demo.com',
      password: 'Demo@123',
      tenantSubdomain: 'demo'
    });
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Sign in to your account
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Or{' '}
          <Link to="/register" className="font-medium text-blue-600 hover:text-blue-500">
            register a new organization
          </Link>
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
              <p className="text-sm text-red-600">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Email address
              </label>
              <input
                type="email"
                required
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                value={formData.email}
                onChange={(e) =>
                  setFormData({ ...formData, email: e.target.value })
                }
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <input
                type="password"
                required
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                value={formData.password}
                onChange={(e) =>
                  setFormData({ ...formData, password: e.target.value })
                }
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Organization Subdomain
              </label>
              <input
                type="text"
                required
                placeholder="your-organization"
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                value={formData.tenantSubdomain}
                onChange={(e) =>
                  setFormData({ ...formData, tenantSubdomain: e.target.value })
                }
              />
              <p className="mt-1 text-xs text-gray-500">
                Enter the subdomain you used during registration
              </p>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {loading ? 'Signing in...' : 'Sign in'}
            </button>
          </form>

          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">
                  Demo credentials
                </span>
              </div>
            </div>

            <div className="mt-6">
              <button
                onClick={handleTestCredentials}
                type="button"
                className="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Use Demo Account
              </button>
              <div className="mt-2 text-xs text-gray-500 text-center">
                <div>Email: admin@demo.com</div>
                <div>Password: Demo@123</div>
                <div>Subdomain: demo</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;