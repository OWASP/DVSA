import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Container, Header, Table, Segment } from 'semantic-ui-react';
import * as API from '../utils/apiCaller';
import { Redirect, HashRouter } from 'react-router-dom';

export class OrdersPage extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            orders:[],
            isLoading: true,
        };
    }

    componentWillMount(){
        let opts = {
                    'action': 'orders'
        };
        let self = this;
        API.callApi(opts)
            .then(function(response) {
                return response.json();
            }).then(function(data) {
                //console.log("payload : ", data);
                if(data && data.status == 'ok') {
                    self.setState({ isLoading: false });
                    self.setState ({ orders: data.orders });
                } else {
                    self.setState ({ isLoading: false });
                    //handle response error
                }
           });
    }

    render(){
        return(
            <Container className='page-top-margin'>
                <Header as='h2'>My Orders</Header>
                {this.state.isLoading && <img src="/images/loader.gif" /> }
                <Table striped bordered>
                    <Table.Header>
                          <Table.Row>
                            <Table.HeaderCell>Date</Table.HeaderCell>
                            <Table.HeaderCell>ID</Table.HeaderCell>
                            <Table.HeaderCell>Status</Table.HeaderCell>
                            <Table.HeaderCell>Total</Table.HeaderCell>
                            <Table.HeaderCell>Confirmation</Table.HeaderCell>
                          </Table.Row>
                       </Table.Header>

                       <Table.Body>
                            {
                                this.state.orders.map( x=>(
                                       <Table.Row>
                                            <Table.Cell>{new Date(x["date"]*1000).toLocaleString()}</Table.Cell>
                                            <Table.Cell><Link to={'/orders/'+x["order-id"]}><a href="">{x["order-id"]}</a></Link></Table.Cell>
                                            <Table.Cell>{x["status"]}</Table.Cell>
                                            <Table.Cell>${x["total"]}</Table.Cell>
                                            <Table.Cell>{x["token"]}</Table.Cell>
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

export default connect(mapStateToProps)(OrdersPage);