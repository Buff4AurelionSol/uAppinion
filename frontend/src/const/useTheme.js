import { ref, watchEffect } from "vue";

const theme = ref(localStorage.getItem("theme") || "light");

watchEffect(() => {
  const isDark = theme.value === "dark";
  document.documentElement.classList.toggle("dark", isDark);
  localStorage.setItem("theme", theme.value);
});

export function useTheme() {
  const toggleTheme = () => {
    theme.value = theme.value === "light" ? "dark" : "light";
  };
  return { theme, toggleTheme };
}
