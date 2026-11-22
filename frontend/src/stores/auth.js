import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { api, refreshAccessToken } from "../api/axios";

export const useAuth = defineStore("auth", () => {
  const authData = ref(null);
  const isRestoring = ref(false);
  const isReady = ref(false);

  const isAuthenticated = computed(() => !!authData.value);

  let restorePromise = null;

  // El guard de rutas espera a esto antes de decidir si hay sesión o no.
  const restoreSession = () => {
    if (isReady.value) return Promise.resolve();
    if (restorePromise) return restorePromise;

    isRestoring.value = true;
    restorePromise = refreshAccessToken()
      .catch(() => {
        authData.value = null;
      })
      .finally(() => {
        isRestoring.value = false;
        isReady.value = true;
        restorePromise = null;
      });

    return restorePromise;
  };

  const buildLoginData = (loginData) => {
    if (!loginData) return null;
    return { email: loginData.email, password: loginData.password };
  };

  const sendLoginData = async (loginData) => {
    const dataLoginToSend = buildLoginData(loginData);
    try {
      const { data } = await api.post("/auth/login", dataLoginToSend);

      authData.value = data;
      console.log("Login exitoso: ", data);
    } catch (e) {
      console.error("Error al logearse: ", e);
      const errorMessage = e.response?.data?.detail || "Credenciales inválidas";
      throw new Error(errorMessage);
    }
  };

  const logout = async () => {
    try {
      await api.post("/auth/logout");
    } catch (e) {
      console.error("Error al cerrar sesión: ", e);
    } finally {
      authData.value = null;
    }
  };

  return {
    authData,
    isAuthenticated,
    isRestoring,
    isReady,
    restoreSession,
    sendLoginData,
    logout,
  };
});
