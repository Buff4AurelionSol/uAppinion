import { createRouter, createWebHistory } from "vue-router";
import BookLibrary from "../features/books/views/BookLibrary.vue";
import BookMetrics from "../features/books/views/BookMetrics.vue";
import MoviesLibrary from "../features/movies/views/MoviesLibrary.vue";
import MoviesMetrics from "../features/movies/views/MoviesMetrics.vue";
import AnimeLibrary from "../features/anime/views/AnimeLibrary.vue";
import AnimeMetrics from "../features/anime/views/AnimeMetrics.vue";

const routes = [
  {
    path: "/books/library",
    name: "Book Library",
    component: BookLibrary,
  },
  {
    path: "/books/metrics",
    name: "Book Metrics",
    component: BookMetrics,
  },
  {
    path: "/movies/library",
    name: "Movies Library",
    component: MoviesLibrary,
  },
  {
    path: "/movies/metrics",
    name: "Movies Metrics",
    component: MoviesMetrics,
  },
  {
    path: "/animes/library",
    name: "Animes Library",
    component: AnimeLibrary,
  },
  {
    path: "/animes/metrics",
    name: "Animes Metrics",
    component: AnimeMetrics,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
