<script setup>
import { useRoute } from "vue-router";
import { computed, onMounted, onBeforeUnmount } from "vue";
import UserMenu from "./components/UserMenu.vue";

const route = useRoute();
const expireMinutes = 15;
let timer = null;

const logout = () => {
  localStorage.removeItem("access_token");
  location.href = "/account";
};

const resetTimer = () => {
  if (timer) clearTimeout(timer);
  timer = setTimeout(logout, expireMinutes * 60 * 1000);
};

const activityEvents = ["click", "mousemove", "keydown", "scroll", "touchstart"];

onMounted(() => {
  resetTimer();
  activityEvents.forEach((e) => document.addEventListener(e, resetTimer));
});

onBeforeUnmount(() => {
  if (timer) clearTimeout(timer);
  activityEvents.forEach((e) => document.removeEventListener(e, resetTimer));
});

const isAdmin = computed(() => {
  const token = localStorage.getItem("access_token");
  if (!token) return false;
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.sub === "admin";
  } catch {
    return false;
  }
});
</script>

<template>
  <div id="app" class="app">
    <nav v-if="route.path !== '/account' && route.path !== '/register'" class="nav">
      <div class="left">
        <router-link to="/home">Home</router-link>
        <router-link to="/challenges">Challenges</router-link>
        <router-link to="/dashboard">Dashboard</router-link>
        <router-link v-if="isAdmin" to="/adminsetup">Setup</router-link>
      </div>

      <div class="right">
        <UserMenu />
      </div>
    </nav>
    <router-view />
  </div>
</template>

<style>
body {
  margin: 0;
  background: #0b0f12;
  color: #c7f0ff;
  font-family: monospace;
}

.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 12px 20px;
  background: #071018;
  border-bottom: 1px solid #0d2330;
}

.nav .left {
  display: flex;
  gap: 18px;
}

.nav .right {
  display: flex;
  align-items: center;
}

a {
  color: #8ef;
  text-decoration: none;
}
</style>
