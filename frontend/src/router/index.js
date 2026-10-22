import { createRouter, createWebHistory } from "vue-router";
import BookLibrary from "../features/books/views/BookLibrary.vue";
import BookMetrics from "../features/books/views/BookMetrics.vue";
import MoviesLibrary from "../features/movies/views/MoviesLibrary.vue";
import MoviesMetrics from "../features/movies/views/MoviesMetrics.vue";
import AnimeLibrary from "../features/anime/views/AnimeLibrary.vue";
import AnimeMetrics from "../features/anime/views/AnimeMetrics.vue";
import MoviesCatalog from "../features/movies/views/MoviesCatalog.vue";
import AnimeCatalog from "../features/anime/views/AnimeCatalog.vue";
import BookCatalog from "../features/books/views/BookCatalog.vue";
import LoginView from "../features/login/views/LoginView.vue";
import { useAuth } from "../stores/auth.js";

const routes = [
  {
    path: "/login",
    name: "Login",
    component: LoginView,
    meta: { guestOnly: true },
  },
  {
    path: "/books/catalog",
    name: "Books Catalog",
    component: BookCatalog,
  },
  {
    path: "/books/library",
    name: "Books Library",
    component: BookLibrary,
    meta: { requiresAuth: true },
  },
  {
    path: "/books/metrics",
    name: "Books Metrics",
    component: BookMetrics,
    meta: { requiresAuth: true },
  },
  {
    path: "/movies/catalog",
    name: "Movies Catalog",
    component: MoviesCatalog,
  },
  {
    path: "/movies/library",
    name: "Movies Library",
    component: MoviesLibrary,
    meta: { requiresAuth: true },
  },
  {
    path: "/movies/metrics",
    name: "Movies Metrics",
    component: MoviesMetrics,
    meta: { requiresAuth: true },
  },
  {
    path: "/animes/catalog",
    name: "Animes Catalog",
    component: AnimeCatalog,
  },
  {
    path: "/animes/library",
    name: "Animes Library",
    component: AnimeLibrary,
    meta: { requiresAuth: true },
  },
  {
    path: "/animes/metrics",
    name: "Animes Metrics",
    component: AnimeMetrics,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from) => {
  const authStore = useAuth();

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: "Login" };
  }

  if (to.meta.guestOnly && authStore.isAuthenticated) {
    return { name: "Books Catalog" };
  }
});

export default router;
