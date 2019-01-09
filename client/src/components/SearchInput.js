import _ from 'lodash'
import React, { Component } from 'react'
import { Search, Grid, Image } from 'semantic-ui-react'
import { Link } from 'react-router-dom';

export default class SearchExampleStandard extends Component {
  componentWillMount() {
    this.resetComponent()
  }

  resRender = ({ title, price, image, type, productid }) => (
    <Link to={`/store/${productid}`} >
      <div key={productid} className='search-popout'>
        <div key='image' className='image'>
          <Image src={image} size='small' />
        </div>
        <div key='content' className='content'>
          {price && <div className='price'>${price}</div>}
          {title && <div className='title'>{title}</div>}
          {type && <div className='description'>{type}</div>}
        </div>
      </div>
    </Link>
  );

  resetComponent = () => this.setState({ isLoading: false, results: [], value: '' })

  handleResultSelect = (e, { result }) => this.setState({ value: '' })

  handleSearchChange = (e, { value }) => {
    this.setState({ isLoading: true, value })

    setTimeout(() => {
      if (this.state.value.length < 1) return this.resetComponent()

      const re = new RegExp(_.escapeRegExp(this.state.value), 'i')
      const isMatch = result => re.test(result.title)

      this.setState({
        isLoading: false,
        results: _.filter(this.props.products, isMatch),
      })
    }, 300)
  }

  render() {
    const { isLoading, value, results } = this.state
    
    return (
      <div>
          <Search
            loading={isLoading}
            onResultSelect={this.handleResultSelect}
            onSearchChange={_.debounce(this.handleSearchChange, 500, { leading: true })}
            results={results}
            value={value}
            resultRenderer={this.resRender}
          />
      </div>
    )
  }
}