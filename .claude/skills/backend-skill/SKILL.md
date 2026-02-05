---
name: backend-skill
description: Build backend functionality by generating routes, handling requests and responses, and connecting to databases. Use for API development and server-side logic.
---

# Backend Skill – Routes, Requests & Database Integration

## Instructions

1. **Route Generation**
   - Define RESTful or GraphQL endpoints
   - Use clear and consistent naming conventions
   - Group routes logically (e.g., /users, /auth, /products)
   - Apply middleware for authentication, validation, and logging

2. **Request & Response Handling**
   - Parse incoming request bodies (JSON, form-data, etc.)
   - Validate inputs and handle errors gracefully
   - Send structured and meaningful responses
   - Use proper HTTP status codes for each scenario

3. **Database Connection**
   - Establish secure and persistent DB connections
   - Query database using ORM or raw SQL safely
   - Handle transactions and rollback when needed
   - Ensure efficient connection pooling and resource management

4. **Best Practices**
   - Keep controllers thin; delegate business logic to services
   - Use async/await or proper concurrency handling
   - Sanitize inputs to prevent injection attacks
   - Log errors without leaking sensitive info

## Example Structure

```js
// Express route example
const express = require("express");
const router = express.Router();
const { getUsers, createUser } = require("../controllers/userController");

// Routes
router.get("/users", getUsers);
router.post("/users", createUser);

module.exports = router;

// Database connection (example using PostgreSQL)
const { Pool } = require("pg");
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

const query = async (sql, params) => {
  const client = await pool.connect();
  try {
    const res = await client.query(sql, params);
    return res.rows;
  } finally {
    client.release();
  }
};
