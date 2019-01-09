function generate_UUID(){
    var dt = new Date().getTime();
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (dt + Math.random()*16)%16 | 0;
        dt = Math.floor(dt/16);
        return (c=='x' ? r :(r&0x3|0x8)).toString(16);
    });
    return uuid;
}

const shoppingCartReducer = (state = [], action) => {
    switch (action.type) {
        case 'ADD_TO_CART':
            if (localStorage.getItem("order-id") === null && localStorage.getItem("cart-id") === null ) {
                var cartid = generate_UUID();
                localStorage.setItem('cart-id', cartid);
            }
            var cart = state.concat(action.product);
            var json = JSON.stringify(cart);
            localStorage.setItem('cart', json);
            return cart;
        case 'REMOVE_FROM_CART':
            var cart = state.filter(({id}) => id !== action.id);
            var json = JSON.stringify(cart);
            if (json.length < 20 && localStorage.getItem("order-id") != null) {
                var orderid = localStorage.getItem("order-id");
                localStorage.removeItem("order-id");
                var cartid = localStorage.getItem("order-id");
                localStorage.removeItem("cart-id");
            }
            localStorage.setItem('cart', json);
            return cart;
        case 'UPDATE_AMOUNT':
            let updatedCart = state.map((cart) => {
                if(cart.id === action.id){
                    return {
                        ...cart,
                        ...action.updates
                    }
                }else{
                    return cart;
                }
            });
            localStorage.setItem('cart', JSON.stringify(updatedCart));
            return updatedCart;
        case 'EMPTY_CART':
            return [];
        default: 
            return state;
    }
      
}

export default shoppingCartReducer;
