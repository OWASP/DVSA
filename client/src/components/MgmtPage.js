import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Button, Segment, Container, Label, Grid, Image, Header, Icon, IconGroup } from 'semantic-ui-react';
import * as API from '../utils/apiCaller';
import { Redirect } from 'react-router-dom';
import { Progress } from 'semantic-ui-react'


export class MgmtPage extends React.Component {

    constructor(props){
        super(props);
        this.state = {
            email: "",
            profileBar: 3,
            submitted: false,
            isLoading: false,
            learningProgressOrderManager: 0,
            learningProgressSendEmail: 0,
            learningProgressCreateReceipt: 0,
            learningProgressFeedbackUpload: 0,
            position: 0,
        }
        this.initLearning = this.initLearning.bind(this);
        this.profileManager = this.profileManager.bind(this);
        this.profileSendEmail = this.profileSendEmail.bind(this);
        this.profileFeedback = this.profileFeedback.bind(this);
    }


    profileManager(){
        let self = this;
        for (var i = 0; i <= self.state.profileBar; i++) {
            var fname = "protego-tmp-" + Math.random().toString(36).substring(2, 15);
            var fcontent = "This-is-a-tmp-file-for-learning";
            let opts = {
                'action': 'new',
                'cart-id': '12341234-1234-1234-1234-123412341234',
                'items': {"13": 1},
            };
            API.callApi(opts).then(function(response) {
                return response.json();
            }).then(function(data) {
                let opts = {
                    'action': 'shipping',
                    'order-id': data["order-id"],
                    'data': {"name":"dummy", "address":"dummy", "email": self.state.email, "phone":"+1123123123"},
                };
                API.callApi(opts).then(function(response) {
                    return response.json();
                }).then(function(data) {
                    let opts = {
                        'action': 'billing',
                        'order-id': data["order-id"],
                        'data': {"ccn":"5555555555555557","exp":"02/33","cvv":"333"},
                    };
                    API.callApi(opts).then(function(response) {
                        return response.json();
                    }).then(function(data) {
                        var prog = self.state.learningProgressOrderManager + 1;
                        if (prog > 100) {
                            prog = 100;
                        }
                        self.setState({ learningProgressOrderManager: prog });
                        self.setState({ learningProgressCreateReceipt: prog });
                    });
                });
            });
        }
    }

    profileSendEmail(){
        let self = this;
        let opts = {
                'action': 'inbox',
        };
        API.callApi(opts).then(function(response) {
            return response.json();
        }).then(function(data) {
            self.setState({ learningProgressSendEmail: data.messages.length });
            console.log(data.messages.length);
        });
    }

    profileFeedback() {
        let self = this;
        for (var i = 0; i <= self.state.profileBar; i++) {
            var fname = "protego-tmp-" + Math.random().toString(36).substring(2, 15);
            var fcontent = "This-is-a-tmp-file-for-learning";
            let opts = {
                'action': 'upload',
                'attachment': fname,
            };
            API.callApi(opts).then(function(response) {
                return response.json();
            }).then(function(data) {
                var formdata = new FormData();
                for(var key in data.fields){
                    formdata.append(key, data.fields[key]);
                }
                formdata.append('file', fcontent);
                var xhr = new XMLHttpRequest();
                xhr.open("POST", data.url, true);
                xhr.onreadystatechange = function() {
                    if(xhr.readyState === 4){
                        if(xhr.status === 200 || xhr.status === 204){

                        }
                        else{
                            //alert("Could not upload file.");
                        }
                        var prog = self.state.learningProgressFeedbackUpload + 1;
                        if (prog > 100) {
                            prog = 100;
                        }
                        self.setState({ learningProgressFeedbackUpload: prog });
                    }
                };
                xhr.send(formdata);
            });
        }
     }

    initLearning = () => {
        var userData = JSON.parse(localStorage.getItem("AccountData"));
        if (typeof userData["email"] != "unidentified" ) {
            this.setState({ email: userData["email"] });
        }
        else {
            alert('Undefined email address. Might not profile properly...');
        }
        this.profileManager();
        setInterval(this.profileSendEmail,3000);
        //this.profileFeedback();
        //console.log(self.state.profile);
        this.setState({ submitted: true });
       // this.setState({ isLoading: true });
    }


    render(){
        return(
            <Container className='page-top-margin'>
                <img src="/images/protegologo.png" width="256px"/>
                <br/><br/>
                <h2>Welcome to Protego Workshop</h2>
                <br/><br/>
                <div>
                    <p>First thing first, let's start the behavioral profiling. Please click on the button below and wait for the confirmation.</p>
                    <br/>
                    <Button type='submit' onClick={this.initLearning} disabled={this.state.submitted}>Start Profiling</Button>
                      {this.state.isLoading && <img src="/images/loader.gif" /> }
                    <br/><br/>
                    { this.state.submitted &&
                        <div>
                        DVSA-ORDER-MANAGER-JS:  <Progress indicating style={{width:"66%"}} percent={this.state.learningProgressOrderManager} progress />
                        DVSA-CREATE-RECEIPT: <Progress indicating style={{width:"66%"}} percent={this.state.learningProgressCreateReceipt} progress />
                        DVSA-SEND-RECEIPT-EMAIL: <Progress indicating style={{width:"66%"}} percent={this.state.learningProgressSendEmail} progress />
                        DVSA-FEEDBACK-UPLOADS: <Progress indicating style={{width:"66%"}} percent={this.state.learningProgressFeedbackUpload} progress />
                        </div>
                    }
                </div>

            </Container>

        );
    }
}

const mapStateToProps = (state) => ({
    cart: state.shoppingCart,
});

export default connect(mapStateToProps)(MgmtPage);