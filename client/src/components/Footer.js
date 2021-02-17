import React from 'react';
import {Container, Icon} from 'semantic-ui-react';
import {API} from 'aws-amplify';

const Footer = () => (
    <footer className='footer-bg'>
        <Container>
            <div className='footer-content'>
                <div className='footer-info'>
                <h5>Created by: <a href="https://github.com/4ppsec/">Tal Melamed (4ppsec) </a></h5>
                <h5>Powered by: <a href="https://owasp.org/www-project-dvsa/"><img align="bottom" width="64px" src="https://owasp.org/assets/images/logo.png"/> </a></h5>
                    <div>
                        <div><Icon name='mail'/> hi@dvsa.cloud </div>
                    </div>
                </div>
                <div className='footer-social'>
                    <a href="https://github.com/OWASP/DVSA/"><Icon name='github' size='big'/> </a>
                    <a href=""><Icon name='owasp' size='big'/></a>
                    <a href="https://twitter.com/DVSAowasp"><Icon name='twitter' size='big'/></a>
                </div>
            </div>
        </Container>
    </footer>
);

export default Footer;
