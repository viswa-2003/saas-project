const pool = require('../src/config/db');
const bcrypt = require('bcrypt');

(async () => {
  try {
    console.log("Waiting 5 seconds for DB...");
    await new Promise(res => setTimeout(res, 5000));

    console.log('Starting database seeding...');

    // Check if super admin already exists
    const { rows } = await pool.query(
      "SELECT COUNT(*) AS count FROM users WHERE email = 'superadmin@system.com'"
    );

    if (Number(rows[0].count) > 0) {
      console.log('Seed data already present, skipping.');
      process.exit(0);
    }

    // Hash passwords
    const passwordSuper = await bcrypt.hash('Admin@123', 10);
    const passwordTenantAdmin = await bcrypt.hash('Demo@123', 10);
    const passwordUser = await bcrypt.hash('User@123', 10);

    console.log('Creating super admin...');
    await pool.query(
      `INSERT INTO users 
       (id, tenant_id, email, password_hash, full_name, role, is_active, created_at)
       VALUES 
       (gen_random_uuid(), NULL, 'superadmin@system.com', $1, 
        'System Super Admin', 'super_admin', TRUE, NOW())`,
      [passwordSuper]
    );

    console.log('Creating demo tenant...');
    const tenantResult = await pool.query(
      `INSERT INTO tenants 
       (id, name, subdomain, status, subscription_plan, max_users, max_projects, created_at)
       VALUES 
       (gen_random_uuid(), 'Demo Company', 'demo', 'active', 'pro', 25, 15, NOW())
       RETURNING id`
    );
    const tenantId = tenantResult.rows[0].id;

    console.log('Creating tenant admin...');
    const tenantAdminResult = await pool.query(
      `INSERT INTO users 
       (id, tenant_id, email, password_hash, full_name, role, is_active, created_at)
       VALUES 
       (gen_random_uuid(), $1, 'admin@demo.com', $2, 
        'Demo Admin', 'tenant_admin', TRUE, NOW())
       RETURNING id`,
      [tenantId, passwordTenantAdmin]
    );
    const tenantAdminId = tenantAdminResult.rows[0].id;

    console.log('Creating regular users...');
    await pool.query(
      `INSERT INTO users 
       (id, tenant_id, email, password_hash, full_name, role, is_active, created_at)
       VALUES 
       (gen_random_uuid(), $1, 'user1@demo.com', $2, 'User One', 'user', TRUE, NOW()),
       (gen_random_uuid(), $1, 'user2@demo.com', $2, 'User Two', 'user', TRUE, NOW())`,
      [tenantId, passwordUser]
    );

    console.log('Creating projects...');
    const project1 = await pool.query(
      `INSERT INTO projects 
       (id, tenant_id, name, description, status, created_by, created_at)
       VALUES 
       (gen_random_uuid(), $1, 'Project Alpha', 
        'First demo project', 'active', $2, NOW())
       RETURNING id`,
      [tenantId, tenantAdminId]
    );
    const project1Id = project1.rows[0].id;

    const project2 = await pool.query(
      `INSERT INTO projects 
       (id, tenant_id, name, description, status, created_by, created_at)
       VALUES 
       (gen_random_uuid(), $1, 'Project Beta', 
        'Second demo project', 'active', $2, NOW())
       RETURNING id`,
      [tenantId, tenantAdminId]
    );
    const project2Id = project2.rows[0].id;

    console.log('Creating tasks...');
    await pool.query(
      `INSERT INTO tasks 
       (id, project_id, tenant_id, title, description, status, priority, assigned_to, due_date, created_at)
       VALUES 
       (gen_random_uuid(), $1, $2, 
        'Design homepage mockup', 'Create high-fidelity design', 
        'todo', 'high', $3, CURRENT_DATE + INTERVAL '7 days', NOW()),

       (gen_random_uuid(), $1, $2, 
        'Implement login API', 'Build JWT auth endpoints', 
        'in_progress', 'medium', $3, CURRENT_DATE + INTERVAL '10 days', NOW()),

       (gen_random_uuid(), $4, $2, 
        'Fix CORS issues', 'Resolve cross-origin problems', 
        'todo', 'high', $3, CURRENT_DATE + INTERVAL '5 days', NOW())`,
      [project1Id, tenantId, tenantAdminId, project2Id]
    );

    console.log('Seed data inserted successfully!');
    process.exit(0);

  } catch (err) {
    console.error('Seed error:', err);
    process.exit(1);
  }
})();
