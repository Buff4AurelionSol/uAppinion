<script setup>
import { computed } from "vue";
import { apiBooks } from "../services/apiBook";
import { statusesValues } from "../consts/booksConsts";

const props = defineProps({
  book: {
    type: Object,
    required: true,
  },
  actionText: {
    type: String,
    default: "Reseñar",
  },
  status: {
    type: String,
  },
});

const myAuthorsNames = computed(() => {
  return props.book?.authors.map((item) => item.name).join(", ");
});

const myStatus = computed(() => {
  if (!props.status) return null;

  return statusesValues.find((item) => item.value === props.status) || null;
});

defineEmits(["action"]);
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
      <div class="flex justify-between">
        <div>
          <h2
            class="font-bold line-clamp-2 leading-tight text-black dark:text-white"
          >
            {{ book?.title }}
          </h2>
        </div>
        <div
          v-if="myStatus"
          class="px-1.5 py-0.5 rounded-md flex items-center shrink-0"
          :class="myStatus?.classes"
        >
          <span>{{ myStatus?.label }}</span>
        </div>
      </div>
      <div>
        <p
          v-if="book?.author_name?.length"
          class="text-sm text-gray-700 dark:text-gray-400 mt-1 truncate"
        >
          {{ book.author_name?.join(", ") }}
        </p>
        <p
          v-else-if="book?.authors?.length"
          class="text-sm text-gray-700 dark:text-gray-400 mt-1 truncate"
        >
          {{ myAuthorsNames }}
        </p>
        <p
          v-else
          class="text-sm text-gray-700 dark:text-gray-400 mt-1 truncate"
        >
          {{ "Autor Desconocido." }}
        </p>
      </div>

      <div class="mt-2 w-full flex justify-between">
        <span
          class="bg-gray-300 px-2 py-1 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md text-xs truncate shrink"
        >
          {{ book?.first_publish_year || "Año desconocido" }}
        </span>
        <button
          @click="$emit('action')"
          class="bg-sky-500 hover:bg-sky-400 dark:bg-sky-700 dark:hover:bg-sky-600 px-2 py-1 rounded-md text-white font-semibold text-sm"
        >
          {{ actionText }}
        </button>
      </div>
    </div>
  </div>
</template>
