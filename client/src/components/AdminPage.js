import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Container, Header, Table, Segment, Form, Button } from 'semantic-ui-react';
import * as API from '../utils/apiCaller';
import { Redirect, HashRouter } from 'react-router-dom';

export class AdminPage extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            orders:[],
            orderFilters: {
                from: "",
                to: "",
                orderid: "",
                userid: "",
                status: "",
            },
            isLoading: false,
            submitted: false,
        };
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.statuses = {
            "100": "incomplete",
            "110": "payment failed",
            "120": "paid",
            "200": "processed",
            "210": "shipped",
            "300": "delivered",
            "500": "cancelled",
            "600": "rejected"
        };
    }

    handleChange = input => event => {
        let self = this;
        let ordrs = {...self.state.orderFilters};
        ordrs[input] = event.target.value;
        self.setState({ orderFilters: ordrs })
    }

    handleSubmit(){
        let self = this;
        self.setState({ submitted: true });
        self.setState({ isLoading: true });
        var data = {};
        for (var item in self.state.orderFilters) {
            console.log("[" + self.state.orderFilters[item] + "]");
            if (typeof self.state.orderFilters[item] === "undefined" || self.state.orderFilters[item].length === 0) {
            }
            else {
                data[item] = self.state.orderFilters[item];
            }
        }
        console.log(data);
        let opts = {
            'action': 'admin-orders',
            'data': data
        };
        API.callApi(opts)
            .then(function(response) {
                return response.json();
            }).then(function(data) {
                console.log(data);
                //console.log("payload : ", data);
                console.log(data);
                if(data.status == 'ok') {
                    self.setState ({ isLoading: false });
                    self.setState ({ submitted: false });
                    self.setState ({ orders: data.orders });
                }
                else {
                    self.setState ({ isLoading: false });
                    self.setState ({ submitted: false });
                    alert(data.message);
                    //handle response error
                }
           });
    }

    componentWillMount(){
        this.handleSubmit();
    }

    render(){
        return(
            <Container className='page-top-margin'>
                <Header as='h2'>Orders</Header>
                <div>
                 <Table striped bordered>
                 <Table.Body>
                 <Table.Row>
                 <Table.Cell>
                 {
                 <Form>

                   <Form.Field>
                      <Table.Cell width={2}>   <input disabled placeholder='From' value={this.state.orderFilters.from} onChange={this.handleChange('from')}/></Table.Cell>

                      <Table.Cell width={2}>   <input disabled placeholder='To' value={this.state.orderFilters.to} onChange={this.handleChange('to')}/></Table.Cell>

                      <Table.Cell width={4}>  <input disabled placeholder='Order' value={this.state.orderFilters.orderid} onChange={this.handleChange('orderid')}/></Table.Cell>

                      <Table.Cell width={4}>      <input disabled placeholder='User' value={this.state.orderFilters.userid} onChange={this.handleChange('userid')}/></Table.Cell>

                      <Table.Cell width={2}>     <input disabled placeholder='Status' value={this.state.orderFilters.status} onChange={this.handleChange('status')}/></Table.Cell>
                    </Form.Field>
                 </Form>
                 }
                </Table.Cell>
                 </Table.Row>

                 <Table.Row>
                  <Table.Cell>
                    <Form>
                          <Button type='submit' onClick={this.handleSubmit} disabled={this.state.submitted}>Get Orders</Button>
                    </Form>
                    </Table.Cell>
                </Table.Row>
                </Table.Body>
                </Table>

                </div>
                <br/>  <br/>
                <div>
                {this.state.isLoading && <img src="/images/loader.gif" /> }
                <Table striped bordered>
                    <Table.Header>
                          <Table.Row>
                            <Table.HeaderCell>Date</Table.HeaderCell>
                            <Table.HeaderCell>Order ID</Table.HeaderCell>
                            <Table.HeaderCell>User ID</Table.HeaderCell>
                            <Table.HeaderCell>Status</Table.HeaderCell>
                            <Table.HeaderCell>Total</Table.HeaderCell>
                            <Table.HeaderCell>Confirmation</Table.HeaderCell>
                          </Table.Row>
                       </Table.Header>

                       <Table.Body>
                            {
                                this.state.orders.map( x=>(
                                       <Table.Row>
                                            <Table.Cell>{new Date(x["paymentTS"]*1000).toLocaleString()}</Table.Cell>
                                            <Table.Cell><Link to={'/orders/'+x["orderId"]}><a href="">{x["orderId"]}</a></Link></Table.Cell>
                                            <Table.Cell>{x["userId"]}</Table.Cell>
                                            <Table.Cell>{this.statuses[x["orderStatus"]]}</Table.Cell>
                                            <Table.Cell>${x["totalAmount"]}</Table.Cell>
                                            <Table.Cell>{x["confirmationToken"]}</Table.Cell>
                                      </Table.Row>
                                ) )
                            }
                       </Table.Body>
                   </Table>
                </div>
            </Container>
        );
    }
}

const mapStateToProps = (state) => ({
    cart: state.shoppingCart
});

export default connect(mapStateToProps)(AdminPage);