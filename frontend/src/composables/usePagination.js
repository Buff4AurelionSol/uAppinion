import { computed, ref } from "vue";

export function usePagination(totalPages, initialPage = 1) {
  const page = ref(initialPage);

  const prevPage = () => {
    if (page.value > 1) page.value--;
  };

  const nextPage = () => {
    if (page.value < totalPages.value) page.value++;
  };

  const setPage = (numberPage) => {
    if (numberPage >= 1 && numberPage <= totalPages.value) {
      page.value = numberPage;
    }
  };

  const visiblePages = computed(() => {
    const total = totalPages.value;
    const currentPage = page.value;

    if (total <= 1) return total === 1 ? [1] : [];

    const pages = [];
    const firsPage = 1;
    const lastPage = total;
    const previousPage = currentPage - 1;
    const next = currentPage + 1;

    pages.push(firsPage);

    if (Math.abs(previousPage - firsPage) > 1) {
      pages.push("...");
    }

    if (firsPage < prevPage) {
      pages.push(previousPage);
    }

    if (currentPage !== firsPage && currentPage !== lastPage) {
      pages.push(currentPage);
    }

    if (next < lastPage) {
      pages.push(next);
    }

    if (Math.abs(lastPage - next) > 1) {
      pages.push("...");
    }

    pages.push(lastPage);

    return pages;
  });

  return {
    page,
    visiblePages,
    prevPage,
    nextPage,
    setPage,
  };
}
