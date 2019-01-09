
const filtersReducerDefaultState = {
  sortBy: '',
  minPrice: 0,
  maxPrice: 100000,
  category: '',
  brand: ''
};

export default (state = filtersReducerDefaultState, action) => {
  switch (action.type) {
    case 'SORT_BY_MAX_PRICE':
      return {
        ...state,
        sortBy: 'maxPrice'
      };
    case 'SORT_BY_MIN_PRICE':
      return {
        ...state,
        sortBy: 'minPrice'
      };
    case 'SET_MIN_PRICE':
      return {
        ...state,
        minPrice: action.startPrice
      };
    case 'SET_MAX_PRICE':
      return {
        ...state,
        maxPrice: action.endPrice
      };
    case 'SET_CATEGORY':
      return {
        ...state,
        category: action.category
      };
    case 'SET_BRAND':
      return {
        ...state,
        brand: action.brand
      };
    default:
      return state;
  }
};
