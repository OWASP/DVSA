

export const fixProductsData = (arr) => {
    let fixed = [];
    for(let i = 0; i < arr.length; i++){
        let temp = {
          title: arr[i].title,
          productid: arr[i].id,
          type: arr[i].type,
          image: arr[i].images[0].url,
          price: String(arr[i].price)
        }
        fixed.push(temp);
    }
    return fixed;
}

export const getBrands = (arr) => {
    let brands = [];
    for(let i = 0; i < arr.length; i++){
        if(!brands.includes(arr[i].brand)){
            brands.push(arr[i].brand);
        }
    }
    return brands;
}

export const getCategories = (arr) => {
    let categories = [];
    for(let i = 0; i < arr.length; i++){
        if(!categories.includes(arr[i].category)){
            categories.push(arr[i].category);
        }
    }
    return categories;
}