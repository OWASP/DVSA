import React from 'react';
import createHistory from 'history/createBrowserHistory';
import { BrowserRouter, Route, Switch, Router } from 'react-router-dom';
import { connect } from 'react-redux';
import { addToCart } from '../actions/shoppingCart';

import NotFoundPage from '../components/NotFoundPage';
import Header from '../components/Header';
import HomePage from '../components/HomePage';
import StorePage from '../components/StorePage';
import ProductView from '../components/ProductView';
import CartPage from '../components/CartPage';
import ShippingPage from '../components/ShippingPage';
import BillingPage from '../components/BillingPage';
import ConfirmationPage from '../components/ConfirmationPage';
import OrdersPage from '../components/OrdersPage'
import { withAuthenticator } from 'aws-amplify-react';
import OrderView from '../components/OrderView';
import InfoPage from '../components/InfoPage';
import AdminPage from '../components/AdminPage';
import ContactPage from '../components/ContactPage';
import ProfilePage from '../components/ProfilePage';
import InboxPage from '../components/InboxPage';
import MessageView from '../components/MessageView';

export const history = createHistory();

export class AppRouter extends React.Component {

    componentDidMount(){
        try {
            const json = localStorage.getItem('cart');
            const cart = JSON.parse(json);
            if(cart){
                this.props.startAddToCart(cart);
            }
        } catch (err) {
            console.log(err);
        }
    }

    render(){
        return(
            <Router history={history}>
                <BrowserRouter>
                <div>
                <Header/>
                    <Switch>
                        <Route path='/' component={StorePage} exact={true}/>
                        <Route path='/info' component={InfoPage} exact={true}/>
                        <Route path='/admin' component={AdminPage} exact={true}/>
                        <Route path='/contact' component={ContactPage} exact={true}/>
                        <Route path='/store' component={StorePage} exact={true}/>
                        <Route path='/store/:id' component={ProductView} />
                        <Route path='/cart' component={CartPage} exact={true}/>
                        <Route path='/shipping' component={ShippingPage} exact={true}/>
                        <Route path='/billing' component={BillingPage} exact={true}/>
                        <Route path='/confirmation' component={ConfirmationPage} exact={true}/>
                        <Route path='/orders' component={OrdersPage} exact={true}/>
                        <Route path='/profile' component={ProfilePage} exact={true}/>
                        <Route path='/orders/:id' component={OrderView} />
                        <Route path='/inbox' component={InboxPage} exact={true}/>
                        <Route path='/inbox/:id' component={MessageView} />
                        <Route component={NotFoundPage} />
                    </Switch>
                </div>
                </BrowserRouter>
            </Router>
        );
    }
}


const mapDispatchToProps = (dispatch) => ({
    startAddToCart: (cart) => dispatch(addToCart(cart))
});

export default connect(undefined, mapDispatchToProps)(withAuthenticator(AppRouter));
