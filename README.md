## Education Practice Platform
Version: 1.0.0
Date: 2025-12-10
Author: GOKU1117
-------------------------------------------
### Overview
-------------------------------------------
Education Practice Platform is a responsive and interactive Capture-The-Flag competition system 
designed for educational challenges. The system includes:

- Frontend: Vue.js 3 (Hacker-style UI)
- Backend: FastAPI (Async + SQLAlchemy)
- Database: PostgreSQL
- Deployment: Docker Compose

Users can register, log in, attempt challenges, and earn cumulative scores. 
An admin interface allows CRUD operations on tasks and real-time monitoring 
of traffic and leaderboard updates.

<img width="1686" height="1023" alt="page (4)" src="https://github.com/user-attachments/assets/8952512a-cc0a-42b6-9d0f-5164b5289d17" />
<img width="1660" height="1024" alt="page (3)" src="https://github.com/user-attachments/assets/89127626-bf63-40d2-847e-75e72eb250bf" />
<img width="1698" height="1023" alt="page (2)" src="https://github.com/user-attachments/assets/051e3c8c-07db-4c81-9704-77c2bcf50b2d" />
<img width="1624" height="1021" alt="page (1)" src="https://github.com/user-attachments/assets/e20a262d-556c-498b-bf76-714fa1bd72f4" />


-----------------------------------------
### Prerequisites
-------------------------------------------
1. Docker Desktop (Windows/Mac/Linux)
2. Docker Compose v2.0+
3. Git (optional for source control)
4. Port availability:
   - 3000 (Frontend)
   - 8000 (Backend)
   - 5432 (PostgreSQL)

-------------------------------------------
### Setup & Installation
-------------------------------------------

###  1️.Clone or copy the project
-------------------------------------------
C:\> git clone https://github.com/your-org/education-practice-platform.git
C:\> cd education-practice-platform

###  2️.Create environment file
-------------------------------------------
##### Copy `.env.example` → `.env`  
##### Edit if needed:
-------------------------------------------
DATABASE_URL=postgresql+asyncpg://ctf:ctfpassword@db:5432/ctfdb
SECRET_KEY=supersecretchangeit
ACCESS_TOKEN_EXPIRE_MINUTES=60

###  3️.Start Docker daemon
-------------------------------------------
Common issue:
> error during connect: this error may indicate that the docker daemon is not running

Solution:
   - Open Docker Desktop manually
   - Wait until "Docker Engine is running" appears
   - Re-run the command below

###  4️.Build and start all containers
-------------------------------------------
C:\ctf> docker-compose up --build

###  5️.Access the system
-------------------------------------------
Frontend UI: http://localhost:3000  
Backend API Docs (Swagger): http://localhost:8000/docs  
PostgreSQL: localhost:5432  
   - user: ctf
   - password: ctfpassword
   - database: ctfdb

-------------------------------------------
###  Database Only Setup (Optional)
-------------------------------------------
If you want to only start PostgreSQL manually:

C:\ctf\db> chmod +x init_db.sh
C:\ctf\db> ./init_db.sh

This script:
- Starts a PostgreSQL container named `ctf_postgres`
- Creates DB: `ctfdb`
- Runs schema `init.sql` automatically

-------------------------------------------
### Default Functionalities
-------------------------------------------

Frontend Features:
- Register/Login page with token auth
- Challenge board (OT network tasks)
- Dashboard with top-10 leaderboard (line chart)
- Admin panel for task upload (CRUD)
- Admin traffic monitoring page

Backend API Highlights:
- Secure password hashing (bcrypt)
- JWT-based token authentication
- Async PostgreSQL operations
- CORS-ready API routes

-------------------------------------------
### Development Commands
-------------------------------------------
####  Local development without Docker
cd backend
bash init_install.sh
source venv/bin/activate
uvicorn app.main:app --reload

####  Frontend development mode
cd frontend
npm install
npm run dev
####  Open http://localhost:5173

-------------------------------------------
### Common Troubleshooting
-------------------------------------------

Problem: Docker daemon not running
- Open Docker Desktop
- Or run in PowerShell (Admin):
  Start-Service docker

Problem: Port conflict (5432, 8000, 3000)
- Edit `docker-compose.yml` ports section
  Example: change "5432:5432" → "55432:5432"

Problem: Database schema missing
- Remove old container and rebuild:
  docker-compose down -v
  docker-compose up --build

Problem: Frontend cannot reach API
- Edit `.env` or set `VUE_APP_API_URL=http://localhost:8000` in frontend

-------------------------------------------
### Data Persistence
-------------------------------------------
Database data is stored in a Docker volume `db_data` (declared in docker-compose.yml).
Even if containers are removed, data will persist until the volume is deleted.

To reset:
docker-compose down -v

-------------------------------------------
### Security
-------------------------------------------
- Passwords are hashed with bcrypt via Passlib
- Tokens use JWT (HS256)
- Sensitive configuration stored in .env (excluded from Git)
- Minimal privilege principle applied in DB schema
- CORS protection ready for future frontend domain restriction

-------------------------------------------
### Future Extensions
-------------------------------------------
- Add email verification & password reset
- Add team-based scoreboard
- Implement admin permission role system
- Integrate real-time WebSocket leaderboard updates
- Store uploaded files in object storage (S3/MinIO)
- Add containerized challenge runners (sandbox per task)

-------------------------------------------
### Clean-up Commands
-------------------------------------------
### # Stop all containers
docker-compose down

### # Remove all containers & DB volumes
docker-compose down -v

-------------------------------------------
### Quick Summary
-------------------------------------------
1. docker compose down -v --remove-orphans
2. docker compose up -d --build
3.docker exec -it ctftemplate-db-1 bash
4.psql -U ctf -d ctfdb

-------------------------------------------
### End of README
-------------------------------------------
