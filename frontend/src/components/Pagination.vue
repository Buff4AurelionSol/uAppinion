<script setup>
defineProps({
  currentPage: {
    type: Number,
    required: true,
  },
  totalPages: {
    type: Number,
    required: true,
  },
  visiblePages: {
    type: Array,
    required: true,
  },
});

const emit = defineEmits(["prev", "next", "setPage"]);
</script>

<template>
  <button
    @click="$emit('prev')"
    :disabled="currentPage === 1"
    class="bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-black dark:text-white py-2 px-4 rounded-sm disabled:opacity-50 transition-colors duration-300"
  >
    Anterior
  </button>
  <template v-for="(p, i) in visiblePages">
    <button
      v-if="p !== '...'"
      :key="'btn-' + i"
      @click="$emit('setPage', p)"
      class="px-2 py-2 bg-gray-200 dark:bg-gray-600 text-black dark:text-white rounded-md transition-colors duration-300"
      :class="p === currentPage ? 'bg-sky-400 text-white dark:bg-sky-800' : ''"
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
    @click="$emit('next')"
    :disabled="currentPage === totalPages"
    class="bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-black dark:text-white py-2 px-4 rounded-sm disabled:opacity-50 transition-colors duration-300"
  >
    Siguiente
  </button>
</template>
