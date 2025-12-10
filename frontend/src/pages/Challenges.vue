<template>
  <section class="challenges">
    <div class="header">
      <h1>Challenges</h1>
      <p class="lead">
        Welcome to the Education Practice Platform.
        Each lesson provides structured exercises and interactive tasks designed to help students strengthen their understanding of course concepts.
      </p>
    </div>

    <div v-if="loading" class="loading">Loading challenges...</div>

    <div
      v-else-if="challengeGroups.length"
      class="challenge-group"
      v-for="group in challengeGroups"
      :key="group.id"
    >
      <h2 class="group-title">{{ group.title }}</h2>
      <p class="group-desc">{{ group.description }}</p>

      <div class="cards">
        <div class="card" v-for="task in group.tasks" :key="task.task_id">

          <div v-if="task.pwned" class="pwned-badge">PWNED</div>

          <div class="card-header">
            <h3>{{ task.title }}</h3>
            <span
              class="difficulty"
              :class="(task.difficulty || 'Unknown').toLowerCase()"
            >
              {{ task.difficulty || 'Unknown' }}
            </span>
          </div>

          <p class="desc">{{ task.description || "No description provided." }}</p>

          <div class="tags" v-if="task.tags && task.tags.length">
            <span class="tag" v-for="tag in task.tags" :key="tag">{{ tag }}</span>
          </div>

          <div class="actions">
            <button class="btn primary" @click="toggleTask(task.task_id)">Start</button>
            <button class="btn ghost" @click="toggleHint(task.task_id)">View Hint</button>
          </div>

          <transition name="slide">
            <div v-if="openedTask === task.task_id" class="answer-box">
              <label class="label">Answer:</label>

              <input
                v-model="task.answerInput"
                :disabled="task.pwned"
                :class="['answer-input', task.pwned ? 'answer-correct' : '']"
                placeholder="Enter your flag or answer..."
              />

              <button
                class="btn primary submit-btn"
                @click="submitAnswer(task)"
                :disabled="task.pwned"
              >
                Submit
              </button>
            </div>
          </transition>

          <transition name="slide">
            <div v-if="openedHint === task.task_id" class="hint-box">
              <label class="label">Hint:</label>
              <p class="hint-text">{{ task.hint || "No hint provided." }}</p>
            </div>
          </transition>

        </div>
      </div>
    </div>

    <div v-else class="empty">
      <p>No challenges available at the moment.</p>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import API from "../services/api";

let user_id = "guest";
const token = localStorage.getItem("access_token");

if (token) {
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    user_id = payload.user_id; 
  } catch (e) {
    console.error("Failed to decode token", e);
  }
}
const solvedKey = `solved_tasks_${user_id}`;
const challengeGroups = ref([]);
const loading = ref(true);
const openedTask = ref(null);
const openedHint = ref(null);
let pollInterval = null;

const solved = ref(JSON.parse(localStorage.getItem(solvedKey) || "{}"));

const toggleTask = (task_id) => {
  openedTask.value = openedTask.value === task_id ? null : task_id;
};

const toggleHint = (task_id) => {
  openedHint.value = openedHint.value === task_id ? null : task_id;
};

const submitAnswer = async (task) => {
  const payload = {
    task_id: task.task_id,
    answer: task.answerInput || ""
  };

  const res = await API.post("/tasks/submit", payload);

  if (res.data.correct) {
      task.pwned = true;
      if (!res.data.repeat) {
          alert(`PWNED! +${res.data.points} 分`);
      } else {
          alert(`I’ve already solved this question (+${res.data.points} points)`);
      }
      solved.value[task.task_id] = { solved: true };
      localStorage.setItem(solvedKey, JSON.stringify(solved.value));
  }
};

const loadChallenges = async () => {
  try {
    const res = await API.get("/tasks/list");
    const data = res.data;

    if (!Array.isArray(data)) {
      challengeGroups.value = [];
      return;
    }

    const cleaned = data.map((t) => {
      const restored = solved.value[t.task_id] || null;

      return {
        ...t,
        difficulty: t.difficulty || "Unknown",
        description: t.description || "No description provided.",
        tags: Array.isArray(t.tags) ? t.tags : [],
        hint: t.hint || "",
        answerInput: "",
        pwned: restored ? true : false
      };
    });

    const grouped = {};
    for (const t of cleaned) {
      const cat = t.category || "General";
      if (!grouped[cat]) {
        grouped[cat] = {
          id: cat,
          title: cat,
          description: "Tasks in " + cat,
          tasks: []
        };
      }
      grouped[cat].tasks.push(t);
    }

    challengeGroups.value = Object.values(grouped);
  } catch (err) {
    console.error("Failed to load tasks:", err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadChallenges();
  pollInterval = setInterval(loadChallenges, 5000);
});

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval);
});
</script>

