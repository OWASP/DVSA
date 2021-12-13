import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Button, Segment, Label, Icon, Image, Dropdown, Form, Transition } from 'semantic-ui-react';
import { removeFromCart, updateCart } from '../actions/shoppingCart';


export class ConfirmationPageItem extends React.Component {
    state = {visible: true}

    toggleVisibility = () => this.setState({ visible: !this.state.visible});

    handleRemove = () =>{
        this.toggleVisibility();
        setTimeout(() => {
            this.props.startRemoveFromCart({id: this.props.id})
        }, 500);
    }
    
    handleSelect = (e) => {
        this.props.startUpdateAmount(this.props.id, {amount: Number(e.target.value)});
    }
    render(){
        return (
            <Transition duration={500} visible={this.state.visible}>
                <Segment className='cart-page_main'>
                    <div className='cart-page_desc'>
                        <div>
                            <Link to={`/store/${this.props.id}`}>
                            <Image size='small' src={this.props.images[0].url} />
                            </Link>
                        </div>
                        <div>
                            <ul>
                                <li><h4>{this.props.title}</h4></li>
                                <li>{this.props.brand}</li>
                            </ul>
                        </div>
                    </div>
                </Segment>
            </Transition>
        );
    }
}

const mapDispatchToProps = (dispatch) => ({
    startRemoveFromCart: (id) => dispatch(removeFromCart(id)),
    startUpdateAmount: (id, update) => dispatch(updateCart(id, update))
});

export default connect(undefined, mapDispatchToProps)(ConfirmationPageItem);