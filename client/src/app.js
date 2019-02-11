require('babel-core/register');
require('babel-polyfill');

import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import 'normalize.css/normalize.css';
import '../styles/styles.scss';
import AppRouter from './routers/AppRouter';
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

ReactDOM.render(jsx, document.getElementById('app'));
