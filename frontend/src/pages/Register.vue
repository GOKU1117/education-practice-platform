<template>
  <section class="account-hero">
    <div class="account-box">
      <h1>Create Account</h1>
      <p class="lead">Fill in your details to register a new account.</p>

      <div class="form">
        <input v-model="rname" placeholder="Username" />
        <input v-model="remail" placeholder="Email" />
        <input v-model="rpass" type="password" placeholder="Password" />
        <button class="btn primary" @click="register">Sign Up</button>

        <p class="hint">
          Already have an account?
          <router-link to="/" class="link">Back to Sign In</router-link>
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue";
import API from "../services/api";
const rname = ref("");
const remail = ref("");
const rpass = ref("");
const dangerousPattern = /<script|<\/script|['"`;]|--|\/\*/i;

const register = async () => {
  if (
    dangerousPattern.test(rname.value) ||
    dangerousPattern.test(remail.value)
  ) {
    alert("Invalid input detected.");
    return;
  }

  const payload = {
    user_name: rname.value,
    user_email: remail.value,
    password: rpass.value,
  };

  const res = await API.post("/auth/register", payload).catch(() =>
    alert("Registration failed")
  );

  if (res?.data) {
    alert("Registration successful! Please sign in.");
    location.href = "/account";
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
</style>
