export const statusesValues = [
  { value: "read", label: "Leído" },
  { value: "reading", label: "Leyendo" },
  { value: "plan_to_read", label: "Quiero leer" },
  { value: "dropped", label: "Abandonado" },
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

const GENRES_VALUES = {};

export const ORDER_BY_VALUES = [
  { value: "created_at", label: "Más recientes" },
  { value: "title_asc", label: "Título A-Z" },
  { value: "date", label: "Fecha" },
];
