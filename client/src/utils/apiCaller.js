import {API} from 'aws-amplify';
const backendStackOutputs = require('../be-stack.json');
// export function callApi(opts) {
//     return (API.post("ApiGateway", "/order", {body: opts}))
//         // .then(res => {
//         //     console.log("RES:", res)
//         // })
//         // .catch(err => {
//         //     console.log("ERR:", err)
//         // })
// }

export function callApi(opts) {
    var authorization = "";
    for(var key in localStorage){
        if ( key.startsWith("CognitoIdentityServiceProvider.") && key.endsWith(".accessToken") ) {
            authorization = localStorage.getItem(key);
        }
    }

    return(
        fetch(backendStackOutputs.ServiceEndpoint + '/order', {
            crossDomain:true,
            method: 'post',
            headers: new Headers({
                'Content-Type': 'application/json',
                'Authorization': authorization
            }),
            body: JSON.stringify(opts)
        })
    )
}