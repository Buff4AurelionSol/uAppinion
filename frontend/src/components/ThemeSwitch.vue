<script setup>
import { Moon } from "@lucide/vue";
import { Sun } from "@lucide/vue";
import { useTheme } from "../const/useTheme";

const themeRef = useTheme();
</script>

<template>
  <button
    @click="themeRef.toggleTheme"
    class="group flex items-center justify-center h-10 w-10 rounded-full bg-gray-300 dark:bg-gray-600"
  >
    <Moon
      class="text-gray-400 hover:text-gray-700"
      v-if="themeRef.theme.value === 'light'"
    />
    <Sun class="text-gray-400 hover:text-gray-100" v-else />
  </button>
</template>
