<script setup>
import { apiBooks } from "../services/apiBook";
import Modal from "../../../components/Modal.vue";
import Select from "../../../components/Select.vue";
import { formatsValues, statusesValues } from "../consts/booksConsts.js";
import { ref } from "vue";
const props = defineProps({
  title: String,
  first_publish_year: Number,
  cover_i: [String, Number],
});

const isOpenModal = defineModel();
const formBookReview = ref({
  status: "",
  format: "",
  num_pages: 0,
  text_review: "",
});
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
    <div class="grid grid-cols-3 items-start gap-3">
      <Select
        class="col-span-1"
        v-model="formBookReview.state"
        :values="statusesValues"
        labelSelect="Estado"
      />
      <Select
        class="col-span-1"
        v-model="formBookReview.format"
        :values="formatsValues"
        labelSelect="Formato"
      />
      <div
        class="col-start-3 row-span-4 w-24 h-40 shrink-0 rounded-md overflow-hidden relative justify-self-end"
      >
        <img
          v-if="props?.cover_i"
          :src="apiBooks.getImageUrl(props.cover_i, 'M')"
          :alt="props?.title"
          class="h-full w-full object-cover rounded-md absolute inset-0"
        />
      </div>
      <label class="relative col-span-1 row-start-2">
        <span class="text-black dark:text-white">Fecha de inicio</span>
        <input
          type="date"
          class="border w-full h-8 border-gray-300 dark:border-gray-400 focus:outline-gray-300 focus:outline-2 dark:focus:outline-gray-400 focus:outline-offset-2 p-3 rounded-md transition-all text-black dark:text-white dark:bg-gray-800 text-sm"
        />
      </label>
      <label class="relative col-span-1 row-start-2">
        <span class="text-black dark:text-white">Fecha de fin</span>
        <input
          type="date"
          class="border w-full h-8 border-gray-300 dark:border-gray-400 focus:outline-gray-300 focus:outline-2 dark:focus:outline-gray-400 focus:outline-offset-2 p-3 rounded-md transition-all text-black dark:text-white dark:bg-gray-800 text-sm"
        />
      </label>

      <label class="relative col-span-1 row-start-3">
        <input
          type="text"
          class="border w-full h-8 border-gray-300 dark:border-gray-400 focus:outline-gray-300 focus:outline-2 dark:focus:outline-gray-400 focus:outline-offset-2 p-3 rounded-md transition-all text-black dark:text-white dark:bg-gray-800 text-sm peer"
        />

        <span
          class="text-black dark:text-white absolute left-0 top-2 ml-3 tracking-wide pointer-events-none peer-focus:text-gray-400 peer-focus:text-sm peer-focus:-translate-y-5 duration-200 bg-white dark:bg-gray-800 text-sm"
          >N. Páginas</span
        >
      </label>
      <textarea
        placeholder="Agrega una reseña aquí... (opcional)"
        class="row-start-4 col-span-2 w-full min-h-24 max-h-44 border border-gray-300 dark:border-gray-400 focus:outline-gray-300 dark:focus:outline-gray-400 focus:outline-2 focus:outline-offset-2 p-3 rounded-md transition-all text-black dark:text-white resize-none field-sizing-content appearance-none dark:bg-gray-800 overflow-y-auto"
        autocomplete="off"
      ></textarea>

      <label
        class="col-span-1 row-start-3 cursor-pointer flex items-center self-center gap-2"
      >
        <input type="checkbox" class="w-4 h-4" />
        <span class="text-black dark:text-white text-sm">¿Es relectura?</span>
      </label>
    </div>
  </Modal>
</template>