<style scoped>
:root {
  --bg: #071018;
  --panel: #0b1720;
  --muted: #9fe8ff;
  --accent: #7eeaff;
  --pwned: #00ffae;
  --glass: rgba(255, 255, 255, 0.03);
}

.challenges {
  background: var(--bg);
  min-height: 100vh;
  padding: 40px 20px;
  color: var(--muted);
}

.header {
  text-align: center;
  max-width: 800px;
  margin: 0 auto 40px auto;
}

.header h1 {
  font-size: 2.6rem;
  margin-bottom: 10px;
  color: var(--accent);
}

.header .lead {
  font-size: 1.1rem;
  color: #cfeffb;
}

.challenge-group {
  background: var(--panel);
  border-radius: 14px;
  padding: 20px 24px;
  margin: 0 auto 32px auto;
  max-width: 1000px;
  box-shadow: 0 8px 28px rgba(3, 6, 10, 0.5);
}

.group-title {
  color: var(--accent);
  font-size: 1.5rem;
  margin-bottom: 4px;
}

.group-desc {
  color: #9fd9e6;
  margin-bottom: 16px;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 18px;
}

.card {
  background: var(--glass);
  padding: 16px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  position: relative;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 16px rgba(0, 198, 255, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  font-size: 1.15rem;
  color: var(--accent);
}

.difficulty {
  font-weight: bold;
  font-size: 0.9rem;
  padding: 2px 8px;
  border-radius: 8px;
  text-transform: uppercase;
}

.difficulty.easy {
  color: #00ffae;
}

.difficulty.medium {
  color: #ffea00;
}

.difficulty.hard {
  color: #ff7272;
}

.difficulty.unknown {
  color: #aaa;
}

.desc {
  color: #cfeffb;
  font-size: 0.95rem;
  margin-top: 8px;
}

.tags {
  margin-top: 10px;
}

.tag {
  display: inline-block;
  background: rgba(0, 198, 255, 0.1);
  color: var(--muted);
  border: 1px solid rgba(0, 198, 255, 0.2);
  border-radius: 6px;
  padding: 2px 8px;
  margin: 2px 4px 2px 0;
  font-size: 0.8rem;
}

.pwned-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(0, 255, 120, 0.15);
  border: 1px solid #00ffae;
  color: #00ffae;
  font-size: 0.75rem;
  font-weight: bold;
  padding: 4px 8px;
  border-radius: 6px;
  pointer-events: none;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 12px;
}

.btn {
  padding: 6px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: transform 0.1s ease, background 0.1s ease;
  font-size: 0.9rem;
}

.btn.primary {
  background: linear-gradient(90deg, #00c6ff, #3ad3d3);
  color: #001219;
}

.btn.ghost {
  background: transparent;
  border: 1px solid rgba(126, 234, 255, 0.12);
  color: var(--muted);
}

.btn:hover {
  transform: translateY(-2px);
}

.answer-box,
.hint-box {
  margin-top: 14px;
  padding: 14px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(126, 234, 255, 0.12);
  border-radius: 10px;
  backdrop-filter: blur(6px);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.label {
  color: var(--accent);
  font-weight: 600;
  font-size: 0.9rem;
}

.answer-input {
  width: 100%;
  box-sizing: border-box;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid rgba(126, 234, 255, 0.18);
  background: #061018;
  color: #c7f0ff;
  font-size: 0.9rem;
  outline: none;
}

.answer-input:disabled {
  opacity: 1;
}

.answer-correct {
  border-color: var(--pwned) !important;
  color: var(--pwned) !important;
}

.hint-text {
  color: #cfeffb;
  font-size: 0.9rem;
  white-space: pre-wrap;
}

.submit-btn {
  align-self: flex-end;
  padding: 8px 18px;
}

.loading {
  text-align: center;
  color: #9fe8ff;
  font-size: 1.2rem;
}

.empty {
  text-align: center;
  color: #9fe8ff;
  font-size: 1rem;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.22s ease;
  max-height: 300px;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  max-height: 0;
  transform: translateY(-6px);
}
</style>
