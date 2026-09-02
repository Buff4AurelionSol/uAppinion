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

      const data = await response.json();

      return data?.works || [];

      return data;
    } catch (e) {
      console.log("Error al traer los libros en tendencia: ", e);
    }
  },

  getImageUrl: (coverId, size = "M") => {
    return `https://covers.openlibrary.org/b/id/${coverId}-${size}.jpg`;
  },
};
