<script setup>
import { computed } from "vue";
import Modal from "../../../components/Modal.vue";
import { apiBooks } from "../services/apiBook.js";
import { statusesValues } from "../consts/booksConsts.js";

const props = defineProps({
  review: {
    type: Object,
    default: () => ({}),
  },
});

const isOpenModal = defineModel();
const limitedGenres = computed(
  () => props.review?.book?.genres?.slice(0, 6) || [],
);

const myStatus = computed(() => {
  if (!props.review?.status) return null;

  return (
    statusesValues.find((item) => item.value === props.review?.status) || null
  );
});
</script>

<template>
  <Modal v-model="isOpenModal">
    <div class="flex gap-4">
      <div class="w-20 h-40 rounded-lg shrink-0 relative overflow-hidden">
        <img
          v-if="review?.book?.cover_i"
          :src="apiBooks.getImageUrl(review?.book?.cover_i, 'M')"
          :alt="review?.book?.title"
          class="h-full w-full object-cover rounded-md absolute inset-0"
        />
      </div>
      <div class="w-full flex flex-col gap-4">
        <div class="flex flex-col gap-3">
          <div class="flex justify-between">
            <div>
              <h3 class="text-2xl font-bold dark:text-white leading-tight">
                {{ review?.book?.title }}
              </h3>
            </div>
            <div
              v-if="myStatus"
              class="px-1.5 py-0.5 rounded-md flex items-center shrink-0"
              :class="myStatus?.classes"
            >
              <span>{{ myStatus?.label }}</span>
            </div>
          </div>
          <h3 class="text-md text-sky-600 dark:text-sky-400">
            {{ review?.book?.authors?.map((item) => item.name).join(", ") }}
          </h3>
        </div>
        <div
          v-if="review?.book.genres.length >= 1"
          class="flex flex-wrap gap-2"
        >
          <div
            v-for="genre in limitedGenres"
            :key="genre.id"
            class="gap-2 px-4 py-0.5 rounded-md bg-gray-200 dark:bg-gray-400 text-gray-900 dark:text-gray-200 text-sm"
          >
            {{ genre.name }}
          </div>
        </div>
        <div class="grid grid-cols-2 gap-2 text-center">
          <div
            class="p-2 rounded-lg bg-gray-200 dark:bg-gray-700/50 border border-gray-300/80 dark:border-gray-600/40"
          >
            <span class="text-xs text-gray-500 dark:text-gray-400 font-medium"
              >Publicación
            </span>
            <p class="text-xs font-semibold text-gray-800 dark:text-gray-200">
              {{ review?.book?.first_publish_year }}
            </p>
          </div>
          <div
            class="p-2 rounded-lg bg-gray-200 dark:bg-gray-700/50 border border-gray-300/80 dark:border-gray-600/40"
          >
            <span class="text-xs text-gray-500 dark:text-gray-400 font-medium">
              Páginas</span
            >
            <p class="text-xs font-semibold text-gray-800 dark:text-gray-200">
              {{ review?.num_pages }}
            </p>
          </div>
          <div
            class="p-2 rounded-lg bg-gray-200 dark:bg-gray-700/50 border border-gray-300/80 dark:border-gray-600/40"
          >
            <span class="text-xs text-gray-500 dark:text-gray-400 font-medium"
              >Inicio de lectura</span
            >
            <p class="text-xs font-semibold text-gray-800 dark:text-gray-200">
              {{ review?.start_date || "Desconocida" }}
            </p>
          </div>
          <div
            class="p-2 rounded-lg bg-gray-200 dark:bg-gray-700/50 border border-gray-300/80 dark:border-gray-600/40"
          >
            <span class="text-xs text-gray-500 dark:text-gray-400 font-medium"
              >Fin de lectura</span
            >
            <p class="text-xs font-semibold text-gray-800 dark:text-gray-200">
              {{ review?.finish_date || "Desconocida" }}
            </p>
          </div>
        </div>
      </div>
    </div>
    <div
      v-if="review?.text_review?.trim()"
      class="mt-4 p-2 bg-sky-50/60 dark:bg-gray-700/40 border-l-4 rounded-r-xl border-y border-r border-sky-500 dark:border-gray-600"
    >
      <div>
        <h3 class="text-xs font-bold uppercase text-sky-600 dark:text-sky-400">
          Reseña
        </h3>
      </div>
      <div>
        <p
          class="mt-1 text-sm text-italic text-gray-700 dark:text-gray-400 leading-relaxed whitespace-pre-line"
        >
          "{{ review?.text_review }}"
        </p>
      </div>
    </div>
  </Modal>
</template>
