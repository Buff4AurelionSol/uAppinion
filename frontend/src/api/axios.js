import axios from "axios";
import { useAuth } from "../stores/auth";

export const api = axios.create({
  baseURL: "http://localhost:8000",
  withCredentials: true,
});

let refreshPromise = null;

// Unica petición de refresh en vuelo: la comparten el arranque de la app y
// el interceptor de 401, para no rotar el refresh token dos veces.
export const refreshAccessToken = () => {
  if (refreshPromise) return refreshPromise;

  // axios "crudo" para que esta petición no vuelva a pasar por el interceptor.
  refreshPromise = axios
    .post(`${api.defaults.baseURL}/auth/refresh`, {}, { withCredentials: true })
    .then(({ data }) => {
      useAuth().authData = data;
      return data;
    })
    .catch((error) => {
      useAuth().authData = null;
      throw error;
    })
    .finally(() => {
      refreshPromise = null;
    });

  return refreshPromise;
};

const isAuthRequest = (url = "") => url.startsWith("/auth/");

api.interceptors.request.use(
  (config) => {
    const authStore = useAuth();
    if (authStore.authData?.access_token) {
      config.headers["Authorization"] =
        `Bearer ${authStore.authData.access_token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response?.status === 401 &&
      originalRequest &&
      !originalRequest._retry &&
      !isAuthRequest(originalRequest.url)
    ) {
      originalRequest._retry = true;

      try {
        await refreshAccessToken();
        originalRequest.headers["Authorization"] =
          `Bearer ${useAuth().authData.access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  },
);
