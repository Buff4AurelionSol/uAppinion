import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { api } from "../api/axios";

export const useAuth = defineStore("auth", () => {
  const authData = ref(null);
  const isAuthenticated = computed(() => !!authData.value);

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

  return { authData, isAuthenticated, sendLoginData };
});
