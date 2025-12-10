from datetime import datetime
from app.db.session import async_session
from app.models import Task
import asyncio
import uuid


SEED_TASKS = [
    {
        "title": "Math Practice: Linear Equations",
        "description": "Solve basic linear equations to reinforce foundational algebra concepts.",
        "category": "Homework Set 01",
        "difficulty": "Easy",
        "tags": ["math", "algebra", "practice"],
        "points": 100,
    },
    {
        "title": "Reading Comprehension: Short Passage",
        "description": "Read a short passage and answer analytical questions to develop comprehension skills.",
        "category": "Homework Set 01",
        "difficulty": "Medium",
        "tags": ["reading", "analysis", "language"],
        "points": 200,
    },
    {
        "title": "Science Inquiry: Experimental Reasoning",
        "description": "Analyze an experiment scenario and apply scientific reasoning to reach conclusions.",
        "category": "Homework Set 01",
        "difficulty": "Hard",
        "tags": ["science", "critical-thinking", "problem-solving"],
        "points": 300,
    },
]

async def seed_tasks():
    async with async_session() as session:
        existing = await session.execute("SELECT COUNT(*) FROM task")
        count = existing.scalar()
        if count == 0:
            print("Inserting default CTF tasks...")
            for t in SEED_TASKS:
                task = Task(
                    task_id=uuid.uuid4(),
                    title=t["title"],
                    description=t["description"],
                    category=t["category"],
                    difficulty=t["difficulty"],
                    tags=t["tags"],
                    points=t["points"],
                    created_at=datetime.utcnow(),
                )
                session.add(task)
            await session.commit()
            print("Done.")
        else:
            print("Tasks already exist, skipping.")
            
if __name__ == "__main__":
    asyncio.run(seed_tasks())
