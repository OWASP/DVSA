import React from 'react';
import { Link } from 'react-router-dom';
import { Image, Button, Icon, Grid } from 'semantic-ui-react';
const src = '/images/404.jpg';

const NotFoundPage = () => (
    <Grid centered>
        <Grid.Row>
            <Image src={src} centered size='large' />
        </Grid.Row>
        <Grid.Row>
            <Button basic color='blue' size={'large'}>
                <Icon name='angle double left' /><Link to="/">Go Home</Link>
            </Button>
        </Grid.Row>
    </Grid>
);

export default NotFoundPage;