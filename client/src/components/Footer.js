import React from 'react';
import {Container, Icon} from 'semantic-ui-react';
import {API} from 'aws-amplify';

const Footer = () => (
    <footer className='footer-bg'>
        <Container>
            <div className='footer-content'>
                <div className='footer-info'>
                <h5>Powered by: <a href="https://www.owasp.org/index.php/OWASP_DVSA"><img align="bottom" width="64px" src="/images/owasplogofooter.svg"/> </a></h5>
                    <div>
                        <div><Icon name='mail'/> tal.melamed@owasp.org </div>
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
