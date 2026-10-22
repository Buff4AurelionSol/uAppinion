<script setup>
import { onMounted } from "vue";
import MainLayout from "./features/MainLayout.vue";
import { useAuth } from "./stores/auth.js";
import { api } from "./api/axios.js";

const authStore = useAuth();

onMounted(async () => {
  if (!authStore.authData) {
    try {
      const { data } = await api.post("/auth/refresh");
      authStore.authData = data;
    } catch (e) {
      console.log("Sesión no iniciada o expirada");
      console.log(e);
    }
  }
});
</script>

<template>
  <MainLayout />
</template>
