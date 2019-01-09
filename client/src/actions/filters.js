
export const sortByMaxPrice = () => ({
    type: 'SORT_BY_MAX_PRICE',
    sortBy: 'maxPrice'
});

export const sortByMinPrice = () => ({
    type: 'SORT_BY_MIN_PRICE',
    sortBy: 'minPrice'
});

export const setMinPrice = (startPrice = undefined) => ({
    type: 'SET_MIN_PRICE',
    startPrice
});

export const setMaxPrice = (endPrice = undefined) => ({
    type: 'SET_MAX_PRICE',
    endPrice
});

export const setCategory = (category = undefined) => ({
    type: 'SET_CATEGORY',
    category
});

export const setBrand = (brand = undefined) => ({
    type: 'SET_BRAND',
    brand
});

