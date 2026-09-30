<script setup>
import { computed, ref, watch } from "vue";
import Screen from "../../../components/Screen.vue";
import Select from "../../../components/Select.vue";
import { useQuery } from "@tanstack/vue-query";
import { apiBooks } from "../services/apiBook.js";
import { statusesValues } from "../consts/booksConsts.js";

const filters = ref({
  year: "Todos",
  status: "read",
  first_date: "",
  end_date: "",
});

const cleanFiltersParams = computed(() => {
  const params = { status: filters.value.status };

  if (filters.value.year === "Todos") return params;
  if (filters.value.year === "Periodo personalizado") {
    return {
      ...params,
      first_date: filters.value.first_date,
      end_date: filters.value.end_date,
    };
  }

  return { ...params, year: filters.value.year };
});

const isQueryEnabled = computed(() => {
  if (filters.value.year === "Periodo personalizado") {
    return !!(filters.value.first_date && filters.value.end_date);
  }

  return true;
});

const { data: years, isLoading: loadingYears } = useQuery({
  queryKey: ["readingYears"],
  queryFn: apiBooks.getMyYearsReaded,
});

const { data: metricsData, isLoading: isLoadingMetrics } = useQuery({
  queryKey: ["myMetricsBooks", cleanFiltersParams],
  queryFn: () => apiBooks.getMyMetrics(cleanFiltersParams.value),
  enabled: isQueryEnabled,
});

const yearWithAll = computed(() => {
  return ["Todos", ...(years.value ?? []), "Periodo personalizado"];
});

const isCustomPeriod = computed(
  () => filters.value.year === "Periodo personalizado",
);
</script>

<template>
  <Screen class="dark:bg-black/90 bg-gray-100">
    <div class="flex flex-col">
      <header class="p-4">
        <h2 class="text-3xl font-semibold text-gray-800 dark:text-gray-100">
          Métricas de mis libros
        </h2>
        <p class="text-md font-light text-gray-600 dark:text-gray-300">
          Analiza tus hábitos de consumo a lo largo del tiempo
        </p>
      </header>
      <div class="flex flex-col px-4 py-2 gap-6">
        <section
          class="flex p-4 w-full bg-gray-100 dark:bg-gray-600 border border-stone-300 dark:border-gray-800 rounded-lg items-end gap-4"
        >
          <div class="w-48">
            <Select
              labelSelect="Año"
              v-model="filters.year"
              :values="yearWithAll"
            />
          </div>
          <div class="w-48">
            <Select
              labelSelect="Estado"
              v-model="filters.status"
              :values="statusesValues"
            />
          </div>
          <div class="flex flex-col gap-1">
            <label
              class="text-xs font-medium"
              :class="
                isCustomPeriod
                  ? 'text-gray-700 dark:text-gray-300'
                  : 'text-gray-300 dark:text-gray-400'
              "
              >Desde</label
            >
            <input
              type="date"
              v-model="filters.first_date"
              :disabled="!isCustomPeriod"
              class="h-10 w-full border border-gray-300 dark:border-gray-400 focus:outline-gray-300 dark:focus:outline-gray-400 focus:outline-2 focus:outline-offset-2 p-2 rounded-md transition-all text-black dark:text-white dark:bg-gray-800 disabled:bg-gray-200 dark:disabled:bg-gray-500 disabled:text-gray-400 disabled:border-gray-200 dark:disabled:border-gray-500"
            />
          </div>
          <div class="flex flex-col gap-1">
            <label
              class="text-xs font-medium"
              :class="
                isCustomPeriod
                  ? 'text-gray-700 dark:text-gray-300'
                  : 'text-gray-300 dark:text-gray-400'
              "
              >Hasta</label
            >
            <input
              type="date"
              v-model="filters.end_date"
              :disabled="!isCustomPeriod"
              class="h-10 w-full border border-gray-300 dark:border-gray-400 focus:outline-gray-300 dark:focus:outline-gray-400 focus:outline-2 focus:outline-offset-2 p-2 rounded-md transition-all text-black dark:text-white dark:bg-gray-800 disabled:bg-gray-200 dark:disabled:bg-gray-500 disabled:text-gray-400 disabled:border-gray-200 dark:disabled:border-gray-500"
            />
          </div>
        </section>
        <section class="flex w-full gap-4 items-center">
          <article class="w-1/4">
            <div
              class="rounded-xl bg-gray-100 dark:bg-gray-600 border border-stone-300 dark:border-stone-800 p-5"
            >
              <p class="text-2xl font-bold text-black dark:text-white">
                {{ metricsData?.total_books_read }}
              </p>
              <p class="text-sm text-gray-500 dark:text-gray-300">Libros</p>
            </div>
          </article>
          <article class="w-1/4">
            <div
              class="rounded-xl bg-gray-100 dark:bg-gray-600 border border-stone-300 dark:border-stone-800 p-5"
            >
              <p class="text-2xl font-bold text-black dark:text-white">
                {{ metricsData?.total_pages_read }}
              </p>
              <p class="text-sm text-gray-500 dark:text-gray-300">Páginas</p>
            </div>
          </article>
          <article class="w-1/4">
            <div
              class="rounded-xl bg-gray-100 dark:bg-gray-600 border border-stone-300 dark:border-stone-800 p-5"
            >
              <p class="text-2xl font-bold text-black dark:text-white">
                {{ metricsData?.average_pages_read }}
              </p>
              <p class="text-sm text-gray-500 dark:text-gray-300">
                Promedio de páginas
              </p>
            </div>
          </article>
          <article class="w-1/4">
            <div
              class="rounded-xl bg-gray-100 dark:bg-gray-600 border border-stone-300 dark:border-stone-800 p-5"
            >
              <p class="text-2xl font-bold text-black dark:text-white">
                {{ metricsData?.total_time_read }}
              </p>
              <p class="text-sm text-gray-500 dark:text-gray-300">
                Años de lectura
              </p>
            </div>
          </article>
        </section>
      </div>
    </div>
  </Screen>
</template>
