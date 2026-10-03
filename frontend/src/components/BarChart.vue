<script setup>
defineProps({
  mainTitle: {
    type: String,
    required: true,
  },
  subTitle: {
    type: [String, Number],
    default: "",
  },
  series: {
    type: Array,
    required: true,
  },
  options: {
    type: Object,
    required: true,
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
});
</script>

<template>
  <section
    class="flex flex-col w-full bg-gray-100 dark:bg-gray-600 border border-gray-300 dark:border-gray-600 rounded-xl p-4"
  >
    <header class="flex flex-col gap-2">
      <div>
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200">
          {{ mainTitle }}
        </h3>
      </div>
      <div>
        <h4 class="text-md text-gray-400 dark:text-gray-400">{{ subTitle }}</h4>
      </div>
    </header>
    <div class="w-full">
      <div
        v-if="isLoading"
        class="text-sm font-medium text-gray-500 dark:text-gray-500"
      >
        Cargando gráfica...
      </div>

      <apexchart
        v-else
        width="100%"
        height="200"
        type="bar"
        :options="options"
        :series="series"
      ></apexchart>
    </div>
  </section>
</template>
