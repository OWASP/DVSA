import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Button, Segment, Icon, Modal, Divider, Image, Loader } from 'semantic-ui-react';


export class AuthButton extends React.Component {

    facebookLogin = () => { this.props.startFacebookLogin(); };

    googleLogin = () => { this.props.startGoogleLogin(); };

    logout = () => { this.props.startLogout(); };

    render(){
        return (
            this.props.isAuthenticated ? (
                <Modal closeIcon trigger={<Icon className='cursor' name='user' size='large'/>} size='mini' centered={false}>
                    <Modal.Header>Profile</Modal.Header>
                    <Modal.Content>
                        <div className='centered-text'>
                            {
                                this.props.profile.image.includes('facebook') ? (
                                    <Image
                                    centered
                                    circular
                                    src={`https://graph.facebook.com/${this.props.profile.fid}/picture?type=large`}
                                    size='small'
                                    />
                                ) : (
                                    <Image
                                    centered
                                    circular
                                    src={this.props.profile.image}
                                    size='small'
                                    />
                                )
                            }
                            <h2>{this.props.profile.name}</h2>
                            <p>Email: {` ${this.props.profile.email}`}</p>
                            <Button
                            fluid size='medium'
                            color='red'
                            content='Logout'
                            onClick={this.logout}
                            />
                        </div>
                    </Modal.Content>
                </Modal>
            ) : (
                <Modal size={'mini'} trigger={<Icon className='cursor' name='user plus' size='large'/>}>
                    <Modal.Content>
                        <div>
                            {/*<Button onClick={this.facebookLogin} fluid size={'medium'} color='facebook'>*/}
                                {/*<Icon name='facebook' size={'big'}  /> Login with Facebook*/}
                            {/*</Button>*/}
                        {/*</div>*/}
                            {/*<Divider horizontal>Or</Divider>*/}
                        {/*<div>*/}
                            {/*<Button onClick={this.googleLogin} fluid size={'medium'} color='google plus'>*/}
                                {/*<Icon name='google plus' size={'big'} /> Login with Google */}
                            {/*</Button>*/}
                        </div>
                    </Modal.Content>
                </Modal>
            )
        );
    }
};


const mapStateToProps = (state) => ({
  isAuthenticated: !!state.auth.uid,
  profile: state.auth
});

const mapDispatchToProps = (dispatch) => ({
    startGoogleLogin: () => dispatch(startGoogleLogin()),
    startFacebookLogin: () => dispatch(startFacebookLogin()),
    startLogout: () => dispatch(startLogout())
});


export default connect(mapStateToProps, mapDispatchToProps)(AuthButton);
