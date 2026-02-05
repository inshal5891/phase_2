---
name: auth-skill
description: Implement secure authentication flows including signup, signin, password hashing, JWT tokens, and Better Auth integration. Use for user access control and identity management.
---

# Auth Skill – Secure Authentication & Authorization

## Instructions

1. **User Signup**
   - Validate user input (email, password, username)
   - Hash passwords using bcrypt or argon2
   - Enforce strong password policies
   - Prevent duplicate accounts

2. **User Signin**
   - Verify credentials securely
   - Use constant-time comparisons
   - Return standardized auth responses
   - Avoid revealing whether user or password was incorrect

3. **Password Security**
   - Never store plain-text passwords
   - Use salted hashing (bcrypt / argon2)
   - Support password reset flows with expiring tokens
   - Invalidate sessions after password changes

4. **JWT Token Handling**
   - Issue access and refresh tokens
   - Sign tokens with strong secrets or key pairs
   - Set proper expiration times
   - Validate tokens on every protected request
   - Rotate and revoke tokens when required

5. **Better Auth Integration**
   - Configure Better Auth providers correctly
   - Handle callbacks and redirects securely
   - Store provider identifiers safely
   - Normalize user profiles across auth methods

6. **Authorization**
   - Implement role-based or permission-based access
   - Protect routes and APIs
   - Enforce least-privilege principles

## Security Best Practices
- Never log passwords, secrets, or raw tokens
- Protect against CSRF, XSS, and replay attacks
- Use HTTPS-only and secure cookies when applicable
- Separate auth logic from business logic
- Fail securely with minimal error disclosure

## Example Structure

```ts
// Signup
const hashedPassword = await bcrypt.hash(password, 12);

// JWT
const accessToken = jwt.sign(
  { userId, role },
  process.env.JWT_SECRET,
  { expiresIn: "15m" }
);

// Token validation
jwt.verify(token, process.env.JWT_SECRET);
