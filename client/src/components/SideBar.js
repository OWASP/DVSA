import React, { Component } from 'react';
import { Sidebar, Menu, Icon } from 'semantic-ui-react';
import { Link } from 'react-router-dom';
import onClickOutside from "react-onclickoutside";


export class SideBar extends Component {
    constructor(props){
        super(props);
    }

  state = { visible: false }

  divStyle = {
    margin: '40px 0 0 0'
  }

  toggleVisibility = () => this.setState({ visible: !this.state.visible })

  handleClickOutside = () => {
    if(this.state.visible){
        this.toggleVisibility();
    }
  };

  onClickLessons() {
    url = "https://github.com/OWASP/DVSA/blob/master/AWS/LESSONS/";
    var win = window.open(url, '_blank');
    win.focus();
  }


  render() {
    const { visible } = this.state
    return (
      <div>
        <Icon className='cursor' name='bars' size='big' onClick={this.toggleVisibility}/>
          <Sidebar
              as={Menu}
              animation='overlay'
              width='thin'
              visible={visible}
              icon='labeled'
              className='menu-sidebar'
              vertical
              inverted
            >
              <Link to='/info'>
                <Menu.Item name='info'>
                    <a><img src="/images/iconinfo.png" width="32px"/></a>
                    <br/>Info
                </Menu.Item>
              </Link>

              <Link to='/store'>
                  <Menu.Item name='home'>
                    <Icon name='home' />
                      Store
                  </Menu.Item>
              </Link>

              <Link to='/cart'>
                  <Menu.Item name='store'>
                    <Icon name='shop' />
                    Cart
                  </Menu.Item>
               </Link>

               <Link to='/profile'>
                  <Menu.Item name='profile'>
                    <a><img src="/images/iconprofile.png" width="28px"/></a>
                    <br/>Profile
                  </Menu.Item>
               </Link>

                <Link to='/orders'>
                    <Menu.Item name='orders'>
                    <a><img src="/images/iconorders.png" width="28px"/></a>
                    <br/>Orders
                  </Menu.Item>
                </Link>

                <Link to='/inbox'>
                    <Menu.Item name='inbox'>
                    <a><img src="/images/iconinbox.png" width="28px"/></a>
                    <br/>Inbox
                  </Menu.Item>
                </Link>

                <Link to='/admin'>
                  <Menu.Item name='admin'>
                    <a> <img src="/images/iconadmin.png" width="28px"/></a>
                    <br/>Admin
                  </Menu.Item>
                </Link>

                    <Menu.Item name='lessons'>
                      <a href="https://github.com/OWASP/DVSA/blob/master/AWS/LESSONS/"> <img src="/images/iconlessons.png" width="32px"/></a>
                      <br/>Lessons
                   </Menu.Item>

          </Sidebar>
      </div>
    )
  }
}
export default onClickOutside(SideBar);

