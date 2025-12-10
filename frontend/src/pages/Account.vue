<template>
  <section class="account-hero">
    <div class="account-box">
      <h1>Sign In</h1>
      <p class="lead">Welcome back! Please enter your credentials to continue.</p>

      <div class="form">
        <input v-model="username" placeholder="Username" />
        <input v-model="password" type="password" placeholder="Password" />
        <button class="btn primary" @click="login">Sign In</button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        <p class="hint">
          Don't have an account?
          <router-link to="/register" class="link">Create one</router-link>
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue";
import API from "../services/api";
const username = ref("");
const password = ref("");
const errorMessage = ref("");
const dangerousPattern = /<script|<\/script|['"`;]|--|\/\*|or\s+1=1/i;

const login = async () => {
  errorMessage.value = "";

  if (
    dangerousPattern.test(username.value) ||
    dangerousPattern.test(password.value)
  ) {
    errorMessage.value = "Invalid characters detected. Please retype.";
    return;
  }

  const payload = { user_name: username.value, password: password.value };
  const res = await API.post("/auth/token", payload).catch(() =>
    alert("Login failed")
  );

  if (res?.data?.access_token) {
    localStorage.setItem("access_token", res.data.access_token);
    alert("Login successful");
    location.href = "/home";
  }
};
</script>

<style scoped>
:root {
  --bg: #071018;
  --panel: #0b1720;
  --muted: #9fe8ff;
  --accent: #7eeaff;
}

.account-hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, #040608 0%, #071018 60%);
  color: var(--muted);
  font-size: 1.05rem;
}

.account-box {
  background: var(--panel);
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
  padding: 48px 36px;
  width: 380px;
  text-align: center;
}

h1 {
  color: var(--accent);
  margin-bottom: 12px;
  font-size: 2rem;
}

.lead {
  font-size: 1.05rem;
  margin-bottom: 28px;
  color: #cfeeff;
}

.form input {
  display: block;
  width: 100%;
  margin: 12px 0;
  padding: 12px 14px;
  border-radius: 8px;
  border: 1px solid #123;
  background: #061018;
  color: #c7f0ff;
  font-size: 1rem;
}

.btn {
  display: inline-block;
  width: 100%;
  margin-top: 14px;
  padding: 12px 16px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.12s ease;
}

.btn.primary {
  background: linear-gradient(90deg, #00c6ff, #3ad3d3);
  color: #001219;
  box-shadow: 0 4px 16px rgba(0, 198, 255, 0.15);
}

.btn:hover {
  transform: translateY(-3px);
}

.hint {
  margin-top: 22px;
  font-size: 0.95rem;
  color: #a8d8e8;
}

.link {
  color: var(--accent);
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
}

.link:hover {
  text-decoration: underline;
}

.error {
  margin-top: 14px;
  color: #ff6b6b;
  font-weight: 600;
}
</style>