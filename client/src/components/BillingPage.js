import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Button, Container, Header, Form } from 'semantic-ui-react';
import * as API from '../utils/apiCaller';
import {Redirect} from 'react-router-dom';
import CreditCardInput from 'react-credit-card-input';
import { emptyCart } from '../actions/shoppingCart';

export class BillingPage extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            isLoading: false,
            toConfirmation: false,
            submitted: false,
            billingInfo: {
                cardNumber: '',
                expiry: '',
                cvv: ''
            },
            confirmationInfo: {
                cart: [],
                amount: '',
                token: ''
            }
        }
        this.handleCardNumberChange = this.handleCardNumberChange.bind(this);
        this.handleCardExpiryChange = this.handleCardExpiryChange.bind(this);
        this.handleCardCVCChange = this.handleCardCVCChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    handleCardNumberChange = event => {
        let billingInfo = {...this.state.billingInfo};
        billingInfo['cardNumber'] = event.target.value;
        this.setState({ billingInfo: billingInfo })
    }
    handleCardExpiryChange = event => {
        let billingInfo = {...this.state.billingInfo};
        billingInfo['expiry'] = event.target.value;
        this.setState({ billingInfo: billingInfo })
    }
    handleCardCVCChange = event => {
        let billingInfo = {...this.state.billingInfo};
        billingInfo['cvv'] = event.target.value;
        this.setState({ billingInfo: billingInfo })
    }
    handleSubmit = () => {
        let self = this;
        self.setState({submitted: true});
        self.setState({isLoading: true});
        const orderId = localStorage.getItem('order-id');
        let opts = {
            'action': 'billing',
            'order-id': orderId,
            'data': {
                'ccn': this.state.billingInfo.cardNumber.replace(/ /g,''),
                'exp': this.state.billingInfo.expiry.replace(/ /g,''),
                'cvv': this.state.billingInfo.cvv 
            }
        };
        API.callApi(opts)
        .then(function(response) {
            return response.json();
        }).then(function(data) {
            //console.log("Response", data);
            if(data && data.status == 'ok') {
                self.setState({submitted: false});
                //if response is ok move to shipping page
                let confirmationInfo = {
                    cart: localStorage.getItem('cart'),
                    amount: data.amount,
                    token: data.token
                }
                self.setState({confirmationInfo: confirmationInfo})
                localStorage.removeItem('order-id');
                localStorage.removeItem('cart-id');
                localStorage.removeItem('cart');
                try {
                    self.props.startEmptyCart();
                } catch (err) {
                    console.log(err);
                }
                self.setState({toConfirmation: true});
            } else {
                self.setState ({ isLoading: false });
                //handle response error
            }
        });
    }
    render(){
        if (this.state.toConfirmation === true) {
            return <Redirect to={{
                pathname: "/confirmation",
                state: { confirmationInfo:  this.state.confirmationInfo }
              }} />
        } 
        return(
            <Container className='page-top-margin'>
            {this.state.isLoading && <img src="/images/loader.gif" /> }
            <Header as='h2'>Enter Card Details</Header><br/><br/>
            <div>
                <Container>
                <CreditCardInput containerClassName="custom-container"
                containerStyle={{
                      padding: '2px',
                      fontSize: '24px'
                    }}
                cardNumberInputProps={{onChange: this.handleCardNumberChange }}
                cardExpiryInputProps={{onChange: this.handleCardExpiryChange }}
                cardCVCInputProps={{onChange: this.handleCardCVCChange }}
                fieldClassName="input"
                />
                </Container>
            </div>
            <Form>
            <Form.Field></Form.Field>
            <Button type='submit' onClick={this.handleSubmit} disabled={this.state.submitted}>Submit</Button>
            </Form>
             <br/><br/> <br/><br/>
            <img src="https://i.imgur.com/kDzF4Cr.png"/>
            </Container>
        );
    }
}

const mapStateToProps = (state) => ({
    cart: state.shoppingCart
});

const mapDispatchToProps = (dispatch) => ({
    startEmptyCart: () => dispatch(emptyCart())
});

export default connect(mapStateToProps, mapDispatchToProps)(BillingPage);