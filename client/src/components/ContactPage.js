import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Button, Container, Table, Header, Form, Dimmer, Loader, Image, Segment, Card, Icon } from 'semantic-ui-react';
import * as API from '../utils/apiCaller';
import {Redirect} from 'react-router-dom';
import ReactNotification from "react-notifications-component";
import "react-notifications-component/dist/theme.css";


export class ContactPage extends React.Component {
    constructor(props){
        super(props);
        var ReactS3Uploader = require('react-s3-uploader');
        this.addNotification = this.addNotification.bind(this);
        this.notificationDOMRef = React.createRef();
        var user = JSON.parse(localStorage.getItem("AccountData"));
        this.state = {
            isLoading: false,
            submitted: false,
            feedback: {
                name: user.fullname,
                email: user.email,
                phone: user.phone,
                subject: '',
                message: ''
            }
        }
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
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
        alert(f);
        let opts = {
            'action': 'feedback'
            'attachment': f;
        };
        API.callApi(opts)
            .then(function(response) {return response.json();}).then(function(data) {
                   alert(data);
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
                        <textarea style={{width: "512px"}} placeholder='Subject' value={this.state.feedback.message} onChange={this.handleChange('message')}/>
                        </Form.Field>

                     </Form>
                    }
                    </Table.Cell>

                    <Table.Cell>
                      {this.state.isLoading && <img src="/images/loader.gif" /> }
                    </Table.Cell>

                        <Table.Cell verticalAlign='top'>
                                <br/>
                                 <input onChange={this.handleAttachment} type="file" class="inputfile" id="embedpollfileinput" />
                                  <label for="embedpollfileinput" class="ui medium grey right floated button">
                                      <i class="ui upload icon"></i>
                                      Attach file
                                  </label>
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