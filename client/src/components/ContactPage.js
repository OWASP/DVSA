import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Button, Container, Table, Header, Form, Dimmer, Loader, Image, Segment, Card, Icon } from 'semantic-ui-react';
import * as API from '../utils/apiCaller';
import {Redirect} from 'react-router-dom';
import ReactNotification from "react-notifications-component";
import "react-notifications-component/dist/theme.css";


function generate_UUID(){
    var dt = new Date().getTime();
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (dt + Math.random()*16)%16 | 0;
        dt = Math.floor(dt/16);
        return (c=='x' ? r :(r&0x3|0x8)).toString(16);
    });
    return uuid;
}

export class ContactPage extends React.Component {
    constructor(props){
        super(props);
        var ReactS3Uploader = require('react-s3-uploader');
        this.addNotification = this.addNotification.bind(this);
        this.notificationDOMRef = React.createRef();
        this.state = {
            isLoading: false,
            submitted: false,
            file: null,
            signedUrl: null,
            feedback: {
                attachment: '',
                name: '',
                email: '',
                phone: '',
                subject: '',
                message: ''
            }
        }
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

     componentWillMount(){
        let self = this;
        var user = JSON.parse(localStorage.getItem("AccountData"));
        if (user != null) {
            let feedback = {...self.state.feedback};
            feedback["name"] = user.fullname;
            feedback["email"] = user.email;
            feedback["phone"] = user.phone;
            self.setState({ feedback: feedback });
        }
     }

  addNotification() {
    this.notificationDOMRef.current.addNotification({
      title: "Sent",
      message: "Thank you!",
      type: "success",
      insert: "top",
      container: "top-right",
      animationIn: ["animated", "fadeIn"],
      animationOut: ["animated", "fadeOut"],
      dismiss: { duration: 2000 },
      dismissable: { click: true }
    });
  }

    handleAttachment = e => {
        var f = e.target.value;
        var fname = f.replace("C:\\fakepath\\", "");
        let opts = {
            'action': 'upload',
            'attachment': fname
        };
        let self = this;
        self.setState({ file: f });
        API.callApi(opts).then(function(response) {
            return response.json();
        }).then(function(data) {
            data = JSON.parse(data);
            self.setState({ signedUrl: data });
            let feedback = {...self.state.feedback};
            feedback["attachment"] = data.fields.key;
            self.setState({ feedback: feedback })
       });
    }

    handleChange = input => event => {
        let self = this;
        let feedback = {...self.state.feedback};
        feedback[input] = event.target.value;
        self.setState({ feedback: feedback })
    }

    handleSubmit = () => {
        let self = this;
        self.setState({ submitted: true });
        self.setState({ isLoading: true });
        if (self.state["signedUrl"]) {
            var s3Data = self.state["signedUrl"];
            var ufile = document.getElementById('embedpollfileinput').files[0];
            var data = new FormData();
            for (var key in s3Data.fields) {
                data.append(key, s3Data.fields[key]);
            }
            data.append('file', ufile);
            var xhr = new XMLHttpRequest();
            console.log(s3Data.url);
            xhr.open("POST", s3Data.url, true);
            xhr.onreadystatechange = function() {
                if(xhr.readyState === 4){
                    if(xhr.status === 200 || xhr.status === 204){
                    }
                    else{
                        //alert("Could not upload file.");
                    }
                }
            };
            xhr.send(data);
        }

        for (var item in self.state.feedback) {
            if (typeof self.state.feedback[item] === "undefined")
                self.state.feedback[item] = "";
        }

        let opts = {
            'action': 'feedback',
            'data': this.state.feedback
        };
        API.callApi(opts)
            .then(function() {}).then(function(data) {
                self.addNotification();
                self.setState({ isLoading: false });
                self.setState({ submitted: false });
        });
    }

    render(){

        return(
            <Container className='page-top-margin'>
                <div>
                <Header as='h2'>Feedback Information</Header>
                <ReactNotification ref={this.notificationDOMRef} />
                <Table>
                  <Table.Row style={{height: "512px"}}>
                  <Table.Cell>
                  {
                    <Form style={{height: "512px"}}>
                        <Form.Field>
                        <label>Your Name</label>
                        <input style={{width: "256px"}} placeholder='Name' value={this.state.feedback.name} onChange={this.handleChange('name')}/>
                        </Form.Field>
                        <Form.Field>
                        <label>Your Email</label>
                        <input disabled style={{width: "256px"}} placeholder='Email' value={this.state.feedback.email}/>
                        </Form.Field>
                        <Form.Field>
                        <label>Your Phone</label>
                        <input style={{width: "256px"}} placeholder='Phone' value={this.state.feedback.phone} onChange={this.handleChange('phone')}/>
                        </Form.Field>
                        <Form.Field>

                        <label>Subject</label>
                        <input style={{width: "512px"}} placeholder='Subject' value={this.state.feedback.subject} onChange={this.handleChange('subject')}/>
                        </Form.Field>

                        <Form.Field>
                        <label>Message</label>
                        <textarea style={{width: "512px"}} placeholder='' value={this.state.feedback.message} onChange={this.handleChange('message')}/>
                        </Form.Field>

                     </Form>
                    }
                    </Table.Cell>

                    <Table.Cell>
                      {this.state.isLoading && <img src="/images/loader.gif" /> }
                    </Table.Cell>
                        <Table.Cell verticalAlign='top'>
                        <Table.Row>
                                <br/>
                                 <input onChange={this.handleAttachment} type="file" class="inputfile" id="embedpollfileinput" />
                                  <label for="embedpollfileinput" class="ui medium grey right floated button">
                                      <i class="ui upload icon"></i>
                                      Attach file
                                  </label>
                            </Table.Row>
                          <Table.Row>
                                <br/>
                                {this.state.file && <label> {this.state.file} </label>}
                           </Table.Row>
                        </Table.Cell>

                    </Table.Row>
                    </Table>

                       <Form>
                          <Button type='submit' onClick={this.handleSubmit} disabled={this.state.submitted}>Send Feedback</Button>
                      </Form>
                </div>

            </Container>
        );
    }
}


const mapStateToProps = (state) => ({
    cart: state.shoppingCart
});

export default connect(mapStateToProps)(ContactPage);