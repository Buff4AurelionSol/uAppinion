<script setup>
import { apiBooks } from "../services/apiBook";
import Modal from "../../../components/Modal.vue";
const props = defineProps({
  title: String,
  first_publish_year: Number,
  cover_i: [String, Number],
});

const isOpenModal = defineModel();
</script>

<template>
  <Modal v-model="isOpenModal">
    <div class="flex items-baseline mb-3 gap-2">
      <h3 class="text-black dark:text-white font-bold text-xl leading-tight">
        {{ props?.title }}
      </h3>
      <span class="text-gray-500 dark:text-gray-400 text-lg shrink-0">
        {{ props?.first_publish_year }}
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
          v-if="props?.cover_i"
          :src="apiBooks.getImageUrl(props.cover_i, 'M')"
          :alt="props?.title"
          class="h-full w-full object-cover rounded-md absolute inset-0"
        />
      </div>
    </div>
  </Modal>
</template>
