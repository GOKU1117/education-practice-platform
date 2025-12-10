<template>
  <div>
    <h2>Monitor</h2>
    <button @click="load">Loading</button>
    <table v-if="logs.length">
      <tr><th>time</th><th>user</th><th>path</th><th>method</th></tr>
      <tr v-for="l in logs" :key="l.id">
        <td>{{ l.created_at }}</td><td>{{ l.user_id }}</td><td>{{ l.path }}</td><td>{{ l.method }}</td>
      </tr>
    </table>
  </div>
</template>

<script>
import API from "../services/api";
import { ref } from "vue";
export default {
  setup() {
    const logs = ref([]);
    const load = async () => {
      const res = await API.get("/admin/traffic");
      logs.value = res.data.logs || [];
    };
    return { logs, load };
  }
};
</script>
