<script setup>
import { apiBooks } from "../services/apiBook";

const props = defineProps({
  book: {
    type: Object,
    required: true,
  },
});

defineEmits(["review"]);
</script>

<template>
  <div
    class="flex gap-1.5 h-40 bg-gray-200 dark:bg-gray-600 rounded-lg p-2 overflow-hidden"
  >
    <div
      class="w-24 h-full shrink-0 bg-gray-300 rounded-md overflow-hidden relative"
    >
      <img
        v-if="book?.cover_i"
        :src="apiBooks.getImageUrl(book.cover_i, 'M')"
        :alt="book?.title"
        class="h-full w-full object-cover rounded-md absolute inset-0"
      />
    </div>
    <div class="flex flex-col justify-between min-w-0 w-full">
      <div>
        <h2
          class="font-bold line-clamp-2 leading-tight text-black dark:text-white"
        >
          {{ book?.title }}
        </h2>
      </div>
      <div>
        <p class="text-sm text-gray-700 dark:text-gray-400 mt-1 truncate">
          {{ book?.author_name?.join(", ") || "Autor Desconocido." }}
        </p>
      </div>

      <div class="mt-2 w-full flex justify-between">
        <span
          class="bg-gray-300 px-2 py-1 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md text-xs truncate shrink"
        >
          {{ book?.first_publish_year || "Año desconocido" }}
        </span>
        <button
          @click="$emit('review')"
          class="bg-sky-500 hover:bg-sky-400 dark:bg-sky-700 dark:hover:bg-sky-600 px-2 py-1 rounded-md text-white font-semibold text-sm"
        >
          Reseñar
        </button>
      </div>
    </div>
  </div>
</template>
