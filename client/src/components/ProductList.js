import React from 'react';
import ProductItem from './ProductItem';
import { Container } from 'semantic-ui-react';

const ProductList = (props) => (
  <Container>
    <div className='products-list'>
      {
          props.products.map((product) => {
            return <ProductItem key={product.id} {...product} />;
          })
      }
    </div>
    </Container>
);



export default ProductList;