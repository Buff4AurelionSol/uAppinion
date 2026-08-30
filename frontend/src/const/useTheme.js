import { ref } from "vue";

const theme = ref("light");

export function useTheme() {
  const toggleTheme = () => {
    theme.value = theme.value === "light" ? "dark" : "light";
  };

  return { theme, toggleTheme };
}
