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

// FIXED CORS CONFIGURATION - Allow multiple origins
app.use(cors({
  origin: process.env.FRONTEND_URL || "http://localhost:3000",
  credentials: true
}));

app.use(morgan('dev'));

// Health check – must reflect DB and migrations/seeds readiness
app.get('/api/health', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    return res.status(200).json({
      status: "ok",
      database: "connected"
    });
  } catch (err) {
    return res.status(500).json({
      status: "error",
      database: "disconnected"
    });
  }
});


// Routes
app.use('/api/auth', authRoutes);
app.use('/api/tenants', tenantRoutes);
app.use('/api', userRoutes);
app.use('/api/projects', projectRoutes);
app.use('/api', taskRoutes);

app.use(errorHandler);

module.exports = app;
