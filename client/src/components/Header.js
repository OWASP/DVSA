import React, {Component} from 'react';
import {connect} from 'react-redux';
import {Icon, Label, Menu, Segment} from 'semantic-ui-react';
import {Link} from 'react-router-dom';
import SideBar from './SideBar';
import AuthButton from './AuthButton';
import * as API from '../utils/apiCaller';
import SearchInput from './SearchInput';
import {fixProductsData} from '../selectors/product';

export class Header extends Component {

    constructor(props){
        super(props);
        this.onClickLogout   = this.onClickLogout.bind(this);
        this.state = {
            inbox: false,
            inboxLength: 0,
        };
        this.ajaxCall = this.ajaxCall.bind(this);
     }


    onClickLogout() {
        localStorage.clear();
        var port = window.location.port;
        if (port == "") {
            port = "80"
        }
        window.location.replace("//" + window.document.domain + ":" + port);
    }

    ajaxCall(){
        let self = this;
        let opts = {
            'action': 'inbox'
        };
        API.callApi(opts)
        .then(function(response) {
                return response.json();
            }).then(function(err, data) {
                if(data) {
                    if ( data.status == "ok" && data.messages.length > 0) {
                        self.setState ({ inbox: true });
                        self.setState ({ inboxLength: data.messages.length });
                    }
                    else {
                        self.setState ({ inbox: false });
                    }
                }
                else {
                    if (err.status == "ok" && err.messages.length > 0) {
                        self.setState ({ inbox: true });
                        self.setState ({ inboxLength: err.messages.length });
                    }
                    else {
                        self.setState ({ inbox: false });
                    }
                }
           });
    }

    componentWillMount() {
        setInterval(this.ajaxCall, 30000);

    }

    render() {
        return (
            <Segment inverted>
                <Menu inverted fixed='top' size='large'>
                    <Menu.Item>
                        <SideBar/>
                    </Menu.Item>
                    <div className='search-input'>
                        <SearchInput products={fixProductsData(this.props.products)}/>
                    </div>
                    <Menu.Item>
                        <img src="https://i.imgur.com/p3R1bCC.png"/>
                        <h3>DVSA - Damn Vulnerable Serverless Application</h3>
                    </Menu.Item>


                    <Menu.Menu position='right'>

                        <Menu.Item>
                            <Link to='/cart'>
                                <Icon className='cursor' size='large' name='shop'/>
                            </Link>
                            {this.props.cartLength > 0 &&
                            <Label size='mini' color='red'>{this.props.cartLength}</Label>}
                        </Menu.Item>

                         <Menu.Item name='inbox'>
                            <Link to='/inbox'>
                            <a><img src='/images/iconinbox.png' width="28px"/></a>
                            </Link>
                            {  this.state.inboxLength > 0 && this.state.inbox &&
                            <Label size='mini' color='red'>{ this.state.inboxLength }</Label>}
                         </Menu.Item>

                         <Menu.Item name='contact'>
                            <Link to='/contact'>
                            <a><img src='https://i.imgur.com/S8Rfv9l.png' width="24px"/></a>
                            </Link>
                         </Menu.Item>

                        <Menu.Item>
                            <a onClick={this.onClickLogout} href="#"><img src='https://i.imgur.com/kYgKJMH.png' width="24px"/></a>
                        </Menu.Item>
                    </Menu.Menu>
                </Menu>
            </Segment>
        );
    }
}

const mapStateToProps = (state) => ({
    cartLength: state.shoppingCart.length,
    products: state.products
});

export default connect(mapStateToProps)(Header);
