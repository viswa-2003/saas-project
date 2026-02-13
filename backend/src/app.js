const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const authRoutes = require('./routes/authRoutes');
const tenantRoutes = require('./routes/tenantRoutes');
const userRoutes = require('./routes/userRoutes');
const projectRoutes = require('./routes/projectRoutes');
const taskRoutes = require('./routes/taskRoutes');
const errorHandler = require('./middleware/errorHandler');
const pool = require('./config/db');

const app = express();

app.use(express.json());

// CORS Configuration
const allowedOrigins = [
  "http://localhost:3000",
  "https://saas-project-frontend-qa4w.onrender.com"
];

app.use(cors({
  origin: function (origin, callback) {
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error("Not allowed by CORS"));
    }
  },
  credentials: true
}));

app.use(morgan('dev'));

// ✅ 1. ROOT ROUTE
app.get('/', (req, res) => {
  res.status(200).json({
    success: true,
    message: 'SaaS Project Backend API',
    version: '1.0.0',
    status: 'running',
    environment: process.env.NODE_ENV || 'development',
    timestamp: new Date().toISOString(),
    endpoints: {
      health: '/api/health',
      auth: {
        register: 'POST /api/auth/register-tenant',
        login: 'POST /api/auth/login',
        me: 'GET /api/auth/me',
        logout: 'POST /api/auth/logout'
      }
    }
  });
});

// ✅ 2. API BASE ROUTE
app.get('/api', (req, res) => {
  res.status(200).json({
    success: true,
    message: 'API is working',
    routes: ['/auth', '/tenants', '/users', '/projects', '/tasks']
  });
});

// Health check
app.get('/api/health', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    return res.status(200).json({
      success: true,
      status: "ok",
      database: "connected",
      timestamp: new Date().toISOString()
    });
  } catch (err) {
    console.error('Database health check failed:', err.message);
    return res.status(500).json({
      success: false,
      status: "error",
      database: "disconnected",
      error: err.message
    });
  }
});

// ✅ 3. AUTH TEST ROUTE
app.get('/api/auth/test', (req, res) => {
  res.status(200).json({
    success: true,
    message: 'Auth routes are mounted and working!',
    availableRoutes: [
      'POST /api/auth/register-tenant',
      'POST /api/auth/login',
      'GET /api/auth/me',
      'POST /api/auth/logout'
    ]
  });
});

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/tenants', tenantRoutes);
app.use('/api', userRoutes);
app.use('/api/projects', projectRoutes);
app.use('/api', taskRoutes);

// ✅ 4. FIXED 404 HANDLER - NO WILDCARD '*'
app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: `Route not found: ${req.method} ${req.originalUrl}`,
    availableEndpoints: {
      root: 'GET /',
      health: 'GET /api/health',
      auth_test: 'GET /api/auth/test',
      register: 'POST /api/auth/register-tenant',
      login: 'POST /api/auth/login',
      me: 'GET /api/auth/me',
      logout: 'POST /api/auth/logout'
    }
  });
});

app.use(errorHandler);

module.exports = app;