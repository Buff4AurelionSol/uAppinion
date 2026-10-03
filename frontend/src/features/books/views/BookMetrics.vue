<script setup>
import { computed, ref, watch } from "vue";
import Screen from "../../../components/Screen.vue";
import Select from "../../../components/Select.vue";
import { useQuery } from "@tanstack/vue-query";
import { apiBooks } from "../services/apiBook.js";
import { MONTH_NAMES, statusesValues } from "../consts/booksConsts.js";
import { useTheme } from "../../../const/useTheme.js";
import BarChart from "../../../components/BarChart.vue";

const filters = ref({
  year: "Todos",
  status: "read",
  first_date: "",
  end_date: "",
});

watch(
  () => filters.value.year,
  (newYear) => {
    if (newYear !== "Periodo personalizado") {
      filters.value.first_date = "";
      filters.value.end_date = "";
    }
  },
);

const { theme } = useTheme();
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

const isSingleYearSelected = computed(() => {
  const { year, first_date, end_date } = filters.value;

  if (year !== "Todos" && year !== "Periodo personalizado") {
    return true;
  }

  if (year === "Periodo personalizado" && first_date && end_date) {
    const auxFirstDate = first_date.slice(0, 4);
    const auxEndDate = end_date.slice(0, 4);
    return auxFirstDate === auxEndDate;
  }

  return false;
});

const subTitlePerPeriod = computed(() => {
  if (
    isCustomPeriod.value &&
    filters.value.first_date &&
    filters.value.end_date
  ) {
    return `${filters.value.first_date} al ${filters.value.end_date}`;
  }
  if (isSingleYearSelected.value) {
    return filters.value.year;
  }

  return "Todos los años";
});

const formatPeriodData = (periodArray, keyValueData = "total") => {
  const data = periodArray ?? [];

  if (isSingleYearSelected.value) {
    const monthData = new Array(12).fill(0);
    data.forEach((item) => {
      const monthIndex = parseInt(item?.period.slice(5, 7), 10);
      if (monthIndex >= 1 && monthIndex <= 12) {
        monthData[monthIndex - 1] = item[keyValueData] ?? 0;
      }
    });

    return {
      categories: MONTH_NAMES,
      seriesData: monthData,
    };
  }

  const categories = data.map((item) => item.period);
  const seriesData = data.map((item) => item[keyValueData] ?? 0);
  return { categories, seriesData };
};

const getBaseChartOptions = (categories) => {
  const textColor = theme.value === "dark" ? "#d1d5dc" : "#364153";

  return {
    chart: {
      type: "bar",
      toolbar: {
        show: false,
      },
    },
    plotOptions: {
      bar: {
        borderRadius: 4,
        horizontal: false,
      },
    },
    xaxis: {
      categories,
      labels: {
        style: {
          colors: textColor,
        },
      },
    },
    yaxis: {
      decimalsInFloat: 0,
      labels: {
        formatter: (value) => Math.floor(value),
        style: {
          colors: textColor,
        },
      },
    },
    grid: {
      show: false,
    },
  };
};

//LIBROS POR PERIODO
const processedBooksCharData = computed(() =>
  formatPeriodData(metricsData.value?.books_per_period, "total"),
);

const titlesBookPerPeriod = computed(() =>
  isSingleYearSelected.value ? "Libros por mes" : "Libros por año",
);

const bookChartSeries = computed(() => [
  {
    name: filters.value.status === "read" ? "Libros Leidos" : "Libros",
    data: processedBooksCharData.value.seriesData,
  },
]);

const bookChartOptions = computed(() =>
  getBaseChartOptions(processedBooksCharData.value.categories),
);

//PÁGINAS POR PERIODO
const processedPagesCharData = computed(() =>
  formatPeriodData(metricsData.value?.pages_per_period, "total_pages"),
);

const titlesPagesPerPeriod = computed(() =>
  isSingleYearSelected.value ? "Páginas por mes" : "Páginas por año",
);

const pagesChartSeries = computed(() => [
  {
    name: filters.value.status === "read" ? "Paginas Leidos" : "Páginas",
    data: processedPagesCharData.value.seriesData,
  },
]);

const pagesChartOptions = computed(() =>
  getBaseChartOptions(processedPagesCharData.value.categories),
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
        <section class="flex w-full gap-2 items-center">
          <div class="w-full flex flex-col md:flex-row gap-2">
            <article class="w-full">
              <div
                class="rounded-xl bg-gray-100 dark:bg-gray-600 border border-stone-300 dark:border-stone-800 p-5"
              >
                <p class="text-2xl font-bold text-black dark:text-white">
                  {{ metricsData?.total_books_read }}
                </p>
                <p class="text-sm text-gray-500 dark:text-gray-300">Libros</p>
              </div>
            </article>
            <article class="w-full">
              <div
                class="rounded-xl bg-gray-100 dark:bg-gray-600 border border-stone-300 dark:border-stone-800 p-5"
              >
                <p class="text-2xl font-bold text-black dark:text-white">
                  {{ metricsData?.total_pages_read }}
                </p>
                <p class="text-sm text-gray-500 dark:text-gray-300">Páginas</p>
              </div>
            </article>
          </div>
          <div class="w-full flex flex-col md:flex-row gap-2">
            <article class="w-full">
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
            <article class="w-full">
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
          </div>
        </section>
        <div class="flex gap-4 flex-col md:flex-row">
          <BarChart
            :mainTitle="titlesBookPerPeriod"
            :subTitle="subTitlePerPeriod"
            :series="bookChartSeries"
            :options="bookChartOptions"
            :isLoading="isLoadingMetrics"
          />
          <BarChart
            :mainTitle="titlesPagesPerPeriod"
            :subTitle="subTitlePerPeriod"
            :series="pagesChartSeries"
            :options="pagesChartOptions"
            :isLoading="isLoadingMetrics"
          />
        </div>
      </div>
    </div>
  </Screen>
</template>
