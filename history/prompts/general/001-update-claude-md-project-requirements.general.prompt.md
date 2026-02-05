---
id: 001
title: Update CLAUDE.md with project requirements
stage: general
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5
feature: none
branch: master
user: user
command: none
labels: ["configuration", "project-setup", "agent-delegation", "tech-stack"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - CLAUDE.md
tests:
 - none
---

## Prompt

Update the claude.md file based on my project requirements. In this file:

Use Auth Agent for authentication
Use Frontend Agent for frontend development (e.g., Next.js)
Use DB Agent for database design and operations
Use Backend Agent for FastAPI development
Below are my project requirements:

Basic Level Functionality
Objective: Using Claude Code and Spec-Kit Plus transform the console app into a modern multi-user web application with persistent storage.
💡Development Approach: Use the Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code. No manual coding allowed. We will review the process, prompts, and iterations to judge each phase and project.
Requirements
Implement all 5 Basic Level features as a web application
Create RESTful API endpoints
Build responsive frontend interface
Store data in Neon Serverless PostgreSQL database
Authentication – Implement user signup/signin using Better Auth
Technology Stack
Layer: Technology
Frontend: Next.js 16+ (App Router)
Backend: Python FastAPI
ORM: SQLModel
Database: Neon Serverless PostgreSQL
Spec-Driven: Claude Code + Spec-Kit Plus
Authentication: Better Auth

Better Auth can be configured to issue JWT (JSON Web Token) tokens when users log in. These tokens are self-contained credentials that include user information and can be verified by any service that knows the secret key.
How It Works
User logs in on Frontend → Better Auth creates a session and issues a JWT token
Frontend makes API call → Includes the JWT token in the Authorization: Bearer <token> header
Backend receives request → Extracts token from header, verifies signature using shared secret
Backend identifies user → Decodes token to get user ID, email, etc. and matches it with the user ID in the URL
Backend filters data → Returns only tasks belonging to that user

## Response snapshot

Successfully updated CLAUDE.md file with comprehensive project-specific guidelines (589 new lines added):

1. **Project Overview Section** - Added project type, objective, development approach, and complete technology stack table

2. **Specialized Agent Usage (MANDATORY)** - Detailed guidelines for delegating work to four specialized agents:
   - Auth Agent (auth-security-specialist) for authentication/authorization
   - Frontend Agent (nextjs-ui-optimizer) for Next.js development
   - Database Agent (neon-db-manager) for database operations
   - Backend Agent (fastapi-backend-engineer) for FastAPI development

3. **Project Requirements** - Comprehensive requirements for:
   - Basic Level Functionality (5 core features)
   - API Design (RESTful conventions, status codes, validation)
   - Authentication & Authorization (JWT flow details)
   - Database (SQLModel, migrations, data isolation)
   - Frontend (App Router, Server/Client Components)

4. **Agentic Dev Stack Workflow** - Step-by-step workflow for every feature implementation

5. **Technology-Specific Guidelines** - Best practices for Next.js, FastAPI, SQLModel, and Better Auth

6. **Practical Agent Delegation Examples** - Three complete implementation examples

7. **Quality Gates & Validation Checklist** - Comprehensive checklists for security, functionality, data isolation, performance, and code quality

8. **Common Patterns for This Stack** - Code examples for protected endpoints, authenticated API calls, Server Components, and SQLModel relationships

9. **Troubleshooting Guide** - Solutions for common issues (401 errors, data isolation, CORS, performance)

## Outcome

- ✅ Impact: CLAUDE.md now serves as comprehensive guide for multi-user web application development with proper agent delegation and tech stack best practices
- 🧪 Tests: No tests required (configuration file)
- 📁 Files: Modified CLAUDE.md (+589 lines)
- 🔁 Next prompts: Ready to proceed with feature specification (/sp.specify) or constitution setup (/sp.constitution)
- 🧠 Reflection: Successfully integrated project requirements with existing SDD workflow. Agent delegation strategy clearly defined with practical examples and quality gates.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (configuration update)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification phase using updated guidelines
