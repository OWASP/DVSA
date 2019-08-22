import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Container, Header, Table, Segment } from 'semantic-ui-react';
import * as API from '../utils/apiCaller';
import { Redirect, HashRouter } from 'react-router-dom';

export class InboxPage extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            messages:[],
            isLoading: true,
        };
    }

    componentWillMount(){
        let opts = {
            'action': 'inbox'
        };
        let self = this;
        API.callApi(opts)
            .then(function(response) {
                return response.json();
            }).then(function(data) {
                //console.log("payload : ", data);
                if(data && data.status == 'ok') {
                    self.setState({ isLoading: false });
                    self.setState ({ messages: data.messages });
                } else {
                    self.setState ({ isLoading: false });
                    //handle response error
                }
           });
    }

    render(){
        return(
            <Container className='page-top-margin'>
                <Header as='h2'>My Inbox</Header>
                {this.state.isLoading && <img src="/images/loader.gif" /> }
                <Table striped bordered>
                    <Table.Header>
                          <Table.Row>
                            <Table.HeaderCell>Date</Table.HeaderCell>
                            <Table.HeaderCell>ID</Table.HeaderCell>
                            <Table.HeaderCell>Subject</Table.HeaderCell>
                            <Table.HeaderCell>From</Table.HeaderCell>
                          </Table.Row>
                       </Table.Header>

                       <Table.Body>
                            {
                                this.state.messages.map( x=>(
                                       <Table.Row>
                                            <Table.Cell>{x["date"].split('.')[0].replace("T", " ")}</Table.Cell>
                                            <Table.Cell><Link to={'/inbox/'+x["msg-id"]}><a href="">{x["msg-id"]}</a></Link></Table.Cell>
                                            <Table.Cell>{x["subject"]}</Table.Cell>
                                            <Table.Cell>{x["sender"]}</Table.Cell>
                                      </Table.Row>
                                ) )
                            }
                       </Table.Body>
                   </Table>

            </Container>
        );
    }
}

const mapStateToProps = (state) => ({
    cart: state.shoppingCart
});

export default connect(mapStateToProps)(InboxPage);