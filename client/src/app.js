import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import 'normalize.css/normalize.css';
import '../styles/styles.scss';
import AppRouter, {history} from './routers/AppRouter';
import configureStore from './store/configureStore';
import 'react-dates/lib/css/_datepicker.css';
import AwsAuth from './aws-exports'

AwsAuth.configure();

const store = configureStore();

const jsx = (
    <Provider store={store}>
        <AppRouter />
    </Provider>
 );

 // let hasRendered = false;
 // const renderApp = () => {
 //     if(!hasRendered){
 //        ReactDOM.render(jsx, document.getElementById('app'));
 //        hasRendered = true;
 //     }
 // }

ReactDOM.render(jsx, document.getElementById('app'));

// firebase.auth().onAuthStateChanged((user) => {
//     if(user) {
//         console.log(user);
//         store.dispatch(login(user));
//         renderApp();
//         if(history.location.pathname !== '/'){
//         history.push('/');
//         }
//     }else{
//         store.dispatch(logout());
//         renderApp();
//     }
// });
//


