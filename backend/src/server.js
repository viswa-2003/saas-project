const app = require('./app');

const port = process.env.PORT || 5000;

const server = app.listen(port, () => {
  console.log('\n=================================');
  console.log('🚀 Server is running!');
  console.log(`📡 Port: ${port}`);
  console.log(`🌍 Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`📍 Base URL: http://localhost:${port}`);
  console.log(`🏠 Root: http://localhost:${port}/`);
  console.log(`🔍 Health: http://localhost:${port}/api/health`);
  console.log(`🔐 Auth Test: http://localhost:${port}/api/auth/test`);
  console.log(`📝 Register: POST http://localhost:${port}/api/auth/register-tenant`);
  console.log(`🔑 Login: POST http://localhost:${port}/api/auth/login`);
  console.log('=================================\n');
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM signal received: closing HTTP server');
  server.close(() => {
    console.log('HTTP server closed');
  });
});

module.exports = server;