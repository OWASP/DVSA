
export const addToCart = (product) => ({
    type: 'ADD_TO_CART',
    product
  });

  export const removeFromCart = ({id}) => ({
    type: 'REMOVE_FROM_CART',
    id
  });

  export const updateCart = (id, updates) => ({
    type: 'UPDATE_AMOUNT',
    id,
    updates
  });

  export const emptyCart = () => ({
    type: 'EMPTY_CART'
  });



