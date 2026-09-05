// src/features/books/services/apiBooks.js

const BASE_URL = "https://openlibrary.org";

export const apiBooks = {
  getTrendingBooks: async () => {
    try {
      const response = await fetch(`${BASE_URL}/trending/now.json?limit=12`, {
        headers: {
          Accept: "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Error HTTP: ", response.status);
      }

      const data = await response.json();

      return data?.works || [];

      return data;
    } catch (e) {
      console.error("Error al traer los libros en tendencia: ", e);
      throw e;
    }
  },

  getImageUrl: (coverId, size = "M") => {
    return `https://covers.openlibrary.org/b/id/${coverId}-${size}.jpg`;
  },

  searchBooks: async (query) => {
    if (!query || !query.trim()) return [];

    try {
      const search_params = new URLSearchParams({
        q: query.trim(),
        limit: 12,
      });

      const response = await fetch(`${BASE_URL}/search.json?${search_params}`);

      if (!response.ok) {
        throw new Error("Error HTTP: ", response.status);
      }

      const data = await response.json();

      return data?.docs || [];
    } catch (e) {
      console.error("Error al buscar el libro ", e);
      throw e;
    }
  },
};
