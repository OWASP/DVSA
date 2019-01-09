import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Container, Header, Button, Table, Segment } from 'semantic-ui-react';
import * as API from '../utils/apiCaller';
import { Redirect, HashRouter } from 'react-router-dom';

export class OrderView extends React.Component {
    constructor(props){
        super(props);
        const id = window.location.pathname.split('/')[2];
        this.state = {
            order: { "orderId": id },
            status: "",
            isLoading: true,
            isDisabled: true,
            toOrders: false
        };

    }

    handleCancel = () => {
        let opts = {
                    'action': 'cancel',
                    'order-id': this.state.order.orderId
        };
        let self = this;
        API.callApi(opts)
            .then(function(response) {
                return response.json();
            }).then(function(err, data) {
                if(data && data.status == 'ok') {
                    self.setState ({ isLoading: false });
                    self.setState ({ toOrders: true});
                } else {
                    self.setState ({ isLoading: false });
                    self.setState ({ toOrders: true});
                }
           });
    }

    componentWillMount(){
        let self = this;
        let opts = {
                    'action': 'get',
                    'order-id': self.state.order.orderId
        };
        API.callApi(opts)
            .then(function(response) {
                return response.json();
            }).then(function(err, data) {
                if(data && data.status == 'ok') {
                    self.setState ({ isLoading: false });
                    self.setState ({ order: data.order });
                    let self = this;
                    if (self.state.order.orderStatus < 120) {
                        self.setState ({ isDisabled: false });
                    }
                    self.setState ({ isLoading: false });
                    self.setState ({ order: data.order });
                } else {
                    if (err.order.orderStatus < 120) {
                        self.setState ({ isDisabled: false });
                    }
                    self.setState ({ isLoading: false });
                    self.setState ({ order: err.order });
                }
           });
    }

    render(){
        if (this.state.toOrders === true) {
            return <Redirect to='/orders' />
        }
        return(
            <Container className='page-top-margin'>
            {this.state.isLoading && <img src="/images/loader.gif" /> }
                <div>
                     <h2>Order {this.state.order.orderId} </h2>
                     <h4>status: {this.state.order.orderStatus}</h4>
                     <h4>Confirmation Token: {this.state.order.confirmationToken}</h4>
                     <h4>Date: {new Date(this.state.order.paymentTS*1000).toLocaleString()}</h4>
                     <h4>Address: {JSON.stringify(this.state.order.address)}</h4>
                     <h4>Total: {this.state.order.totalAmount}</h4>

                     <br/><br/>
                    <Button type='submit' color='red' onClick={this.handleCancel} disabled={this.state.isDisabled}>Cancel Order</Button>
                 </div>
            </Container>
        );
    }
}


const mapStateToProps = (state) => ({
    cart: state.shoppingCart,
});

export default connect(mapStateToProps)(OrderView);