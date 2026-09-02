<script setup>
import { onMounted, ref, watchEffect } from "vue";
import { apiBooks } from "../services/apiBook";
import Screen from "../../../components/Screen.vue";

const trendingBooks = ref([]);

onMounted(async () => {
  const response = await apiBooks.getTrendingBooks();
  trendingBooks.value = response;
});
</script>

<template>
  <Screen>
    <section
      class="grid grid-cols-[repeat(auto-fit,minmax(280px,1fr))] gap-3 mt-2 mx-2"
    >
      <div
        v-for="book in trendingBooks"
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
