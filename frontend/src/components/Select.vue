<script setup>
const props = defineProps({
  labelSelect: {
    type: String,
    default: "",
  },
  values: {
    type: Array,
    default: () => [],
  },
});

const selectModelValue = defineModel();
</script>

<template>
  <label class="flex flex-col gap-1.5">
    <span
      v-if="labelSelect"
      class="text-xs font-medium text-gray-600 dark:text-gray-300"
      >{{ labelSelect }}</span
    >
    <select
      v-model="selectModelValue"
      class="w-full h-full border border-gray-300 dark:border-gray-400 focus:outline-gray-300 dark:focus:outline-gray-400 focus:outline-2 focus:outline-offset-2 rounded-md transition-all text-black dark:text-white dark:bg-gray-800 px-2 py-1.5 text-sm"
    >
      <option
        v-for="item in values"
        :key="typeof item === 'object' ? item.value : item"
        :value="typeof item === 'object' ? item.value : item"
        class="text-sm"
      >
        {{ typeof item === "object" ? item.label : item }}
      </option>
    </select>
  </label>
</template>
