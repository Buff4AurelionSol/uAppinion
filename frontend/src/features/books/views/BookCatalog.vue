<script setup>
import { computed, ref, watch } from "vue";
import { apiBooks } from "../services/apiBook";
import Screen from "../../../components/Screen.vue";
import { useDebounce } from "../../../debounce/useDebounce.js";
import { keepPreviousData, useQuery } from "@tanstack/vue-query";
import BookCard from "../components/BookCard.vue";
import { usePagination } from "../../../composables/usePagination.js";
import Pagination from "../../../components/Pagination.vue";
import ModalBookReviewForm from "../components/ModalBookReviewForm.vue";

const searchQuery = ref("");
const debounceSearch = useDebounce(searchQuery, 500);
const isOpenModal = ref(false);
const bookSelected = ref(null);

const totalPagesRef = computed(() => searchBooks.value?.totalPages || 0);

const { visiblePages, page, nextPage, prevPage, setPage } =
  usePagination(totalPagesRef);

const {
  data: trendingBooks,
  isLoading: isLoadingTrending,
  isError: isErrorTrending,
} = useQuery({
  queryKey: ["books", "trending"],
  queryFn: apiBooks.getTrendingBooks,
  staleTime: 1000 * 60 * 10,
  enabled: computed(() => !debounceSearch.value.trim()),
});

const {
  data: searchBooks,
  isLoading: isLoadingSearch,
  isFetching: isFetchingSearch,
  isError: isErrorSearch,
} = useQuery({
  queryKey: ["books", "search", debounceSearch, page],
  queryFn: () => apiBooks.searchBooks(debounceSearch.value, page.value, 12),
  staleTime: 1000 * 60 * 10,
  enabled: computed(() => !!debounceSearch.value.trim()),
  placeholderData: keepPreviousData,
});

const isLoadingBooks = computed(() => {
  return debounceSearch.value.trim()
    ? isLoadingSearch.value
    : isLoadingTrending.value;
});

const isErrorBooks = computed(() => {
  return debounceSearch.value.trim()
    ? isErrorSearch.value
    : isErrorTrending.value;
});
const booksToDisplay = computed(() => {
  return debounceSearch.value.trim()
    ? searchBooks.value?.data || []
    : trendingBooks.value || [];
});

watch(debounceSearch, () => {
  setPage(1);
});

const openModal = () => {
  isOpenModal.value = true;
};

const openReview = (book) => {
  openModal();
  bookSelected.value = book;
};

watch(isOpenModal, (isOpen) => {
  if (!isOpen) bookSelected.value = null;
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

    <div v-else-if="isErrorBooks" class="text-red-500 mt-4 ml-2">
      <p v-if="debounceSearch.trim()">
        Error con el servidor al buscar los libros.
      </p>
      <p v-else>Error al traer los libros del servidor.</p>
    </div>
    <section
      v-else
      class="grid grid-cols-[repeat(auto-fit,minmax(280px,1fr))] gap-3 mt-2 mx-2"
    >
      <BookCard
        v-for="book in booksToDisplay"
        :key="book.key"
        :book="book"
        :class="{ 'opacity-50 pointer-events-none': isFetchingSearch }"
        @action="openReview(book)"
      />
    </section>
    <section
      v-if="debounceSearch.trim() && totalPagesRef > 1"
      class="flex justify-center items-center gap-4 mt-2"
    >
      <Pagination
        :currentPage="page"
        :totalPages="totalPagesRef"
        :visiblePages="visiblePages"
        @prev="prevPage"
        @next="nextPage"
        @setPage="setPage"
      />
    </section>
    <ModalBookReviewForm
      :bookKey="bookSelected?.key"
      :title="bookSelected?.title"
      :first_publish_year="bookSelected?.first_publish_year"
      :cover_i="bookSelected?.cover_i"
      :authors="bookSelected?.author_name"
      v-model="isOpenModal"
    />
  </Screen>
</template>
