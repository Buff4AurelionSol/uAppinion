<script setup>
import { computed, onMounted, ref, watch, watchEffect } from "vue";
import { apiBooks } from "../services/apiBook";
import Screen from "../../../components/Screen.vue";
import { useDebounce } from "../../../debounce/useDebounce.js";
import { useQuery } from "@tanstack/vue-query";

const searchQuery = ref("");
const debounceSearch = useDebounce(searchQuery, 400);

const { data: trendingBooks, isLoading: isLoadingTrending } = useQuery({
  queryKey: ["books", "trending"],
  queryFn: apiBooks.getTrendingBooks,
  staleTime: 1000 * 60 * 5,
  enabled: computed(() => !debounceSearch.value.trim()),
});

const { data: searchBooks, isLoading: isLoadingSearch } = useQuery({
  queryKey: ["books", "search", debounceSearch],
  queryFn: () => apiBooks.searchBooks(debounceSearch.value),
  staleTime: 1000 * 60 * 5,
  enabled: computed(() => !!debounceSearch.value.trim()),
});

const isLoadingBooks = computed(
  () => isLoadingTrending.value || isLoadingSearch.value,
);

const booksToDisplay = computed(() => {
  return debounceSearch.value.trim()
    ? searchBooks.value || []
    : trendingBooks.value || [];
});
</script>

<template>
  <Screen>
    <section>
      <input
        placeholder="El señor de los anillos..."
        v-model="searchQuery"
        class="h-10 w-1/2 mt-2 border border-gray-300 focus:outline-gray-300 focus:outline-2 focus:outline-offset-2 ml-2 p-2 rounded-md transition-all"
      />
    </section>
    <div v-if="isLoadingBooks">
      <p>Están cargando los libros...</p>
    </div>
    <section
      v-else
      class="grid grid-cols-[repeat(auto-fit,minmax(280px,1fr))] gap-3 mt-2 mx-2"
    >
      <div
        v-for="book in booksToDisplay"
        :key="book.key"
        class="flex gap-1.5 h-40 bg-gray-200 rounded-lg p-2 overflow-hidden"
      >
        <div class="w-24 h-full shrink-0 bg-gray-300 rounded-mdoverflow-hidden">
          <img
            v-if="book?.cover_i"
            :src="apiBooks.getImageUrl(book.cover_i, 'M')"
            :alt="book?.title"
            class="h-full w-full object-cover rounded-md"
          />
        </div>
        <div class="flex flex-col justify-between">
          <div class="flex gap-2">
            <h2
              v-for="author in book.author_name"
              :key="author"
              class="text-gray-700"
            >
              {{ author }}
            </h2>
          </div>
          <h2 class="font-bold line-clamp-2 leading-tight">
            {{ book?.title }}
          </h2>
          <h2 class="text-gray-500">{{ book?.first_publish_year }}</h2>
        </div>
      </div>
    </section>
  </Screen>
</template>
