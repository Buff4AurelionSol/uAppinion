import { createRouter, createWebHistory } from "vue-router";
import BookLibrary from "../views/books/BookLibrary.vue";
import BookMetrics from "../views/books/BookMetrics.vue";
import MoviesLibrary from "../views/movies/MoviesLibrary.vue";
import MoviesMetrics from "../views/movies/MoviesMetrics.vue";
import AnimeLibrary from "../views/anime/AnimeLibrary.vue";
import AnimeMetrics from "../views/anime/AnimeMetrics.vue";

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
