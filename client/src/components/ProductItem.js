import React from 'react';
import { Link } from 'react-router-dom';
import { Image, Label, Rating, Button, Icon, Dimmer } from 'semantic-ui-react';

export default class ProductItem extends React.Component {
    state = {
        isWatched: false
    };

    handleShow = () => this.setState({ active: true });
    handleHide = () => this.setState({ active: false });

    addToWatch = () => {
        if(this.state.isWatched){
            this.setState({isWatched: false});
        }else{
            this.setState({isWatched: true});
        }
    }



    render(){
        
        const { active } = this.state;
        const content = (
            <div>
                <Link to={`/store/${this.props.id}`}>
                    <Button basic inverted>V i e w</Button>
                </Link>
            </div>
        );
        return (
            <div className="card">
                <Dimmer.Dimmable
                    as={Image}
                    label={{ribbon: true, size: 'tiny',color: 'teal', content: <h5>{`$${this.props.price}`}</h5> }}
                    dimmed={active}
                    dimmer={{ active, content }}
                    onMouseEnter={this.handleShow}
                    onMouseLeave={this.handleHide}
                    size='huge'
                    src={this.props.images[0].url}
                />
                <div className="card-container">
                    <div className='card-name_price'>
                        <div>
                            <h4>{this.props.title}</h4>
                        </div>
                    </div>
                    <div className='card-rating'>
                        <div>
                            <div><p>{this.props.type}</p></div>
                            <div><Rating maxRating={5} defaultRating={3} icon='star' size='small' /></div>
                        </div>
                        <div className='card-heart'>
                            <Icon 
                            className='cursor' 
                            onClick={this.addToWatch} 
                            color={this.state.isWatched ? 'red': 'black'} 
                            name='heart outline' 
                            size='large' />
                        </div>
                    </div>
                </div>
            </div>
            );
    }
}


