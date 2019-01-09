import React from 'react';
import { Container, Label, Select, Button, Icon, Image, Rating, Form } from 'semantic-ui-react';
import { connect } from 'react-redux';
import { addToCart } from '../actions/shoppingCart'; 
import Lightbox from 'lightbox-react';

export class ProductView extends React.Component {
    state = {
        added: this.props.cart.some((cart) => cart.id == this.props.product.id),
        photoIndex: 0,
        isOpen: false
    };

    handleAddToCart = () => {
        const cart = this.props.product;
        cart.size = this.state.size;
        this.props.startAddToCart(cart);
    };


    render(){
        const images = this.props.product.images.map((images) => images.url);
        const {
            photoIndex,
            isOpen,
            active
        } = this.state;
        let added = this.props.cart.some((cart) => cart.id == this.props.product.id);
        return (
            <div className='page-top-margin'>
                <Container>
                    <div  className='product-view'>
                        <div>
                            <div>
                                <Image 
                                src={this.props.product.images[photoIndex].url} 
                                onClick={() => this.setState({ isOpen: true })} 
                                label={{ as: 'a', corner: 'left', size: 'big',color: 'teal', icon: 'search plus' }}
                                className='product-view_main-image cursor'
                                />
                            </div>
                            <div className='product-view_images'>
                                {
                                    this.props.product.images.map((image, i) => {
                                        return (
                                        <div key={i}>
                                            <Image 
                                            onClick={() => this.setState({photoIndex: i})} 
                                            src={image.url} 
                                            size='tiny'
                                            className='cursor'
                                            disabled={this.state.photoIndex !== i}
                                            />
                                        </div>
                                        )
                                    })
                                } 
                            </div>
                        </div>
                        <div className='product-page__info'>
                            <div>
                                <h1>{this.props.product.title}</h1>
                                <Rating maxRating={5} defaultRating={3} icon='star' size='small' />
                            </div>
                            <div>
                                <span className='cart-page_green'>In Stock</span>
                            </div>
                            <div>
                                <p className='product-page__desc'>{this.props.product.description}</p>
                            </div>
                            <div>
                                <Label as='a' color='teal' tag>
                                    <h3>{`$${this.props.product.price}`}</h3>
                                </Label>
                            </div>
                            <div>
                                <div>
                                    <Button 
                                    onClick={this.handleAddToCart}
                                    disabled={added}
                                    content='Add to Cart'
                                    size='large'
                                    color='green'
                                    className='product-page__button'
                                    />
                                </div>
                                
                            </div>
                        </div>
                    </div>
                </Container>
                {isOpen &&
                    <Lightbox
                        mainSrc={images[photoIndex]}
                        nextSrc={images[(photoIndex + 1) % images.length]}
                        prevSrc={images[(photoIndex + images.length - 1) % images.length]}
 
                        onCloseRequest={() => this.setState({ isOpen: false })}
                        onMovePrevRequest={() => this.setState({
                            photoIndex: (photoIndex + images.length - 1) % images.length,
                        })}
                        onMoveNextRequest={() => this.setState({
                            photoIndex: (photoIndex + 1) % images.length,
                        })}
                    />
                }
            </div>
        )
    }
}

const mapStateToProps = (state, props) => ({
    product: state.products.find((product) => product.id ===  props.match.params.id),
    cart: state.shoppingCart
});

const mapDispatchToProps = (dispatch) => ({
    startAddToCart: (product) => dispatch(addToCart(product))
});

export default connect(mapStateToProps, mapDispatchToProps)(ProductView);