<script setup>
import { computed } from "vue";

const props = defineProps({
  topData: {
    type: Array,
    default: () => [],
  },
  title: {
    type: String,
    required: true,
  },
  subTitle: {
    type: String,
    default: "",
  },
  valueKey: {
    type: String,
    default: "total_pages",
  },
});

const maxValue = computed(() => {
  if (!props.topData.length) return 1;
  return Math.max(
    ...props.topData.map((item) => Number(item?.[props.valueKey] || 0)),
    1,
  );
});

const getMyPercentage = (item) => {
  const value = Number(item?.[props.valueKey] || 0);
  return Math.min((value / maxValue.value) * 100, 100);
};
</script>

<template>
  <section
    class="flex flex-col w-full bg-gray-100 dark:bg-gray-600 border border-gray-300 dark:border-gray-600 rounded-xl p-4"
  >
    <header>
      <div>
        <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200">
          {{ title }}
        </h3>
      </div>
      <div>
        <h4 class="text-md text-gray-400 dark:text-gray-400">{{ subTitle }}</h4>
      </div>
    </header>

    <div v-if="!topData.length">
      <p>No hay datos disponibles</p>
    </div>

    <div v-else class="flex flex-col w-full gap-3 mt-2">
      <div
        v-for="(item, index) in topData"
        class="flex gap-4 items-start"
        :key="index"
      >
        <div class="text-gray-500 dark:text-gray-400 w-6 font-medium shrink-0">
          {{ index + 1 }}
        </div>
        <div class="flex flex-col w-full">
          <div class="flex justify-between w-full">
            <slot name="valuesTop" :item="item" :index="index">
              <span>{{ item?.name }}</span>
            </slot>
          </div>

          <div
            class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden"
          >
            <div
              class="h-full bg-blue-400 rounded-full transition-all duration-500 ease-out"
              :style="{ width: `${getMyPercentage(item)}%` }"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
