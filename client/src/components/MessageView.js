import React from 'react';
import { connect } from 'react-redux';
import base64 from 'react-native-base64'
import { Container, Header, Table, Segment } from 'semantic-ui-react';
import * as API from '../utils/apiCaller';
import { Redirect } from 'react-router-dom';

export class MessageView extends React.Component {
    constructor(props){
        super(props);
        const id = window.location.pathname.split('/')[2];
        this.state = {
            msgId: id,
            msgData: "",
            isLoading: true
        };
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
                    self.setState ({ isLoading: false });
                    self.setState ({ msgData: err.message });
                }
           });
    }

    render(){
        return(
            <Container className='page-top-margin'>
            {this.state.isLoading && <img src="/images/loader.gif" /> }
                <div>
                     <h2>Message {this.state.msgId} </h2>
                     <br/><br/>
                          <div>
                            { 
                                <div dangerouslySetInnerHTML={{__html: base64.decode(this.state.msgData).replace(/(<? *script)/gi, 'illegalscript')}} >
                                </div>
                            }
                          </div>
                 </div>
            </Container>
        );
    }
}


const mapStateToProps = (state) => ({
    cart: state.shoppingCart,
});

export default connect(mapStateToProps)(MessageView);