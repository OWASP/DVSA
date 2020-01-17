import React, { Component } from 'react';
import { connect } from 'react-redux';
import { Sidebar, Segment, Button, Menu, Image, Icon, Header, Label, Form, Input } from 'semantic-ui-react';
import ProductList from './ProductList';
import { sortByMaxPrice, sortByMinPrice, setMinPrice, setMaxPrice, setBrand, setCategory} from '../actions/filters';
import selectProducts from '../selectors/productsFilter';
import { getBrands, getCategories } from '../selectors/product';
import { isMobile } from 'react-device-detect';
import Footer from "./Footer";
import * as API from '../utils/apiCaller';


export class StorePage extends Component {
  state = { visible: isMobile ? false : true  }

  sleep(ms){
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  componentDidMount() {

        let opts = { 'action': 'account' };
        API.callApi(opts)
        .then(function(response) {
            return response.json();
        }).then(function(data) {
            if(data && data.status == 'ok') {
                localStorage.setItem("AccountData", JSON.stringify(data.account));
            } else {
                if (data.status == "err" && data.msg == "could not find user") {
                    sleep(5000);
                    API.callApi(opts)
                    .then(function(response) {
                        return response.json();
                    }).then(function(data) {
                        if(data && data.status == 'ok') {
                            localStorage.setItem("AccountData", JSON.stringify(data.account));
                        } else {
                            if (data.status == "err" && data.msg == "could not find user") {
                                alert(data.msg);
                                localStorage.clear();
                                var port = window.location.port;
                                if (port == "") {
                                    port = "80"
                                }
                                window.location.replace("//" + window.document.domain + ":" + port);
                            }
                        }
                    });
                }
            }
        })
        .catch(function () {
            alert("[ERROR] DVSA backend does not work properly. Try to delete cache and re-login.")
        });
    }

  toggleVisibility = () => this.setState({ visible:  !this.state.visible });

  handleSortByMaxPrice = () => { this.props.startSortByMaxPrice(); }

  handleSortByMinPrice = () => { this.props.startSortByMinPrice(); }

  handleSetMaxPrice = (e) => { this.props.startSetMaxPrice(e.target.value); }

  handleSetMinPrice = (e) => { this.props.startSetMinPrice(e.target.value); }

  handleSetCategory = (e) => { this.props.startSetCategory(e.target.value); }

  handleSetBrand = (e) => { this.props.startSetBrand(e.target.value); }

handleResetFilter = () => {
    document.getElementById("filter-max-input").reset();
    document.getElementById("filter-min-input").reset();
    document.getElementById("filter-category-input").reset();
    document.getElementById("filter-brand-input").reset();
    this.props.startSetMaxPrice('');
    this.props.startSetMinPrice('');
    this.props.startSetCategory('');
    this.props.startSetBrand('');
    isMobile && this.toggleVisibility();
}

  render() {
    const { visible } = this.state;
    return (
      <div className='mt'>
        <div className='store-page'>
            <div className='store-page_filter'>
                <Sidebar
                as={Menu}
                animation='overlay'
                width='thin'
                visible={visible}
                className='filter-sidebar'
                >
            <Menu vertical >
            <Menu.Item header><h4>Filter</h4></Menu.Item>
                <Menu.Item onClick={this.handleSortByMinPrice} className='cursor'>
                    <span>Price Low to High</span>
                </Menu.Item>
                <Menu.Item onClick={this.handleSortByMaxPrice} className='cursor'>
                    <span>Price High to Low</span>
                </Menu.Item>
                <Menu.Item>
                    <Form id='filter-max-input'>
                        <Form.Field width='15'>
                            <Input onChange={this.handleSetMaxPrice} transparent placeholder='Max Price' />
                        </Form.Field>
                    </Form>
                </Menu.Item>
                <Menu.Item>
                    <Form id='filter-min-input'>
                        <Form.Field width='15'>
                            <Input onChange={this.handleSetMinPrice} transparent placeholder='Min Price' />
                        </Form.Field>
                    </Form>
                </Menu.Item>
                {/*}
                <Menu.Item>
                    <Form onChange={this.handleSetCategory} id='filter-category-input'>
                        <Form.Field control='select'>
                            <option value='' >Category</option>
                            {

                                getCategories(this.props.allProducts).map((category, index) => {
                                    return <option key={index} value={category}>{category}</option>
                                })
                            }
                        </Form.Field>
                    </Form>
                </Menu.Item>*/}
                <Menu.Item>
                    <Form onChange={this.handleSetBrand} id='filter-brand-input'>
                        <Form.Field control='select'>
                            <option value=''>Brand</option>
                            {
                                getBrands(this.props.allProducts).map((brand, index) => {
                                    return <option key={index} value={brand}>{brand}</option>
                                })
                            }
                        </Form.Field>
                    </Form>
                </Menu.Item>
                <Menu.Item>
                    <Button basic  fluid onClick={this.handleResetFilter} content='Reset Filter'/>
                </Menu.Item>
                </Menu>
            </Sidebar>

            </div>
            <div className='store-products'>
                <div>
                    <Button
                    className='filter-button'
                    onClick={this.toggleVisibility}
                    floated='right'
                    color='teal'
                    icon='filter'
                    />
                </div>
                <div>
                    <ProductList products={this.props.products} />
                </div>
            </div>
        </div>
          <Footer />
      </div>

    )
  }
}

const mapStateToProps = (state) => {
    return {
      products: selectProducts(state.products, state.filters),
      allProducts: state.products
    };
  };

const mapDispatchToProps = (dispatch) => ({
    startSortByMaxPrice: () => dispatch(sortByMaxPrice()),
    startSortByMinPrice: () => dispatch(sortByMinPrice()),
    startSetMinPrice: (price) => dispatch(setMinPrice(price)),
    startSetMaxPrice: (price) => dispatch(setMaxPrice(price)),
    startSetCategory: (category) => dispatch(setCategory(category)),
    startSetBrand: (brand) => dispatch(setBrand(brand))
});

export default connect(mapStateToProps, mapDispatchToProps)(StorePage);
