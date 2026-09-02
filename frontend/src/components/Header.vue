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

const { theme } = useTheme();

const route = useRoute();

const currentMedia = computed(() => route.path.split("/")[1] || "books");
const currentView = computed(() => route.path.split("/")[2] || "library");

const isMediaActive = (media) => currentMedia.value === media;
const isViewActive = (view) => currentView.value === view;
</script>

<template>
  <header
    class="flex w-full h-16 px-6 justify-between items-center gap-2"
    :class="theme === 'light' ? 'bg-gray-200' : 'bg-gray-800'"
  >
    <div class="flex">
      <h2
        class="text-2xl font-semibold"
        :class="theme === 'light' ? 'text-black' : 'text-white'"
      >
        uAppinnion
      </h2>
    </div>

    <nav class="flex flex-1 items-center justify-end gap-4">
      <ul
        class="flex items-center gap-2 rounded-lg p-1.5"
        :class="theme === 'light' ? 'bg-gray-300 ' : 'bg-gray-600'"
      >
        <li class="flex items-center w-auto">
          <router-link
            class="flex items-center justify-between gap-2.5 w-auto text-sm rounded-lg transition-colors"
            :class="[
              theme === 'light' ? 'text-black' : 'text-white',
              isMediaActive('books')
                ? theme === 'light'
                  ? 'bg-gray-100 p-1.5'
                  : 'bg-gray-700 p-1.5'
                : '',
            ]"
            :to="`/books/${currentView}`"
          >
            <BookOpen
              stroke-width="2"
              :class="theme === 'light ' ? 'text-gray-500' : 'text-gray-400'"
            />
            Libros
          </router-link>
        </li>
        <li class="flex items-center">
          <router-link
            class="flex items-center justify-between gap-2.5 w-auto text-sm rounded-lg transition-colors"
            :class="[
              theme === 'light' ? 'text-black' : 'text-white',
              isMediaActive('movies')
                ? theme === 'light'
                  ? 'bg-gray-100 p-1.5'
                  : 'bg-gray-700 p-1.5'
                : '',
            ]"
            :to="`/movies/${currentView}`"
          >
            <Clapperboard
              stroke-width="2"
              :class="theme === 'light ' ? 'text-gray-500' : 'text-gray-400'"
            />Peliculas
          </router-link>
        </li>

        <li class="flex items-center">
          <router-link
            class="flex items-center justify-between gap-2.5 w-auto text-sm rounded-lg transition-colors"
            :class="[
              theme === 'light' ? 'text-black' : 'text-white',
              isMediaActive('animes')
                ? theme === 'light'
                  ? 'bg-gray-100 p-1.5'
                  : 'bg-gray-700 p-1.5'
                : '',
            ]"
            :to="`/animes/${currentView}`"
          >
            <Tv
              :class="theme === 'light ' ? 'text-gray-500' : 'text-gray-400'"
              stroke-width="2"
            />Animes
          </router-link>
        </li>
      </ul>

      <ul
        class="flex items-center gap-2 rounded-lg p-1.5"
        :class="theme === 'light' ? 'bg-gray-300 ' : 'bg-gray-600'"
      >
        <li>
          <router-link
            :to="`/${currentMedia}/library`"
            class="block p-1 rounded-md transition-colors"
            :class="
              isViewActive('library')
                ? theme === 'light'
                  ? 'bg-white shadow-sm'
                  : 'bg-gray-700'
                : ''
            "
            ><Library
              :class="theme === 'light ' ? 'text-gray-500' : 'text-gray-400'"
              stroke-width="2"
          /></router-link>
        </li>
        <li>
          <router-link
            :to="`/${currentMedia}/metrics`"
            class="block p-1 rounded-md transition-colors"
            :class="
              isViewActive('metrics')
                ? theme === 'light'
                  ? 'bg-white shadow-sm'
                  : 'bg-gray-700'
                : ''
            "
            ><ChartLine
              :class="theme === 'light ' ? 'text-gray-500' : 'text-gray-400'"
              stroke-width="2"
            />
          </router-link>
        </li>
      </ul>
    </nav>

    <ThemeSwitch />
  </header>
</template>
