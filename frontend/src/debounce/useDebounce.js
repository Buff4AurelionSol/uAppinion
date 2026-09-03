import { onWatcherCleanup, ref, watch } from "vue";

export const useDebounce = (value, delay) => {
  const debounceData = ref(value.value);

  watch(value, (newValue) => {
    const timeOut = setTimeout(() => {
      debounceData.value = newValue;
    }, delay);

    onWatcherCleanup(() => {
      clearTimeout(timeOut);
    });
  });

  return debounceData;
};
