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

const routes = [
  {
    path: "/books/catalog",
    name: "Books Catalog",
    component: BookCatalog,
  },
  {
    path: "/books/library",
    name: "Books Library",
    component: BookLibrary,
  },
  {
    path: "/books/metrics",
    name: "Books Metrics",
    component: BookMetrics,
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
  },
  {
    path: "/movies/metrics",
    name: "Movies Metrics",
    component: MoviesMetrics,
  },
  {
    path: "/animes/library",
    name: "Animes Catalog",
    component: AnimeCatalog,
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
