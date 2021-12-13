import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Container, Header, Segment } from 'semantic-ui-react';
import * as API from '../utils/apiCaller';
import {Redirect} from 'react-router-dom';
import CartPageItem  from './ConfirmationPageItem';

export class ConfirmationPage extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            orderid: this.props.location.state.confirmationInfo.orderId
        }
    }

    componentWillMount(){
      let self = this;
      let opts = {
          'action': 'complete',
          'order-id': this.state.orderid
      };
      API.callApi(opts)
          .then(function(response) {
              return response.json();
          }).then(function(err, data) {
         });
    }

    render(){
        const token = this.props.location.state.confirmationInfo.token;
        const amount = this.props.location.state.confirmationInfo.amount;
        let cart = this.props.location.state.confirmationInfo.cart;
        const orderid = this.props.location.state.confirmationInfo.orderId;
        if(cart) cart = JSON.parse(cart);
        return(
            <Container className='page-top-margin'>
            <div>
            <Header as='h2'>Confirmation for order: {orderid}</Header>
                {
                    cart.length > 0 ? (
                    <div>
                        <div>
                            {
                                cart.map((cart) => {
                                    return <CartPageItem key={cart.id} {...cart} />;
                                })
                            }
                        </div>
                    </div>) : <div>Your cart is empty</div>
                }
                <div>
                 <Segment>Total Price: $ {amount}</Segment>
                 <Segment>Confirmation Token: {token}</Segment>
                 </div>
                </div>
            </Container>
        );
    }
}

const mapStateToProps = (state) => ({
    cart: state.shoppingCart
});

export default connect(mapStateToProps)(ConfirmationPage);