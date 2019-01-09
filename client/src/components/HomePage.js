import React from 'react';
import { Link } from 'react-router-dom';
import { Button, Segment, Image, Container } from 'semantic-ui-react';
import Footer from '../components/Footer';

export default class HomePage extends React.Component {

    render() {
        return (
            <div>
               <div className='home-bg centered'>
                    <div className='home-main'>
                        <h2>ReactJS e-commerce Web App</h2>
                        <div className='centered'>
                            <Link to='/store'>
                                <Button inverted color='teal' content='View Store' />
                            </Link>
                        </div>
                    </div>
               </div>
               <Container className='home-desc'>
                    <Segment raised>
                        <div className='home-content centered'>

                        </div>
                    </Segment>
                </Container>
                <Footer />
            </div>
            
        );
    }
}

