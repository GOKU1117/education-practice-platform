<template>
  <section class="hero">
    <div class="hero-inner">
      <div class="hero-text">
        <h1>Education Practice Platform</h1>
        <p class="lead">A collaborative learning space for students to practice and reinforce classroom concepts.</p>
        <p class="sub">
          Teachers can create customized exercises and assignments, while students engage in interactive problem-solving
          to strengthen their understanding. Enhance learning outcomes through structured practice and guided challenges.
        </p>
        <div class="actions">
          <a class="btn primary" href="/challenges">Start Challenges</a>
          <a class="btn ghost" href="/dashboard">Dashboard</a>
        </div>
      </div>

      <div class="carousel" aria-label="OT CTF highlights carousel">
        <div
          class="slides"
          :style="{ transform: `translateX(-${currentIndex * 100}%)` }"
          role="list"
        >
          <figure class="slide" role="listitem">
            <img src="/images/education-01.jpg" alt="Interactive Assignment Platform Placeholder" />
            <figcaption>
              <h3>Interactive Assignment Platform</h3>
              <p>Students can submit answers online and receive feedback, while teachers track progress and adjust teaching strategies.</p>
            </figcaption>
          </figure>

          <figure class="slide" role="listitem">
            <img src="/images/education-02.jpg" alt="After-Class Practice Sets Placeholder" />
            <figcaption>
              <h3>After-Class Practice Sets</h3>
              <p>Teachers can create diverse exercises that help students reinforce key concepts learned in class.</p>
            </figcaption>
          </figure>

          <figure class="slide" role="listitem">
            <img src="/images/education-03.jpg" alt="Concept Reinforcement Placeholder" />
            <figcaption>
              <h3>Concept Reinforcement</h3>
              <p>Students progress through structured, step-by-step questions designed to strengthen understanding and support self-learning.</p>
            </figcaption>
          </figure>
        </div>

        <div class="controls">
          <button class="ctrl" @click="prev" aria-label="Previous slide">‹</button>
          <div class="dots">
            <button
              v-for="(s, i) in slidesCount"
              :key="i"
              :class="['dot', { active: i === currentIndex }]"
              @click="go(i)"
              :aria-label="`Go to slide ${i + 1}`"
            ></button>
          </div>
          <button class="ctrl" @click="next" aria-label="Next slide">›</button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";

const currentIndex = ref(0);
const slidesCount = 3;
let timer = null;

const next = () => {
  currentIndex.value = (currentIndex.value + 1) % slidesCount;
};

const prev = () => {
  currentIndex.value = (currentIndex.value - 1 + slidesCount) % slidesCount;
};

const go = (i) => {
  currentIndex.value = i;
};

onMounted(() => {
  timer = setInterval(next, 4500);
});

onBeforeUnmount(() => {
  if (timer) clearInterval(timer);
});
</script>

<style scoped>
:root {
  --bg: #071018;
  --panel: #0b1720;
  --muted: #9fe8ff;
  --accent: #7eeaff;
  --glass: rgba(255,255,255,0.03);
}

.hero {
  min-height: 76vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, #040608 0%, #071018 60%);
  color: var(--muted);
  padding: 40px 20px;
}

.hero-inner {
  max-width: 1200px;
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 520px;
  gap: 28px;
  align-items: center;
}

.hero-text h1 {
  font-size: 3.2rem;
  margin: 0 0 10px 0;
  letter-spacing: -1px;
  color: var(--accent);
}

.lead {
  font-size: 1.25rem;
  margin-bottom: 12px;
  color: #cfeffb;
}

.sub {
  color: #9fd9e6;
  line-height: 1.5;
  max-width: 56ch;
  margin-bottom: 18px;
  font-size: 1rem;
}

.actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.btn {
  display: inline-block;
  padding: 10px 16px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.98rem;
  transition: transform .12s ease, box-shadow .12s ease;
}

.btn.primary {
  background: linear-gradient(90deg, #00c6ff, #3ad3d3);
  color: #001219;
  box-shadow: 0 6px 18px rgba(0,198,255,0.12);
}

.btn.ghost {
  background: transparent;
  border: 1px solid rgba(126,234,255,0.12);
  color: var(--muted);
}

.btn:hover { transform: translateY(-3px); }

.carousel {
  background: var(--panel);
  border-radius: 12px;
  padding: 12px;
  box-shadow: 0 10px 30px rgba(3,6,10,0.6);
  overflow: hidden;
}

.slides {
  display: flex;
  width: 300%;
  transition: transform 0.6s cubic-bezier(.2,.9,.2,1);
}

.slide {
  width: 100%;
  display: grid;
  grid-template-rows: 1fr auto;
  gap: 10px;
  align-items: stretch;
  padding: 6px;
}

.slide img {
  width: 100%;
  height: 320px;
  object-fit: cover;
  border-radius: 8px;
  background: linear-gradient(90deg,#021018,#04202a);
  display: block;
}

.slide figcaption {
  padding: 8px 6px;
}

.slide h3 {
  margin: 6px 0 4px 0;
  font-size: 1.05rem;
  color: var(--accent);
}

.slide p {
  margin: 0;
  font-size: 0.95rem;
  color: #cfeffb;
}

/* Controls */
.controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 8px;
}

.ctrl {
  background: var(--glass);
  border: none;
  padding: 8px 12px;
  border-radius: 8px;
  color: var(--muted);
  font-size: 1.3rem;
  cursor: pointer;
}

.dots {
  display: flex;
  gap: 8px;
  align-items: center;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.04);
  cursor: pointer;
  transition: transform .12s ease, background .12s ease;
}

.dot.active {
  background: var(--accent);
  transform: scale(1.25);
}

@media (max-width: 980px) {
  .hero-inner { grid-template-columns: 1fr; }
  .slide img { height: 260px; }
  .hero-text h1 { font-size: 2.4rem; }
}

@media (max-width: 480px) {
  .slide img { height: 180px; }
  .lead { font-size: 1rem; }
  .hero-text h1 { font-size: 1.8rem; }
}
</style>
