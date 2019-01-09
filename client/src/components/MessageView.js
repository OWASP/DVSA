import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import base64 from 'react-native-base64'
import { Container, Header, Button, Table, Segment } from 'semantic-ui-react';
import * as API from '../utils/apiCaller';
import { Redirect, HashRouter } from 'react-router-dom';

export class MessageView extends React.Component {
    constructor(props){
        super(props);
        const id = window.location.pathname.split('/')[2];
        this.state = {
            msgId: id,
            msgData: "",
            isLoading: true,
            toInbox: false
        };
    }


    handleDelete = () => {
        let opts = {
                    'action': 'delete',
                    'msg-id': this.state.msgId
        };
        let self = this;
        API.callApi(opts)
            .then(function(response) {
                return response.json();
            }).then(function(err, data) {
                if(data && data.status == 'ok') {
                    self.setState ({ isLoading: false });
                    self.setState ({ toInbox: true});
                } else {
                    self.setState ({ isLoading: false });
                    self.setState ({ toInbox: true});
                }
           });
    }

    componentWillMount(){
        let self = this;
        let opts = {
                    'action': 'message',
                    'msg-id': self.state.msgId,
                    'type': 'html'
        };
        API.callApi(opts)
            .then(function(response) {
                return response.json();
            }).then(function(err, data) {
                if(data && data.status == 'ok') {
                    self.setState ({ isLoading: false });
                    self.setState ({ msgData: data.message });
                } else {
                    //console.log(err.message);
                    self.setState ({ isLoading: false });
                    self.setState ({ msgData: err.message });
                }
           });
    }

    render(){
        if (this.state.toInbox === true) {
            return <Redirect to='/inbox' />
        }
        return(
            <Container className='page-top-margin'>
            {this.state.isLoading && <img src="/images/loader.gif" /> }
                <div>
                     <h2>Message {this.state.msgId} </h2>
                     <br/><br/>
                          <div>
                            { base64.decode(this.state.msgData).indexOf('</') !== -1
                                ? (
                                    <div dangerouslySetInnerHTML={{__html: base64.decode(this.state.msgData).replace(/(<? *script)/gi, 'illegalscript')}} >
                                    </div>
                                  )
                                : this.props.textOrHtml
                              }

                          </div>
                    <br/><br/>
                    <Button type='submit' color='red' onClick={this.handleDelete}>Delete Message</Button>
                 </div>
            </Container>
        );
    }
}


const mapStateToProps = (state) => ({
    cart: state.shoppingCart,
});

export default connect(mapStateToProps)(MessageView);