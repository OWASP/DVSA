import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Button, Segment, Container, Label, Dimmer, Loader, Grid, Image, Header, Icon, IconGroup } from 'semantic-ui-react';
import CartPageItem  from './CartPageItem';
import {cartTotalPrice, cartTotalAmount} from '../selectors/cart-total';
import * as API from '../utils/apiCaller';
import {Redirect} from 'react-router-dom';

export class CartPage extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            toShipping: false,
            isLoading: false,
        }
        this.onClickCheckout = this.onClickCheckout.bind(this);
    }

    onClickCheckout() {
        let self = this;
        self.setState({isLoading: true});
        const orderId = localStorage.getItem('order-id');
        const cartId  = localStorage.getItem('cart-id');
        let cart    = localStorage.getItem('cart') ? localStorage.getItem('cart') : null;
        cart = cart ? JSON.parse(cart) : cart;
        let cartItems = {};
        if(cart && cart.length) {
            cart.forEach(element => {
                cartItems[element.id] = element.amount;
            });
        } 
        let opts = {};
        if(orderId) {
            opts = {
                "action": "update", 
                "order-id": orderId, 
                "items": cartItems
            }
        } else {
            opts = {
                "action": "new", 
                "cart-id": cartId, 
                "items": cartItems
            }
        }
        if(cartId && cart) {
            //if order id not present send action new else send action update
            API.callApi(opts)
            .then(function(response) {
                return response.json();
            }).then(function(err, data) {

                if(data && data.status == 'ok') {
                    self.setState({toShipping: false});
                    if(opts.action == 'new') {
                        localStorage.setItem('order-id', data['order-id']);
                    }

                    self.setState({toShipping: true});
                } else {
                    self.setState ({ isLoading: false });
                    var orderid = "";
                    if (err.status == "err" && err.msg == "could not find order") {
                        localStorage.removeItem('order-id');
                        opts = {
                            "action": "new",
                            "cart-id": cartId,
                            "items": cartItems
                        }
                        API.callApi(opts)
                        .then(function(response) {
                            return response.json();
                        }).then(function(err, data) {
                            if (err.msg == "order created" || data.msg == "order created") {
                                if (err.status == "ok"){
                                    orderid = err["order-id"];
                                }
                                else if (data.status == "ok"){
                                    orderid == data["order-id"];
                                }
                                localStorage.setItem("order-id", orderid)
                                self.setState({toShipping: true});
                            }
                        });
                    }
                    else if (err.status == "ok" && err.msg == "order created") {
                        orderid = err["order-id"];
                        localStorage.setItem("order-id", orderid)
                        self.setState({toShipping: true});
                    }
                    else {
                        self.setState({toShipping: false});
                    }
                }
            });
        } else {
            //handle no items in cart error
        } 
    }

    render(){
        const cart = this.props.cart;
        const totalPrice = this.props.cartTotalPrice;
        const totalAmount = this.props.cartTotalAmount;
        if (this.state.toShipping === true) {
            return <Redirect to='/shipping' />
        }      
        return (
            <Container className='page-top-margin'>
            {this.state.isLoading && <img src="/images/loader.gif" /> }
                {
                    cart.length > 0 ? (
                    <div className='cart-page'>
                        <div className='cart-page_items'>
                            {
                                cart.map((cart) => {
                                    return <CartPageItem key={cart.id} {...cart} />;
                                })
                            }
                        </div>
                            <Segment secondary className='cart-page_check'>
                                <h4>Order Summary</h4>
                                <div className='cart-page_check__item'>
                                    <div>Subtotal ({`${totalAmount} `}{totalAmount > 1 ? 'items' : 'item'})</div>
                                    <div><h4>${totalPrice}</h4></div>
                                </div>
                                <div className='cart-page_check__item'>
                                    <div>Shipping</div>
                                    <div><h4 className='cart-page_green'>Free</h4></div>
                                </div>
                                <div className='cart-page_check__item'>
                                    <div><h4>Total Price</h4></div>
                                    <div><h4>${totalPrice}</h4></div>
                                </div>
                                <div className='cart-page_check__item'>
                                    <Button fluid color='teal' onClick={this.onClickCheckout}>CHECK OUT</Button>
                                </div>
                                <div className='cart-page_check__item cart-page_check_item_paypal'>
                                <Image centered src="/images/paypal.png" />
                                </div>
                            </Segment>
                        </div>
                        ) : (
                            <Link to='/store' >
                                <Segment textAlign='center'>
                                    
                                        <h3>Your cart is currently empty.</h3>
                                        <Icon size='massive' name='shopping bag' />
                                            <h4>Click to start shop</h4>
                                    
                                </Segment>  
                            </Link>
                        )
                }
            </Container>
        );
    }
}

const mapStateToProps = (state) => ({
    cart: state.shoppingCart,
    cartTotalPrice: cartTotalPrice(state.shoppingCart),
    cartTotalAmount: cartTotalAmount(state.shoppingCart)
});

export default connect(mapStateToProps)(CartPage);