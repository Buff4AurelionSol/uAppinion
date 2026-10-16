<script setup>
import Header from "../components/Header.vue";
import { useAuth } from "../stores/auth.js";
const authStore = useAuth();
</script>
<template>
  <div class="flex flex-col min-h-screen">
    <Header v-if="authStore.isAuthenticated" />
    <RouterView />
  </div>
</template>
