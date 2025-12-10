<template>
  <section class="dashboard">
    <div class="header">
      <h1>🏆 Dashboard</h1>
      <p class="lead">Top 10 participants with the highest cumulative challenge scores.</p>
    </div>

    <div class="panel">
      <h2>Top 10 Players</h2>

      <div class="leaderboard">
        <div 
          class="player"
          v-for="(u, i) in top10"
          :key="i"
          :class="['rank-' + (i + 1)]"
        >
          <div class="rank">#{{ i + 1 }}</div>

          <img 
            class="avatar"
            :src="u.avatar || `https://api.dicebear.com/7.x/bottts/svg?seed=${u.user_name}`"
          />

          <div class="info">
            <div class="name">{{ u.user_name }}</div>

            <div class="bar">
              <div 
                class="fill"
                :style="{ width: progressWidth[i] + '%' }"
              ></div>
            </div>
          </div>

          <div class="score">{{ u.total }}</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import API from "../services/api";

const top10 = ref([]);
const maxScore = ref(1);
const progressWidth = ref([]);

onMounted(async () => {
  const res = await API.get("/leaderboard/score");
  top10.value = res.data.top10 || [];

  maxScore.value = Math.max(...top10.value.map(u => u.total), 1);

  progressWidth.value = top10.value.map(() => 0);

  setTimeout(() => {
    progressWidth.value = top10.value.map(u => (u.total / maxScore.value) * 100);
  }, 200);
});
</script>

<style scoped>
:root {
  --bg: #071018;
  --panel: #0b1720;
  --muted: #9fe8ff;
  --accent: #7eeaff;

  --gold: #ffd700;
  --silver: #c0c0c0;
  --bronze: #cd7f32;
}

.dashboard {
  background: var(--bg);
  min-height: 100vh;
  padding: 40px 20px;
  color: var(--muted);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.header {
  text-align: center;
  margin-bottom: 30px;
  max-width: 700px;
}

.header h1 {
  font-size: 2.6rem;
  margin-bottom: 8px;
  color: var(--accent);
}

.lead {
  color: #cfeffb;
  font-size: 1.05rem;
}

.panel {
  background: var(--panel);
  border-radius: 14px;
  padding: 28px;
  max-width: 900px;
  width: 100%;
  box-shadow: 0 8px 28px rgba(3, 6, 10, 0.6);
}

.panel h2 {
  color: var(--accent);
  margin-bottom: 20px;
  font-size: 1.4rem;
  border-left: 4px solid var(--accent);
  padding-left: 10px;
}

.leaderboard {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.player {
  display: flex;
  align-items: center;
  background: #0d1d28;
  padding: 14px 18px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(5, 10, 15, 0.5);
  gap: 14px;

  opacity: 0;
  transform: translateY(10px);
  animation: fadeUp 0.5s ease forwards;
}

.rank {
  width: 40px;
  font-size: 1.3rem;
}

.rank-1 .rank {
  color: var(--gold);
}
.rank-2 .rank {
  color: var(--silver);
}
.rank-3 .rank {
  color: var(--bronze);
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  background: #ffffff22;
}

.info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.name {
  font-size: 1.1rem;
  margin-bottom: 6px;
}

.bar {
  width: 100%;
  height: 8px;
  background: rgba(255,255,255,0.08);
  border-radius: 4px;
  overflow: hidden;
}

.fill {
  height: 100%;
  background: var(--accent);
  transition: width 0.8s ease;
}

.score {
  width: 80px;
  text-align: right;
  font-size: 1.2rem;
  color: #cfeffb;
}

@keyframes fadeUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
