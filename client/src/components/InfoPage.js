import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import { Button, Segment, Container, Label, Grid, Image, Header, Icon, IconGroup } from 'semantic-ui-react';
import * as API from '../utils/apiCaller';
import {Redirect} from 'react-router-dom';

export class InfoPage extends React.Component {
    render(){
        return(
            <Container className='page-top-margin'>
                <a href="https://www.owasp.org/index.php/OWASP_DVSA">
                <img src="/images/owasplogoinfo.png"/>
                </a>
                <br/><br/>
                <h2>Information</h2>
                <p>
                    Damn Vulnerable Serverless Application (DVSA) is a deliberately vulnerable application aiming to be an aid for security professionals to test their skills and tools in a legal environment, help developers better understand the processes of securing serverless applications and to aid both students & teachers to learn about serverless application security in a controlled class room environment.
                    The aim of DVSA is to practice some of the most common serverless vulnerabilities, with a simple straightforward interface.
                    Please note, there are both documented and undocumented vulnerabilities with this software. This is intentional. You are encouraged to try and discover as many issues as possible.
                </p>
                <div>
                <h3>Disclaimer</h3>
                <b>* DO NOT INSTALL DVSA ON A PRODUCTION ACCOUNT *</b> <br/>
                We do not take responsibility for the way in which any one uses this application (DVSA). We have made the purposes of the application clear and it should not be used maliciously. We have given warnings and taken measures to prevent users from installing DVSA on to production accounts.
                <h3>Documentation</h3>
                Solutions can be found in the project <a href="https://github.com/OWASP/DVSA/blob/master/AWS/LESSONS/README.md">github page</a>
                <h3>Links</h3>
                <a href="https://github.com/OWASP/Serverless-Top-10-Project/blob/master/README.md">OWASP Top 10 - Serverless Interpretation</a><br/>
                <a href="https://www.protego.io/category/a-deep-dive-into-serverless-attacks/">Deep-Dive into Serverless Attacks - Series</a><br/>
                <a href="https://www.owasp.org/index.php/OWASP_Serverless_Top_10_Project">OWASP Serverless Top 10 Project</a><br/>
                <a href="https://twitter.com/DVSAowasp">Twitter Account (Hackable)</a><br/>
                <a href="https://owasp.slack.com/join/shared_invite/enQtNDI5MzgxMDQ2MTAwLTEyNzIzYWQ2NDZiMGIwNmJhYzYxZDJiNTM0ZmZiZmJlY2EwZmMwYjAyNmJjNzQxNzMyMWY4OTk3ZTQ0MzFhMDY">Slack Channel #project-sls-top-10</a>
                <h3> License</h3>
                Damn Vulnerable Serverless Application (DVSA) is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Damn Vulnerable Serverless Application (DVSA) is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Damn Vulnerable Serverless Application (DVSA). If not, see http://www.gnu.org/licenses/.
                <h3>Source Code</h3>
                Source code is published on <a href="https://github.com/owasp/dvsa/">GitHub</a><br/><br/>
                <h3>Acknowledgements</h3>
                DVSA was created by <a href="https://twitter.com/4ppsec">Tal Melamed</a>
                 <br/><br/> <br/>
                </div>
            </Container>

        );
    }
}

const mapStateToProps = (state) => ({
    cart: state.shoppingCart,
});

export default connect(mapStateToProps)(InfoPage);