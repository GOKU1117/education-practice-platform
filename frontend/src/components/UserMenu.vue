<template>
  <div class="user-menu" @click.stop="toggleMenu">
    <div class="user-info">
      <img class="avatar" :src="avatarPath" />
      <span class="username">{{ username }}</span>
    </div>

    <transition name="fade">
      <div v-if="menuOpen" class="dropdown">
        <button class="btn ghost logout" @click="logout">Logout</button>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";

const token = localStorage.getItem("access_token");
const menuOpen = ref(false);

const username = computed(() => {
  if (!token) return "";
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.sub || "";
  } catch {
    return "";
  }
});

const iconIndex = Math.floor(Math.random() * 3) + 1;

const avatarPath = computed(() => {
  return `/images/user-icon-0${iconIndex}.jpg`;
});

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value;
};

const closeMenu = () => {
  menuOpen.value = false;
};

onMounted(() => {
  document.addEventListener("click", closeMenu);
});

onBeforeUnmount(() => {
  document.removeEventListener("click", closeMenu);
});

const logout = () => {
  localStorage.removeItem("access_token");
  location.href = "/account";
};
</script>

<style scoped>
.user-menu {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #7eeaff;
}

.username {
  margin-top: 4px;
  font-size: 0.85rem;
  color: #9fe8ff;
  font-weight: 600;
}

.dropdown {
  position: absolute;
  top: 68px;
  right: -10px;
  width: 150px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(126, 234, 255, 0.12);
  border-radius: 10px;
  backdrop-filter: blur(8px);
  box-shadow: 0 8px 24px rgba(0, 198, 255, 0.12);
  display: flex;
  flex-direction: column;
  gap: 12px;
  z-index: 50;
}

.drop-username {
  color: #7eeaff;
  font-weight: 700;
  text-align: center;
  font-size: 0.9rem;
}

.btn {
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform .12s ease;
}

.btn.ghost {
  background: transparent;
  border: 1px solid rgba(126,234,255,0.12);
  color: #9fe8ff;
}

.btn:hover {
  transform: translateY(-3px);
}

.logout {
  width: 100%;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity .18s ease, transform .18s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

.user-menu * {
  cursor: pointer;
}
</style>
