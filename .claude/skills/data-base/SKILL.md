---
name: database-skill
description: Design and manage databases by creating tables, writing migrations, and optimizing schema. Use for building reliable and scalable data storage.
---

# Database Skill – Tables, Migrations & Schema Design

## Instructions

1. **Schema Design**
   - Define entities and relationships clearly
   - Choose appropriate data types for each column
   - Enforce constraints (primary key, foreign key, unique, not null)
   - Normalize tables to reduce redundancy
   - Consider indexing for frequently queried columns

2. **Table Creation**
   - Write CREATE TABLE statements correctly
   - Include meaningful column names and defaults
   - Apply constraints and indexes as per design
   - Ensure compatibility with target DB (Postgres, MySQL, SQLite, etc.)

3. **Migrations**
   - Write versioned migration scripts
   - Support safe schema evolution without data loss
   - Include rollback mechanisms
   - Automate migrations for dev, staging, and production

4. **Data Integrity & Best Practices**
   - Use transactions for critical operations
   - Validate relationships and constraints
   - Avoid unnecessary denormalization unless performance requires it
   - Document schema changes clearly

## Example Structure

```sql
-- Users table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  email VARCHAR(100) NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Migration example
ALTER TABLE users ADD COLUMN last_login TIMESTAMP;
