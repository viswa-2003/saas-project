const fs = require("fs");
const path = require("path");
const pool = require("../src/config/db");

(async () => {
  try {
    console.log("Running migrations...");

    const sql = fs.readFileSync(
  path.join(__dirname, "../db/init/001_schema.sql"),
  "utf8"
);


    await pool.query(sql);
    console.log("Migrations completed successfully.");
    process.exit(0);
  } catch (err) {
    console.error("Migration failed:", err);
    process.exit(1);
  }
})();
