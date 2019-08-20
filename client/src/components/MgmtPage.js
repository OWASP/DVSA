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
            submitted: false,
            learningProgress: 0,
        }
        this.initLearning = this.initLearning.bind(this);
    }

    initLearning = () => {
        var actions = [];
        let self = this;
        //console.log(self.state.profile);
        self.setState({ submitted: true });
        for (var i = 0; i <= 100; i++) {

            self.setState({ learningProgress: i });
        }

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
                    <br/><br/>
                    <Progress style={{width:"66%"}} percent={this.state.learningProgress} progress />


                </div>

            </Container>

        );
    }
}

const mapStateToProps = (state) => ({
    cart: state.shoppingCart,
});

export default connect(mapStateToProps)(MgmtPage);