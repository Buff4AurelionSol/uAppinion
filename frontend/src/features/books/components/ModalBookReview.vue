<script setup>
import { apiBooks } from "../services/apiBook";
import Modal from "../../../components/Modal.vue";
import Select from "../../../components/Select.vue";
import {
  formatsValues,
  INITIAL_REVIEW_FORM,
  requiredFields,
  statusesValues,
} from "../consts/booksConsts.js";
import { computed, ref, watch, watchEffect } from "vue";
import { useQuery } from "@tanstack/vue-query";
const props = defineProps({
  bookKey: String,
  title: String,
  first_publish_year: Number,
  cover_i: [String, Number],
});

const isOpenModal = defineModel();
const formBookReview = ref({ ...INITIAL_REVIEW_FORM });

const { data: genresBook, isLoading } = useQuery({
  queryKey: ["genres", () => props.bookKey],
  queryFn: () => apiBooks.getGenresByBook(props.bookKey),
  enabled: computed(() => !!props.bookKey && isOpenModal.value),
});

const buildReviewPayload = (formData, bookProps) => {
  return {
    id: crypto.randomUUID(),
    status: formData.status,
    num_pages: Number(formData.num_pages),
    start_date: formData.start_date ? formData.start_date : null,
    finish_date: formData.finish_date ? formData.finish_date : null,
    is_read: formData.is_read,
    text_review: formData.text_review,
    book: {
      key: bookProps.bookKey,
      title: bookProps.title,
      first_publish_year: bookProps.first_publish_year,
      cover_i: bookProps.cover_i,
      genres: genresBook.value,
    },
  };
};

const sendBookReview = async () => {
  const isAnyRequiredEmpty = requiredFields.some(
    (field) => !formBookReview.value[field],
  );

  if (isAnyRequiredEmpty) {
    console.log("Faltan campos por llenar");
    return;
  }

  const dataToSend = buildReviewPayload(formBookReview.value, props);

  try {
    const response = await fetch("http://127.0.0.1:8000/books/catalog", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(dataToSend),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Detalle del error del backend:", errorData);
      throw new Error(`Error del servidor: ${response.status}`);
    }

    const result = await response.json();
    console.log("Guardado con exito", result);
  } catch (e) {
    console.error("Error en la petición:", e);
  }
};

watch(isOpenModal, (isOpen) => {
  if (!isOpen) {
    formBookReview.value = { ...INITIAL_REVIEW_FORM };
  }
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
    <form @submit.prevent="sendBookReview">
      <div class="grid grid-cols-3 items-start gap-3">
        <Select
          class="col-span-1"
          v-model="formBookReview.status"
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
            v-model="formBookReview.start_date"
            type="date"
            class="border w-full h-8 border-gray-300 dark:border-gray-400 focus:outline-gray-300 focus:outline-2 dark:focus:outline-gray-400 focus:outline-offset-2 p-3 rounded-md transition-all text-black dark:text-white dark:bg-gray-800 text-sm"
          />
        </label>
        <label class="relative col-span-1 row-start-2">
          <span class="text-black dark:text-white">Fecha de fin</span>
          <input
            v-model="formBookReview.finish_date"
            type="date"
            class="border w-full h-8 border-gray-300 dark:border-gray-400 focus:outline-gray-300 focus:outline-2 dark:focus:outline-gray-400 focus:outline-offset-2 p-3 rounded-md transition-all text-black dark:text-white dark:bg-gray-800 text-sm"
          />
        </label>

        <label class="relative col-span-1 row-start-3">
          <input
            v-model="formBookReview.num_pages"
            type="number"
            class="border w-full h-8 border-gray-300 dark:border-gray-400 focus:outline-gray-300 focus:outline-2 dark:focus:outline-gray-400 focus:outline-offset-2 p-3 rounded-md transition-all text-black dark:text-white dark:bg-gray-800 text-sm peer"
          />

          <span
            class="text-black dark:text-white absolute left-0 top-2 ml-3 tracking-wide pointer-events-none peer-focus:text-gray-400 peer-focus:text-sm peer-focus:-translate-y-5 duration-200 bg-white dark:bg-gray-800 text-sm"
            >N. Páginas</span
          >
        </label>
        <textarea
          v-model="formBookReview.text_review"
          placeholder="Agrega una reseña aquí... (opcional)"
          class="row-start-4 col-span-2 w-full min-h-24 max-h-44 border border-gray-300 dark:border-gray-400 focus:outline-gray-300 dark:focus:outline-gray-400 focus:outline-2 focus:outline-offset-2 p-3 rounded-md transition-all text-black dark:text-white resize-none field-sizing-content appearance-none dark:bg-gray-800 overflow-y-auto"
          autocomplete="off"
        ></textarea>

        <label
          class="col-span-1 row-start-3 cursor-pointer flex items-center self-center gap-2"
        >
          <input
            type="checkbox"
            class="w-4 h-4"
            v-model="formBookReview.is_read"
          />
          <span class="text-black dark:text-white text-sm">¿Es relectura?</span>
        </label>
        <div class="col-span-2">
          <button
            type="submit"
            class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded-md transition-colors text-sm"
          >
            Guardar Reseña
          </button>
        </div>
      </div>
    </form>
  </Modal>
</template>
