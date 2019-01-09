import React, {Component} from 'react';
import {connect} from 'react-redux';
import {Icon, Label, Menu, Segment} from 'semantic-ui-react';
import {Link} from 'react-router-dom';
import SideBar from './SideBar';
import AuthButton from './AuthButton';
import SearchInput from './SearchInput';
import {fixProductsData} from '../selectors/product';

export class Header extends Component {

    constructor(props){
        super(props);
        this.onClickLogout   = this.onClickLogout.bind(this);
        //this.state = ({isLoading: true});
     }


    onClickLogout() {
        localStorage.clear();
        var port = window.location.port;
        if (port == "") {
            port = "80"
        }
        window.location.replace("//" + window.document.domain + ":" + port);
    }

    /*
    componentWillMount(){
        let self = this;
        var i = false;
        for(var key in localStorage){
            if ( key.startsWith("CognitoIdentityServiceProvider.") && key.endsWith(".userData") ) {
                self.setState({ isLoading: false });
                i = true;
                break;
            }
        }
        if (i == false) {
            location.reload();
        }
    }*/

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
                        <img width="128px" src="https://i.imgur.com/NZWCtGA.png"/>
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
                        <Menu.Item>
                            <a onClick={this.onClickLogout} href="#"><img src="https://i.imgur.com/kYgKJMH.png" width="24px"/></a>
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
