<script setup>
import { ref, watchEffect } from "vue";

const isOpen = defineModel({ type: Boolean, default: false });
const modalRef = ref(null);

watchEffect(() => {
  if (!modalRef.value) return;
  if (isOpen.value) {
    modalRef.value.showModal();
  } else {
    modalRef.value.close();
  }
});

const closeModal = () => {
  isOpen.value = false;
};

const closeBackdropclick = (e) => {
  if (e.target === modalRef.value) {
    closeModal();
  }
};
</script>

<template>
  <dialog
    ref="modalRef"
    class="w-full max-w-lg m-auto p-0 rounded-md dark:bg-gray-800"
    @close="closeModal"
    @click="closeBackdropclick"
  >
    <div class="p-12 relative" @click="(e) => e.stopPropagation()">
      <button
        type="button"
        class="bg-gray-400 px-2 py-1.5 rounded-md text-white absolute top-4 right-4 hover:bg-gray-500 transition-colors font-bold"
        @click="closeModal"
      >
        X
      </button>
      <slot> </slot>
    </div>
  </dialog>
</template>
