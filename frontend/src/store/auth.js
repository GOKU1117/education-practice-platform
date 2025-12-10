import { reactive } from "vue";
const state = reactive({ user: null });
export default {
  install(app) {
    app.config.globalProperties.$auth = state;
  },
  login(payload) {
    localStorage.setItem("access_token", payload.token);
    state.user = payload.user;
  },
  logout() {
    localStorage.removeItem("access_token");
    state.user = null;
  },
  state
};
