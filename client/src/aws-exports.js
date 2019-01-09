const backendStackOutputs = require('./be-stack.json');
import Amplify, {Auth} from 'aws-amplify';
import regeneratorRuntime from "regenerator-runtime";

const AwsConfig = {
    Auth: {
        identityPoolId: backendStackOutputs.IdentityPoolId,
        region: backendStackOutputs.IdentityPoolId.split(':')[0],
        userPoolId: backendStackOutputs.UserPoolId,
        userPoolWebClientId: backendStackOutputs.UserPoolClientId,
    },
    API: {
        endpoints: [
            {
                name: "ApiGateway",
                endpoint: backendStackOutputs.ServiceEndpoint,
                custom_header: async () => {
                    return { Authorization: (await Auth.currentSession()).idToken.jwtToken }
                }
                // return { Authorization: (await Auth.currentSession()).idToken.jwtToken }

                // custom_header: () => Auth.currentSession().then(res => res.idToken.jwtToken)
                // .then()async () => {
                // return {
                //     Authorization: (await Auth.currentSession()).idToken.jwtToken
                // }
                // }
            }
        ]
    }
};

const configure = () => Amplify.configure(AwsConfig);

export default {
    configure
}
