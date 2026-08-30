<script setup>
import { BookOpen } from "@lucide/vue";
import { Clapperboard } from "@lucide/vue";
import { Tv } from "@lucide/vue";
import ThemeSwitch from "./ThemeSwitch.vue";
import { ChartLine } from "@lucide/vue";
import { Library } from "@lucide/vue";
import { useTheme } from "../const/useTheme.js";

const { theme } = useTheme();
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
          <a
            href="/"
            class="flex items-center justify-between gap-2.5 w-auto text-sm rounded-md"
            :class="theme === 'light' ? 'text-black' : 'text-white'"
          >
            <BookOpen
              stroke-width="2"
              :class="theme === 'light ' ? 'text-gray-500' : 'text-gray-400'"
            />
            Libros
          </a>
        </li>
        <li class="flex items-center">
          <a
            href="/"
            class="flex items-center justify-between gap-2.5 w-auto text-sm"
            :class="theme === 'light' ? 'text-black' : 'text-gray-200'"
          >
            <Clapperboard
              stroke-width="2"
              :class="theme === 'light ' ? 'text-gray-500' : 'text-gray-400'"
            />Peliculas
          </a>
        </li>

        <li class="flex items-center">
          <a
            href="/"
            class="flex items-center justify-between gap-2.5 w-auto text-sm"
            :class="theme === 'light' ? 'text-black' : 'text-gray-200'"
          >
            <Tv
              :class="theme === 'light ' ? 'text-gray-500' : 'text-gray-400'"
              stroke-width="2"
            />Animes
          </a>
        </li>
      </ul>

      <ul
        class="flex items-center gap-2 rounded-lg p-1.5"
        :class="theme === 'light' ? 'bg-gray-300 ' : 'bg-gray-600'"
      >
        <li>
          <a href="/"
            ><Library
              :class="theme === 'light ' ? 'text-gray-500' : 'text-gray-400'"
              stroke-width="2"
          /></a>
        </li>
        <li>
          <a href="/"
            ><ChartLine
              :class="theme === 'light ' ? 'text-gray-500' : 'text-gray-400'"
              stroke-width="2"
            />
          </a>
        </li>
      </ul>
    </nav>

    <ThemeSwitch />
  </header>
</template>
