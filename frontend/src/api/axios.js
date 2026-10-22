import axios from "axios";
import { useAuth } from "../stores/auth";

export const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  withCredentials: true,
});

let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

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

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers["Authorization"] = `Bearer ${token}`;
            return api(originalRequest);
          })
          .catch((error) => {
            return Promise.reject(error);
          });
      }

      isRefreshing = true;
      const authStore = useAuth();

      try {
        const { data } = await axios.post(
          "http://127.0.0.1:8000/auth/refresh",
          {},
          { withCredentials: true },
        );

        const newAccessToken = data.access_token;
        authStore.authData = data;

        processQueue(null, newAccessToken);

        originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;

        return api(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError, null);

        authStore.authData = null;

        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }
    return Promise.reject(error);
  },
);
