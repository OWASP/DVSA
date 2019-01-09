export const cartTotalPrice = (cart) => {
    return cart.map((product) => {
        return product.price * product.amount;
    })
    .reduce((sum, value) => sum + value, 0);
}


export const cartTotalAmount = (cart) => {
    return cart
        .map((cart) => cart.amount)
        .reduce((sum, value) => sum + value, 0);
}
