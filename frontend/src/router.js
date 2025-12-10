import { createRouter, createWebHistory } from "vue-router";
import Account from "./pages/Account.vue";
import Register from "./pages/Register.vue";
import Home from "./pages/Home.vue";
import Challenges from "./pages/Challenges.vue";
import Dashboard from "./pages/Dashboard.vue";
import AdminSetup from "./pages/AdminSetup.vue";

const routes = [
  { path: "/", redirect: '/account'},
  { path: "/account", component: Account},
  { path: "/register", component: Register},
  { path: "/home", component: Home, meta: { requiresAuth: true }},
  { path: "/challenges", component: Challenges, meta: { requiresAuth: true } },
  { path: "/dashboard", component: Dashboard, meta: { requiresAuth: true } },
  { path: "/adminsetup", component: AdminSetup, meta: { requiresAuth: true, adminOnly: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access_token");
  if (to.meta.requiresAuth && !token) return next("/account");

  if (to.meta.adminOnly) {
    try {
      const payload = JSON.parse(atob(token.split(".")[1]));
      if (payload.sub !== "admin") return next("/home");
    } catch {
      return next("/account");
    }
  }
  next();
});

export default router;
