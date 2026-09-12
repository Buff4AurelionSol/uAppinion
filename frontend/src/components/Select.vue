<script setup>
const props = defineProps({
  labelSelect: {
    type: String,
    default: "",
  },
  values: {
    type: Object,
    default: () => ({}),
  },
});

const selectModelValue = defineModel();
</script>

<template>
  <label class="flex flex-col gap-1.5">
    <span class="text-black dark:text-white">{{ labelSelect }}</span>
    <select
      v-model="selectModelValue"
      class="w-full h-8 border border-gray-300 dark:border-gray-400 focus:outline-gray-300 dark:focus:outline-gray-400 focus:outline-2 focus:outline-offset-2 rounded-md transition-all text-black dark:text-white dark:bg-gray-800 px-2 py-1.5 text-sm"
    >
      <option
        v-for="(label, key) in values"
        :key="key"
        :value="key"
        class="text-sm"
      >
        {{ label }}
      </option>
    </select>
  </label>
</template>
