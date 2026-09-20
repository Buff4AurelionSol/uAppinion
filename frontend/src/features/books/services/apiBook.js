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

  searchBooks: async (query, page = 1, limit = 12) => {
    if (!query || !query.trim()) return { data: [], totalPages: 0 };

    try {
      const search_params = new URLSearchParams({
        q: query.trim(),
        page,
        limit,
      });

      const response = await fetch(`${BASE_URL}/search.json?${search_params}`);

      if (!response.ok) {
        throw new Error("Error HTTP: ", response.status);
      }

      const data = await response.json();
      const totalBooks = data.numFound || 0;
      const totalPages = Math.ceil(totalBooks / limit);

      return {
        data: data?.docs || [],
        totalPages,
      };
    } catch (e) {
      console.error("Error al buscar el libro ", e);
      throw e;
    }
  },

  getGenresByBook: async (bookKey) => {
    try {
      const response = await fetch(`${BASE_URL}${bookKey}.json`);
      const data = await response.json();
      if (!data.subjects) return [];

      const genres = data.subjects.flatMap((subjectString) =>
        subjectString.split(",").map((genre) => genre.trim()),
      );

      console.log(genres);

      return genres;
    } catch (e) {
      console.error(
        "Hubo un error al conseguir los géneros del libro desde la API EXTERNA ",
        e,
      );
      return [];
    }
  },

  getAllMyGenres: async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/genres");
      const data = await response.json();
      return data || [];
    } catch (e) {
      console.error("Hubo un error al traer los géneros de los libros");
    }
  },

  getMyCatalogLibraryBooks: async ({
    page = 1,
    limit = 12,
    search = "",
    genre_id = "",
    order_by = "",
  }) => {
    try {
      const params = new URLSearchParams({
        page,
        limit,
      });

      if (search) params.append("search", search);
      if (genre_id) params.append("genre_id", genre_id);
      if (order_by) params.append("order_by", order_by);

      const response = await fetch(
        `http://127.0.0.1:8000/books/library?${params.toString()}`,
      );

      if (!response.ok) {
        throw new Error("Error HTTP: ", response.status);
      }

      return await response.json();
    } catch (e) {
      console.error(
        "Hubo un error al traer el catalogo de mi libreria de libros.",
      );
      throw e;
    }
  },
};
