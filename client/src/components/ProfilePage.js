import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Button, Container, Table, Header, Form, Dimmer, Loader, Image, Segment, Card, Icon } from 'semantic-ui-react';
import * as API from '../utils/apiCaller';
import {Redirect} from 'react-router-dom';
import ReactNotification from "react-notifications-component";
import "react-notifications-component/dist/theme.css";

export class ProfilePage extends React.Component {
    constructor(props){
        super(props);
        this.addNotification = this.addNotification.bind(this);
        this.notificationDOMRef = React.createRef();
        this.state = {
            profile:{
                name: '',
                email: '',
                address: '',
                phone: '',
                avatar: ''
            },
            isLoading: false,
            submitted: false
        }
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleNewImage = this.handleNewImage.bind(this);
    }


     componentWillMount(){
        let self = this;
        var user = JSON.parse(localStorage.getItem("AccountData"));
        if (user != null) {
            let profile = {...self.state.profile};
            profile["avatar"] = user.avatar;
            profile["name"] = user.fullname;
            profile["email"] = user.email;
            profile["address"] = user.address;
            profile["phone"] = user.phone;
            self.setState({ profile: profile });
        }
     }

     addNotification() {
        this.notificationDOMRef.current.addNotification({
          title: "Success",
          message: "Profile was updated",
          type: "success",
          insert: "top",
          container: "top-right",
          animationIn: ["animated", "fadeIn"],
          animationOut: ["animated", "fadeOut"],
          dismiss: { duration: 2000 },
          dismissable: { click: true }
        });
      }

    handleNewImage = e => {
      let self = this;
      self.setState({ isLoading: true });
      var file = e.target.files[0]
      var reader = new FileReader();
      reader.onloadend = function() {
         var b64 = reader.result.split('base64,')[1];
         var xhr=new XMLHttpRequest();
         var formData = new FormData();
         formData.append("image", b64);
         xhr.open("POST", "https://api.imgur.com/3/image");
         xhr.setRequestHeader("Authorization", "Client-ID b05581f073b24c4");
         xhr.onreadystatechange = function() {
            self.setState({ isLoading: false });
            if (xhr.readyState == XMLHttpRequest.DONE) {
                var imgurResponse = JSON.parse(xhr.responseText);
                if (imgurResponse.success) {
                    var link = imgurResponse.data.link;
                    let profile = {...self.state.profile};
                    profile["avatar"] = link;
                    self.setState({ profile: profile });
                    self.handleSubmit();

                }
            }
         }
         xhr.send(formData);
      }
      reader.readAsDataURL(file);
    }

    handleChange = input => event => {
        let self = this;
        let profile = {...self.state.profile};
        profile[input] = event.target.value;
        self.setState({ profile: profile })
    }

    handleSubmit = () => {
        let self = this;
        //console.log(self.state.profile);
        self.setState({ submitted: true });
        self.setState({ isLoading: true });
        for (var item in self.state.profile) {
            if (typeof self.state.profile[item] === "undefined")
                self.state.profile[item] = "";
        }
        let opts = {
            'action': 'profile',
            'data': this.state.profile
        };
        API.callApi(opts)
            .then(function(response) {
                return response.json();
            }).then(function(data) {
                //console.log("payload : ", data);
                if(data && data.status == 'ok') {
                    let opts = { 'action': 'account' };
                    API.callApi(opts)
                    .then(function(response) {
                        return response.json();
                    }).then(function(data) {
                        if(data && data.status == 'ok') {
                            self.setState({ isLoading: false });
                            self.setState({ submitted: false });
                            localStorage.setItem("AccountData", JSON.stringify(data.account));
                            self.addNotification();
                        } else {
                            //handle response error
                        }
                    });
                } else {
                    self.setState ({ isLoading: false });
                    self.setState({ submitted: false });
                    //handle response error
                }
           });
    }

    render(){
        return(
            <Container className='page-top-margin'>
                <div>
                <Header as='h2'>Profile Details</Header>
                   <ReactNotification ref={this.notificationDOMRef} />
                <Table>
                  <Table.Row style={{height: "512px"}}>
                  <Table.Cell>
                  {
                    <Form style={{height: "512px"}}>
                        <Form.Field>
                        <label>Name</label>
                        <input style={{width: "512px"}} placeholder='Name' value={this.state.profile.name} onChange={this.handleChange('name')}/>
                        </Form.Field>
                        <Form.Field>
                        <label>Address</label>
                        <input style={{width: "512px"}} placeholder='Address' value={this.state.profile.address} onChange={this.handleChange('address')}/>
                        </Form.Field>
                        <Form.Field>
                        <label>Email</label>
                        <input disabled style={{width: "512px"}} placeholder='Email' value={this.state.profile.email}/>
                        </Form.Field>
                        <Form.Field>
                        <label>Phone</label>
                        <input style={{width: "512px"}} placeholder='Phone' value={this.state.profile.phone} onChange={this.handleChange('phone')}/>
                        </Form.Field>
                     </Form>
                    }
                    </Table.Cell>

                    <Table.Cell>
                      {this.state.isLoading && <img src="/images/loader.gif" /> }
                    </Table.Cell>

                        <Table.Cell verticalAlign='top'>
                                <Image floated='right' size='small' src={this.state.profile.avatar} />
                                <br/>
                                 <input onChange={this.handleNewImage} type="file" class="inputfile" id="embedpollfileinput" />
                                  <label for="embedpollfileinput" class="ui medium grey right floated button">
                                      <i class="ui upload icon"></i>
                                      Upload image
                                  </label>
                        </Table.Cell>
                    </Table.Row>
                    </Table>

                       <Form>
                          <Button type='submit' onClick={this.handleSubmit} disabled={this.state.submitted}>Update</Button>
                      </Form>
                </div>
            </Container>
        );
    }
}

const mapStateToProps = (state) => ({
    cart: state.shoppingCart
});

export default connect(mapStateToProps)(ProfilePage);