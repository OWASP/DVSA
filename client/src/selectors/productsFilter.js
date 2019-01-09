
export default (products, {sortBy, minPrice, maxPrice, category, brand}) => {

    return products.filter((product) => {
        const maxPriceMatch = maxPrice ? product.price <= maxPrice : true;
        const minPriceMatch = minPrice ? product.price >= minPrice : true;
        const categoryMatch = category ? product.category === category : true;
        const brandMatch = brand ? product.brand === brand : true;

        return minPriceMatch && maxPriceMatch && categoryMatch && brandMatch;
    }).sort((a, b) => {
        if(sortBy === 'minPrice'){
            return a.price > b.price ? 1 : -1;
        }
        if(sortBy === 'maxPrice'){
            return a.price < b.price ? 1 : -1;
        }
    });
}