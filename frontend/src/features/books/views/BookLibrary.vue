<script setup>
import { useQuery } from "@tanstack/vue-query";
import Screen from "../../../components/Screen.vue";
import Select from "../../../components/Select.vue";
import { ORDER_BY_VALUES } from "../consts/booksConsts.js";
import { apiBooks } from "../services/apiBook.js";
import { computed, ref } from "vue";
import BookCard from "../components/BookCard.vue";
import { useDebounce } from "../../../debounce/useDebounce.js";
import { usePagination } from "../../../composables/usePagination.js";
import Pagination from "../../../components/Pagination.vue";
import ModalReviewBook from "../components/ModalReviewBook.vue";

const searchBookInLibrary = ref();
const debounceSearch = useDebounce(searchBookInLibrary, 500);
const reviews = computed(() => catalogBooks.value?.reviews || []);
const totalBooks = computed(() => catalogBooks.value?.total || 0);
const totalPages = computed(() => catalogBooks.value?.pages || 0);
const totalPagesRead = computed(
  () => catalogBooks.value?.total_pages_read || 0,
);
const reviewSelected = ref(null);
const isOpenModal = ref(false);

const { visiblePages, page, nextPage, prevPage, setPage } =
  usePagination(totalPages);

const { data: genreData, isFetching: isFetchingGenres } = useQuery({
  queryKey: ["genreslibraryBooks"],
  queryFn: apiBooks.getAllMyGenres,
});

const {
  data: catalogBooks,
  isFetching: isFetchingBooks,
  isLoading: isLoadingBooks,
} = useQuery({
  queryKey: ["catalogLibraryBooks", debounceSearch, page],
  queryFn: apiBooks.getMyCatalogLibraryBooks,
});

const genresValues = computed(() => {
  return (
    genreData.value?.map((item) => {
      const formattedName =
        item.name.charAt(0).toUpperCase() + item.name.slice(1);

      return {
        value: item.id,
        label: formattedName,
      };
    }) || []
  );
});

const openModal = () => {
  isOpenModal.value = true;
};

const openReview = (review) => {
  openModal();
  reviewSelected.value = review;
};
</script>

<template>
  <Screen class="dark:bg-black/90">
    <header class="p-4">
      <h2 class="text-3xl font-bold dark:text-white">Mi biblioteca</h2>
      <div
        class="flex items-center gap-1 text-gray-400 dark:text-gray-400 mt-0.5"
      >
        <p>{{ totalBooks }} libros</p>
        <p class="relative -top-1">.</p>
        <p>{{ totalPagesRead }} páginas</p>
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
    <div v-if="isLoadingBooks" class="text-black dark:text-white mt-4 ml-2">
      <p>Están cargando los libros...</p>
    </div>
    <section
      v-else
      class="grid grid-cols-[repeat(auto-fit,minmax(280px,1fr))] gap-3 mt-2 mx-2"
    >
      <BookCard
        v-for="review in reviews"
        :key="review.book.key"
        :book="review.book"
        actionText="Ver reseña"
        :class="{ 'opacity-50 pointer-events-none': isFetchingBooks }"
        @action="openReview(review)"
      />
    </section>
    <section
      v-if="totalPages > 1"
      class="flex justify-center items-center gap-4 mt-2"
    >
      <Pagination
        :currentPage="page"
        :totalPages="totalPages"
        :visiblePages="visiblePages"
        @next="nextPage"
        @prev="prevPage"
        @setPage="setPage"
      />
    </section>
    <ModalReviewBook :review="reviewSelected" v-model="isOpenModal" />
  </Screen>
</template>
