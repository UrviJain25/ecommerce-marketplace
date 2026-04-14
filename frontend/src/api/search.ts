import api from "./axios";

export const searchProducts = async (
  keyword: string,
  minPrice: number,
  maxPrice: number,
  categoryId?: number
) => {
  try {
    let url = `/search?keyword=${keyword}&min_price=${minPrice}&max_price=${maxPrice}`;

    if (categoryId) {
      url += `&category_id=${categoryId}`;
    }

    const res = await api.get(url);

    return res.data;
  } catch (err: any) {
    throw err;
  }
};