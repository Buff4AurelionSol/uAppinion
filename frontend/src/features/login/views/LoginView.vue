<script setup>
import { ref } from "vue";
import { INITIAL_LOGIN_DATA } from "../consts/const";
import { useAuth } from "../../../stores/auth";
import { useRouter } from "vue-router";

const loginData = ref({ ...INITIAL_LOGIN_DATA });
const isLoadingLogin = ref(false);
const authStore = useAuth();
const router = useRouter();

const handleLoginSubmit = async () => {
  try {
    isLoadingLogin.value = true;
    await authStore.sendLoginData(loginData.value);
    loginData.value = { ...INITIAL_LOGIN_DATA };
    router.push({ name: "Books Catalog" });
  } catch (e) {
    throw e;
  } finally {
    isLoadingLogin.value = false;
  }
};
</script>

<template>
  <div class="flex items-center justify-center flex-1 p-4">
    <section
      class="flex flex-col gap-4 p-8 w-full max-w-md items-center bg-white dark:bg-gray-900 shadow-xl border border-gray-200 rounded-md"
    >
      <header class="flex flex-col items-start w-full">
        <div class="flex flex-col gap-2">
          <h2 class="font-bold text-xl text-black dark:text-gray-100">
            Bienvenido de nuevo
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-300">
            ¡Inicia sesión para acceder a tu biblioteca o comenzar a hacer
            reseñas!
          </p>
        </div>
      </header>
      <form
        @submit.prevent="handleLoginSubmit"
        class="w-full flex flex-col gap-2"
      >
        <div class="w-full">
          <div>
            <label class="flex flex-col gap-2">
              <span class="text-gray-500 dark:text-gray-300"
                >Correo electrónico</span
              >
              <input
                type="email"
                class="border w-full h-8 border-gray-300 dark:border-gray-400 focus:outline-gray-300 focus:outline-2 dark:focus:outline-gray-400 focus:outline-offset-2 p-3 rounded-md transition-all text-black dark:text-white dark:bg-gray-800 text-sm"
                v-model="loginData.email"
              />
            </label>
          </div>
          <div>
            <label class="flex flex-col gap-2">
              <span class="text-gray-500 dark:text-gray-300">Contraseña</span>
              <input
                type="password"
                class="border w-full h-8 border-gray-300 dark:border-gray-400 focus:outline-gray-300 focus:outline-2 dark:focus:outline-gray-400 focus:outline-offset-2 p-3 rounded-md transition-all text-black dark:text-white dark:bg-gray-800 text-sm"
                v-model="loginData.password"
              />
            </label>
          </div>
        </div>
        <button type="submit" class="w-full bg-sky-400 px-2 py-2 rounded-md">
          <span class="font-medium text-gray-100">{{
            isLoadingLogin ? "Iniciando..." : "Inciar Sesión"
          }}</span>
        </button>
      </form>
      <p>¿No tienes una cuenta?</p>
      <p>Registrate aquí</p>
    </section>
  </div>
  <div></div>
</template>
