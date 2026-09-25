export const statusesValues = [
  {
    value: "read",
    label: "Leído",
    classes:
      "text-sm bg-emerald-100 text-emerald-800 dark:bg-emerald-500/20 dark:text-emerald-300",
  },
  {
    value: "reading",
    label: "Leyendo",
    classes:
      "text-sm bg-amber-100 text-amber-800 dark:bg-amber-500/20 dark:text-amber-300",
  },
  {
    value: "plan_to_read",
    label: "Quiero leer",
    classes:
      "text-sm bg-gray-300 text-gray-700 dark:bg-gray-700 dark:text-gray-300",
  },
  {
    value: "dropped",
    label: "Abandonado",
    classes:
      "text-sm bg-rose-100 text-rose-800 dark:bg-rose-500/20 dark:text-rose-300",
  },
];

export const formatsValues = [
  { value: "physical", label: "Físico" },
  { value: "digital", label: "Digital" },
  { value: "audio", label: "Audio" },
];

export const requiredFields = ["status", "num_pages"];

export const INITIAL_REVIEW_FORM = {
  status: "",
  format: "",
  start_date: "",
  finish_date: "",
  num_pages: "",
  text_review: "",
  is_read: false,
};

export const ORDER_BY_VALUES = [
  { value: "created_at", label: "Más recientes" },
  { value: "title_asc", label: "Título A-Z" },
  { value: "date", label: "Fecha" },
];
