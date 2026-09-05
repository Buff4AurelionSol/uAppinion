<script setup>
import { BookOpen } from "@lucide/vue";
import { Clapperboard } from "@lucide/vue";
import { Tv } from "@lucide/vue";
import ThemeSwitch from "./ThemeSwitch.vue";
import { ChartLine } from "@lucide/vue";
import { Library } from "@lucide/vue";
import { useTheme } from "../const/useTheme.js";
import { useRoute } from "vue-router";
import { computed, watchEffect } from "vue";

const route = useRoute();

const currentMedia = computed(() => route.path.split("/")[1] || "books");
const currentView = computed(() => route.path.split("/")[2] || "library");

const isMediaActive = (media) => currentMedia.value === media;
const isViewActive = (view) => currentView.value === view;
</script>

<template>
  <header
    class="flex w-full h-16 px-6 justify-between items-center gap-2 bg-gray-200 dark:bg-gray-800"
  >
    <div class="flex">
      <h2 class="text-2xl font-semibold text-black dark:text-white">
        uAppinnion
      </h2>
    </div>

    <nav class="flex flex-1 items-center justify-end gap-4">
      <ul
        class="flex items-center gap-2 rounded-lg p-1.5 bg-gray-300 dark:bg-gray-600"
      >
        <li class="flex items-center w-auto">
          <router-link
            class="flex items-center justify-between gap-2.5 w-auto text-sm rounded-lg transition-colors text-black dark:text-white"
            :class="{
              'bg-gray-100 dark:bg-gray-700 p-1.5': isMediaActive('books'),
            }"
            :to="`/books/${currentView}`"
          >
            <BookOpen
              stroke-width="2"
              class="text-gray-500 dark:text-gray-700'"
            />
            Libros
          </router-link>
        </li>
        <li class="flex items-center">
          <router-link
            class="flex items-center justify-between gap-2.5 w-auto text-sm rounded-lg transition-colors text-black dark:text-white"
            :class="{
              'bg-gray-100 dark:bg-gray-700 p-1.5': isMediaActive('movies'),
            }"
            :to="`/movies/${currentView}`"
          >
            <Clapperboard
              stroke-width="2"
              class="text-gray-500 dark:text-gray-400"
            />Peliculas
          </router-link>
        </li>

        <li class="flex items-center">
          <router-link
            class="flex items-center justify-between gap-2.5 w-auto text-sm rounded-lg transition-colors text-black dark:text-white"
            :class="{
              'bg-gray-100 dark:bg-gray-700 p-1.5': isMediaActive('animes'),
            }"
            :to="`/animes/${currentView}`"
          >
            <Tv
              class="text-gray-500 dark:text-gray-400"
              stroke-width="2"
            />Animes
          </router-link>
        </li>
      </ul>

      <ul
        class="flex items-center gap-2 rounded-lg p-1.5 bg-gray-300 dark:bg-gray-600"
      >
        <li>
          <router-link
            :to="`/${currentMedia}/library`"
            class="block p-1 rounded-md transition-colors"
            :class="{
              'bg-white shadow-sm dark:bg-gray-700': isViewActive('library'),
            }"
            ><Library
              class="text-gray-500 dark:text-gray-400'"
              stroke-width="2"
          /></router-link>
        </li>
        <li>
          <router-link
            :to="`/${currentMedia}/metrics`"
            class="block p-1 rounded-md transition-colors"
            :class="{
              'bg-white shadow-sm dark:bg-gray-700': isViewActive('metrics'),
            }"
            ><ChartLine
              class="text-gray-500 dark:text-gray-400"
              stroke-width="2"
            />
          </router-link>
        </li>
      </ul>
    </nav>

    <ThemeSwitch />
  </header>
</template>
