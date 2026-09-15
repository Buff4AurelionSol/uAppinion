<script setup>
import { BookOpen } from "@lucide/vue";
import { Clapperboard } from "@lucide/vue";
import { Tv } from "@lucide/vue";
import ThemeSwitch from "./ThemeSwitch.vue";
import { ChartLine } from "@lucide/vue";
import { Library } from "@lucide/vue";
import { Search } from "@lucide/vue";

import { useRoute } from "vue-router";
import { computed } from "vue";

const route = useRoute();

const currentMedia = computed(() => route.path.split("/")[1] || "books");
const currentView = computed(() => route.path.split("/")[2] || "catalog");

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
            class="flex items-center justify-between gap-2.5 w-auto text-sm rounded-lg transition-colors hover:text-black dark:hover:text-white"
            :class="[
              isMediaActive('books')
                ? 'bg-gray-100 dark:bg-gray-700 p-1.5 dark:text-white'
                : 'text-gray-400 dark:text-gray-400',
            ]"
            :to="`/books/${currentView}`"
          >
            <BookOpen
              stroke-width="2"
              class="text-gray-500 dark:text-gray-400"
            />
            Libros
          </router-link>
        </li>
        <li class="flex items-center">
          <router-link
            class="flex items-center justify-between gap-2.5 w-auto text-sm rounded-lg transition-colors hover:text-black dark:hover:text-white"
            :class="[
              isMediaActive('movies')
                ? 'bg-gray-100 dark:bg-gray-700 p-1.5 dark:text-white'
                : 'text-gray-400 dark:text-gray-400',
            ]"
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
            class="flex items-center justify-between gap-2.5 w-auto text-sm rounded-lg transition-colors hover:text-black dark:hover:text-white"
            :class="[
              isMediaActive('animes')
                ? 'bg-gray-100 dark:bg-gray-700 p-1.5 dark:text-white'
                : 'text-gray-400 dark:text-gray-400',
            ]"
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
            :to="`/${currentMedia}/catalog`"
            class="block p-1 rounded-md transition-colors group"
            :class="{
              'bg-white shadow-sm dark:bg-gray-700': isViewActive('catalog'),
            }"
            ><Search
              stroke-width="2"
              :class="[
                'text-gray-500',
                isViewActive('catalog')
                  ? 'dark:text-gray-400'
                  : 'dark:text-gray-500',
                'group-hover:text-gray-400',
              ]"
          /></router-link>
        </li>
        <li>
          <router-link
            :to="`/${currentMedia}/library`"
            class="block p-1 rounded-md transition-colors group"
            :class="{
              'bg-white shadow-sm dark:bg-gray-700': isViewActive('library'),
            }"
            ><Library
              stroke-width="2"
              :class="[
                'text-gray-500',
                isViewActive('library')
                  ? 'dark:text-gray-400'
                  : 'dark:text-gray-500',
                'group-hover:text-gray-400',
              ]"
          /></router-link>
        </li>
        <li>
          <router-link
            :to="`/${currentMedia}/metrics`"
            class="block p-1 rounded-md transition-colors group"
            :class="{
              'bg-white shadow-sm dark:bg-gray-700': isViewActive('metrics'),
            }"
            ><ChartLine
              stroke-width="2"
              :class="[
                'text-gray-500',
                isViewActive('metrics')
                  ? 'dark:text-gray-400'
                  : 'dark:text-gray-500',
                'group-hover:text-gray-400',
              ]"
            />
          </router-link>
        </li>
      </ul>
    </nav>

    <ThemeSwitch />
  </header>
</template>
