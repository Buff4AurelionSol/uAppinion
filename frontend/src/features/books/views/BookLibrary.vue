<script setup>
import { computed, ref, watch } from "vue";
import { apiBooks } from "../services/apiBook";
import Screen from "../../../components/Screen.vue";
import { useDebounce } from "../../../debounce/useDebounce.js";
import { keepPreviousData, useQuery } from "@tanstack/vue-query";
import Modal from "../../../components/Modal.vue";

const searchQuery = ref("");
const debounceSearch = useDebounce(searchQuery, 500);
const page = ref(1);
const isOpenModal = ref(false);
const bookSelected = ref(null);

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

const visiblePages = computed(() => {
  const total = totalPages.value;
  const currentPage = page.value;

  if (total <= 1) return total === 1 ? [1] : [];

  const pages = [];
  const firstPage = 1;
  const lastPage = total;
  const previousPage = currentPage - 1;
  const nextPage = currentPage + 1;

  pages.push(firstPage);

  if (Math.abs(firstPage - previousPage) > 1) {
    pages.push("...");
  }

  if (firstPage < previousPage) {
    pages.push(previousPage);
  }

  if (currentPage !== firstPage && currentPage !== lastPage) {
    pages.push(currentPage);
  }

  if (nextPage < lastPage) {
    pages.push(nextPage);
  }

  if (Math.abs(nextPage - lastPage) > 1) {
    pages.push("...");
  }

  pages.push(lastPage);

  return pages;
});

const goToPage = (numberPage) => {
  if (numberPage >= 1 && numberPage <= totalPages.value) {
    page.value = numberPage;
  }
};

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
      <div
        v-for="book in booksToDisplay"
        :key="book.key"
        class="flex gap-1.5 h-40 bg-gray-200 dark:bg-gray-600 rounded-lg p-2 overflow-hidden"
        :class="{ 'opacity-50 pointer-events-none': isFetchingSearch }"
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
              @click="openReview(book)"
              class="bg-sky-500 hover:bg-sky-400 dark:bg-sky-700 dark:hover:bg-sky-600 px-2 py-1 rounded-md text-white font-semibold text-sm"
            >
              Reseñar
            </button>
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
      <template v-for="(p, i) in visiblePages">
        <button
          v-if="p !== '...'"
          :key="'btn-' + i"
          @click="goToPage(p)"
          class="px-2 py-2 bg-gray-200 dark:bg-gray-600 text-black dark:text-white rounded-md transition-colors duration-300"
          :class="p === page ? 'bg-sky-400 text-white dark:bg-sky-800' : ''"
        >
          {{ p }}
        </button>

        <span
          v-else
          :key="'dots-' + i"
          class="px-2 py-2 bg-gray-200 dark:bg-gray-600 text-black dark:text-white rounded-md select-none transition-colors duration-300"
        >
          {{ p }}
        </span>
      </template>

      <button
        @click="nextPage"
        :disabled="page === totalPages"
        class="bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-black dark:text-white py-2 px-4 rounded-sm disabled:opacity-50 transition-colors duration-300"
      >
        Siguiente
      </button>
    </section>
    <Modal v-model="isOpenModal">
      <div class="flex items-baseline mb-3 gap-2">
        <h3 class="text-black dark:text-white font-bold text-xl leading-tight">
          {{ bookSelected?.title }}
        </h3>
        <span class="text-gray-500 dark:text-gray-400 text-lg shrink-0">
          {{ bookSelected?.first_publish_year }}
        </span>
      </div>
      <div class="flex items-start gap-6 mt-4">
        <div class="flex flex-1 flex-col gap-2">
          <label class="relative w-full">
            <input
              type="text"
              class="border w-full border-gray-300 dark:border-gray-400 focus:outline-gray-300 focus:outline-2 dark:focus:outline-gray-400 focus:outline-offset-2 p-3 rounded-md transition-all text-black dark:text-white dark:bg-gray-800 peer"
            />

            <span
              class="text-black dark:text-white absolute left-0 top-2 ml-3 tracking-wide pointer-events-none peer-focus:text-gray-400 peer-focus:text-sm peer-focus:-translate-y-5 duration-200 bg-white dark:bg-gray-800"
              >Número de páginas</span
            >
          </label>
          <textarea
            placeholder="Agrega una reseña"
            class="w-full min-h-24 max-h-44 border border-gray-300 dark:border-gray-400 focus:outline-gray-300 dark:focus:outline-gray-400 focus:outline-2 focus:outline-offset-2 p-3 rounded-md transition-all text-black dark:text-white resize-none field-sizing-content appearance-none dark:bg-gray-800 overflow-y-auto"
            autocomplete="off"
          >
          </textarea>
        </div>
        <div class="w-24 h-40 shrink-0 rounded-md overflow-hidden relative">
          <img
            v-if="bookSelected?.cover_i"
            :src="apiBooks.getImageUrl(bookSelected.cover_i, 'M')"
            :alt="bookSelected?.title"
            class="h-full w-full object-cover rounded-md absolute inset-0"
          />
        </div>
      </div>
    </Modal>
  </Screen>
</template>
