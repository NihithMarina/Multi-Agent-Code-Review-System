# CodeGuardian AI

CodeGuardian AI is an enterprise-grade multi-agent pull request review platform. It automatically ingests GitHub pull requests, analyzes changed files with a LangGraph-orchestrated agent swarm, and returns professional review comments, fix suggestions, and analytics for engineering leadership.

## Core capabilities

- GitHub PR ingestion and optional comment posting
- Seven specialized agents: Security, Performance, Clean Code, Testing, Documentation, Dependency, and Architecture
- Coordinator agent for deduplication, ranking, and comment generation
- JWT authentication, GitHub OAuth integration points, and role-based access control
- RAG support for organization coding standards using Sentence Transformers and FAISS
- Semantic search across prior reviews and AI-generated code fixes
- Review history, analytics dashboards, and a responsive React + Tailwind UI
- Docker Compose deployment and GitHub Actions CI

## Architecture

CodeGuardian AI follows a clean-architecture layout:

- Transport layer: FastAPI routers for auth, reviews, GitHub ingestion, search, analytics, and webhooks
- Application layer: review orchestration, semantic search, fix generation, authentication, analytics, and GitHub services
- Domain layer: SQLAlchemy models, Pydantic schemas, and review-finding abstractions
- AI orchestration: LangGraph pipeline that executes the seven specialist agents before the coordinator consolidates output

## Repository features

- PostgreSQL persistence for users, organizations, repositories, and reviews
- Redis ready for queues, caches, and async workflow coordination
- GitHub webhook and pull-request analysis entry points
- FAISS-backed semantic search over historical reviews and organization standards
- Generated remediation suggestions tied to review findings

## Repo layout

- `backend`: FastAPI, SQLAlchemy, LangGraph, Redis, Postgres, and service layer code
- `frontend`: React, Tailwind CSS, and dashboard views
- `.github/workflows`: CI pipeline

## Local development

1. Create and activate a Python virtual environment.
2. Install backend dependencies from `backend/requirements.txt`.
3. Start PostgreSQL and Redis with Docker Compose.
4. Run the backend with Uvicorn.
5. Install frontend dependencies and run the Vite dev server.

### Backend commands

- Run the API: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` from the `backend` directory.
- Run tests: `python -m pytest -q` from the repository root.
- Build the backend container: `docker build -f backend/Dockerfile .`

### Frontend commands

- Install dependencies: `npm install` from the `frontend` directory.
- Run the dev server: `npm run dev`.
- Build for production: `npm run build`.

## Environment variables

- `DATABASE_URL`
- `REDIS_URL`
- `JWT_SECRET_KEY`
- `GITHUB_CLIENT_ID`
- `GITHUB_CLIENT_SECRET`
- `GITHUB_APP_ID`
- `GITHUB_APP_PRIVATE_KEY`
- `OPENAI_API_KEY`

## Backend

The backend exposes health, authentication, review, GitHub, search, webhook, and analytics endpoints. The review pipeline is built around a LangGraph state machine so the agent flow can be expanded or swapped without changing API handlers.

## Frontend

The frontend is a responsive analytics dashboard for PR review status, review history, and organization-level insights.

## Deployment

- Use `docker compose up --build` to launch PostgreSQL, Redis, the FastAPI backend, and the frontend container.
- Set `APP_ENV=production` in production deployments and apply database migrations before starting the API.

