<template>
  <section class="setup">
    <div class="form-box">
      <h1>Create Task</h1>
      <p class="lead">Only admin users can create and upload new challenges.</p>

      <form @submit.prevent="createTask">
        <input v-model="title" placeholder="Title" required />
        <textarea v-model="description" placeholder="Description" rows="4" />

        <input v-model="category" placeholder="Category" />

        <select v-model="difficulty">
          <option value="Easy">Easy</option>
          <option value="Medium">Medium</option>
          <option value="Hard">Hard</option>
        </select>

        <input
          v-model="tags"
          placeholder="Tags (comma-separated, e.g. modbus, network, exploit)"
        />

        <input
          v-model.number="points"
          type="number"
          placeholder="Points"
          min="0"
        />

        <input v-model="answer" placeholder="Answer (correct solution)" />

        <input v-model="hint" placeholder="Hint (shown to users)" />

        <button type="submit" class="btn primary" :disabled="loading" href="/challenges">
          {{ loading ? "Creating..." : "Submit" }}
        </button>
      </form>

      <p v-if="message" class="msg">{{ message }}</p>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue";
import API from "../services/api";

const title = ref("");
const description = ref("");
const category = ref("");
const difficulty = ref("Easy");
const tags = ref("");
const points = ref(0);
const message = ref("");
const loading = ref(false);
const answer = ref("");
const hint = ref("");

const createTask = async () => {
  message.value = "";
  loading.value = true;

  const token = localStorage.getItem("access_token");
  const formData = new FormData();

  formData.append("title", title.value);
  formData.append("description", description.value);
  formData.append("category", category.value);
  formData.append("difficulty", difficulty.value);
  formData.append("tags", tags.value);
  formData.append("points", points.value);

  formData.append("answer", answer.value);
  formData.append("hint", hint.value);

  try {
    const res = await API.post("/admin/tasks/create", formData, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    message.value = `Created task: ${res.data.title}`;
    resetForm();
  } catch (err) {
    if (err.response) {
      message.value = `Error ${err.response.status}: ${
        err.response.data.detail || "Failed to create task"
      }`;
    } else {
      message.value = "Network or server error.";
    }
  } finally {
    loading.value = false;
  }
};

const resetForm = () => {
  title.value = "";
  description.value = "";
  category.value = "";
  difficulty.value = "Easy";
  tags.value = "";
  points.value = 0;
  answer.value = "";
  hint.value = "";
};
</script>

<style scoped>
:root {
  --bg: #071018;
  --panel: #0b1720;
  --accent: #7eeaff;
  --muted: #9fe8ff;
}

.setup {
  background: var(--bg);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--muted);
}

.form-box {
  background: var(--panel);
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
  width: 420px;
  text-align: center;
}

h1 {
  color: var(--accent);
  margin-bottom: 10px;
}

.lead {
  font-size: 1rem;
  color: #b7eaff;
  margin-bottom: 20px;
}

form input,
form textarea,
form select {
  width: 100%;
  padding: 12px;
  margin: 8px 0;
  border-radius: 8px;
  border: 1px solid #123;
  background: #061018;
  color: #c7f0ff;
  font-size: 1rem;
}

form select {
  background: #061018;
  color: #9fe8ff;
}

.btn.primary {
  width: 100%;
  background: linear-gradient(90deg, #00c6ff, #3ad3d3);
  color: #001219;
  padding: 10px;
  margin-top: 10px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.btn.primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.msg {
  margin-top: 16px;
  color: #8ff;
}
</style>
