<script setup>
import { computed, onMounted, ref, watch, watchEffect } from "vue";
import { apiBooks } from "../services/apiBook";
import Screen from "../../../components/Screen.vue";
import { useDebounce } from "../../../debounce/useDebounce.js";
import { keepPreviousData, useQuery } from "@tanstack/vue-query";

const searchQuery = ref("");
const debounceSearch = useDebounce(searchQuery, 500);
const page = ref(1);

const { data: trendingBooks, isLoading: isLoadingTrending } = useQuery({
  queryKey: ["books", "trending"],
  queryFn: apiBooks.getTrendingBooks,
  staleTime: 1000 * 60 * 5,
  enabled: computed(() => !debounceSearch.value.trim()),
});

const {
  data: searchBooks,
  isLoading: isLoadingSearch,
  isFetching: isFetchingSearch,
} = useQuery({
  queryKey: ["books", "search", debounceSearch, page],
  queryFn: () => apiBooks.searchBooks(debounceSearch.value, page.value, 12),
  staleTime: 1000 * 60 * 5,
  enabled: computed(() => !!debounceSearch.value.trim()),
  placeholderData: keepPreviousData,
});

const isLoadingBooks = computed(
  () => isLoadingTrending.value || isLoadingSearch.value,
);

const booksToDisplay = computed(() => {
  return debounceSearch.value.trim()
    ? searchBooks.value?.data || []
    : trendingBooks.value || [];
});

const totalPages = computed(() => searchBooks.value?.totalPages || 0);

const prevPage = () => {
  if (page.value > 1) page.value--;
};

const nextPage = () => {
  if (page.value < totalPages.value) page.value++;
};

watch(debounceSearch, () => {
  page.value = 1;
});
</script>

<template>
  <Screen class="dark:bg-black/90">
    <section>
      <input
        placeholder="El señor de los anillos..."
        v-model="searchQuery"
        class="h-10 w-1/2 mt-2 border border-gray-300 dark:border-gray-400 focus:outline-gray-300 dark:focus:outline-gray-400 focus:outline-2 focus:outline-offset-2 ml-2 p-2 rounded-md transition-all text-black dark:text-white"
      />
    </section>
    <div v-if="isLoadingBooks" class="text-black dark:text-white mt-4 ml-2">
      <p>Están cargando los libros...</p>
    </div>
    <section
      v-else
      class="grid grid-cols-[repeat(auto-fit,minmax(280px,1fr))] gap-3 mt-2 mx-2"
    >
      <div
        v-for="book in booksToDisplay"
        :key="book.key"
        class="flex gap-1.5 h-40 bg-gray-200 dark:bg-gray-600 rounded-lg p-2 overflow-hidden"
        :class="{ 'opaccity-50 pointer-events-none': isFetchingSearch }"
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
        <div class="flex flex-col justify-between min-w-0">
          <h2
            class="font-bold line-clamp-2 leading-tight text-black dark:text-white"
          >
            {{ book?.title }}
          </h2>
          <p class="text-sm text-gray-700 dark:text-gray-400 mt-1 truncate">
            {{ book?.author_name?.join(", ") || "Autor Desconocido." }}
          </p>

          <div class="mt-auto">
            <span
              class="bg-gray-300 px-2 py-1 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md text-xs w-fit"
            >
              {{ book?.first_publish_year || "Año desconocido" }}
            </span>
          </div>
        </div>
      </div>
    </section>
    <section
      v-if="debounceSearch.trim() && totalPages > 1"
      class="flex justify-center items-center gap-4 mt-2"
    >
      <button
        @click="prevPage"
        :disabled="page === 1"
        class="bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-black dark:text-white py-2 px-4 rounded-sm disabled:opacity-50 transition-colors duration-300"
      >
        Anterior
      </button>
      <span class="text-black dark:text-white"
        >{{ page }} - {{ totalPages }}</span
      >
      <button
        @click="nextPage"
        :disabled="page === totalPages"
        class="bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-black dark:text-white py-2 px-4 rounded-sm disabled:opacity-50 transition-colors duration-300"
      >
        Siguiente
      </button>
    </section>
  </Screen>
</template>
