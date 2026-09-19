<script setup>
import { useQuery } from "@tanstack/vue-query";
import Screen from "../../../components/Screen.vue";
import Select from "../../../components/Select.vue";
import { ORDER_BY_VALUES } from "../consts/booksConsts.js";
import { apiBooks } from "../services/apiBook.js";
import { computed } from "vue";

const { data: genres, isFetching: isFetchingGenres } = useQuery({
  queryKey: ["libraryBooks"],
  queryFn: apiBooks.getAllMyGenres,
});

const genresValues = computed(() => {
  return (
    genres.value?.map((item) => {
      const formattedName =
        item.name.charAt(0).toUpperCase() + item.name.slice(1);

      return {
        value: item.id,
        label: formattedName,
      };
    }) || []
  );
});
</script>

<template>
  <Screen class="dark:bg-black/90">
    <header class="p-4">
      <h2 class="text-3xl font-bold dark:text-white">Mi biblioteca</h2>
      <div
        class="flex items-center gap-1 text-gray-400 dark:text-gray-400 mt-0.5"
      >
        <p>20 libros</p>
        <p class="relative -top-1">.</p>
        <p>8494 páginas</p>
      </div>
      <div class="flex gap-2 items-center mt-2">
        <input
          placeholder="Buscar por título o autor"
          class="h-10 flex-1 w-full border border-gray-300 dark:border-gray-400 focus:outline-gray-300 dark:focus:outline-gray-400 focus:outline-2 focus:outline-offset-2 p-2 rounded-md transition-all text-black dark:text-white dark:bg-gray-800"
        />
        <Select :values="genresValues" labelSelect="" class="w-56 h-10" />
        <Select :values="ORDER_BY_VALUES" labelSelect="" class="w-56 h-10" />
      </div>
    </header>
  </Screen>
</template>
