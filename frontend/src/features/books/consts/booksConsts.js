export const statusesValues = {
  read: "Leído",
  reading: "Leyendo",
  plan_to_read: "Quiero leer",
  dropped: "Abandonado",
};

export const formatsValues = {
  physical: "Físico",
  digital: "Digital",
  audio: "Audio",
};

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
