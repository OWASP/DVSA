const serialize = require('node-serialize');
const { LambdaClient, InvokeCommand } = require("@aws-sdk/client-lambda");
const { CognitoIdentityProviderClient, AdminGetUserCommand } = require("@aws-sdk/client-cognito-identity-provider");
const jose = require('node-jose');



exports.handler = (event, context, callback) => {
    // console.log(JSON.stringify(event));
    var req = serialize.unserialize(event.body); 
    var headers = serialize.unserialize(event.headers);
    var auth_header = headers.Authorization || headers.authorization;
    var token_sections = auth_header.split('.');
    var auth_data = jose.util.base64url.decode(token_sections[1]);
    var token = JSON.parse(auth_data);
    var user = token.username;
    var isAdmin = false;
    
    var params = {
      UserPoolId: process.env.userpoolid,
      Username: user
    };
    
    try {
        const cognitoidentityserviceprovider = new CognitoIdentityProviderClient();
        const command = new AdminGetUserCommand(params);
        const userData = cognitoidentityserviceprovider.send(command);
        
        userData.then((userData)=>{
            // console.log("userData", JSON.stringify(userData));
            var len = Object.keys(userData.UserAttributes).length;
            for (var i=0; i< len; i++) {
                if (userData.UserAttributes[i].Name === "custom:is_admin") {
                    isAdmin = userData.UserAttributes[i].Value;
                    break;
                }
            }
            var action = req.action;
            var isOk = true;
            var payload = {};
            var functionName = "";
            
            switch(action) {
                case "new":
                    payload = { "user": user, "cartId": req["cart-id"], "items": req["items"] };
                    functionName = "DVSA-ORDER-NEW";
                    break;

                case "update":
                    payload = { "user": user, "orderId": req["order-id"], "items": req["items"] };
                    functionName = "DVSA-ORDER-UPDATE";
                    break;

                case "cancel":
                    payload = { "user": user, "orderId": req["order-id"] };
                    functionName = "DVSA-ORDER-CANCEL";
                    break;

                case "get":
                    payload = { "user": user, "orderId": req["order-id"], "isAdmin": isAdmin };
                    functionName = "DVSA-ORDER-GET";
                    break;

                case "orders":
                    payload = { "user": user };
                    functionName = "DVSA-ORDER-ORDERS";
                    break;

                case "account":
                    payload = { "user": user };
                    functionName = "DVSA-USER-ACCOUNT";
                    break;

                case "profile":
                    payload = { "user": user, "profile": req["data"]  };
                    functionName = "DVSA-USER-PROFILE";
                    break;

                case "shipping":
                    payload = { "user": user, "orderId": req["order-id"], "shipping": req["data"] };
                    functionName = "DVSA-ORDER-SHIPPING";
                    break;

                case "billing":
                    payload = { "user": user, "orderId": req["order-id"], "billing": req["data"] };
                    functionName = "DVSA-ORDER-BILLING";
                    break;
                
                case "complete":
                    payload = { "orderId": req["order-id"] };
                    functionName = "DVSA-ORDER-COMPLETE";
                    break;

                case "inbox":
                    payload = { "action": "inbox", "user": user };
                    functionName = "DVSA-USER-INBOX";
                    break;

                case "message":
                    payload = { "action": "get", "user": user, "msgId": req["msg-id"], "type": req["type"] };
                    functionName = "DVSA-USER-INBOX";
                    break;

                case "delete":
                    payload = { "action": "delete", "user": user, "msgId": req["msg-id"] };
                    functionName = "DVSA-USER-INBOX";
                    break;

                case "upload":
                    payload = { "user": user, "file": req["attachment"] };
                    functionName = "DVSA-FEEDBACK-UPLOADS";
                    break;

                case "feedback":
                    const response = {
                            statusCode: 200,
                            headers: {
                                "Access-Control-Allow-Origin" : "*"
                            },
                            body: JSON.stringify({"status": "ok", "message": `Thank you ${req["data"]["name"]}.`})
                    };
                    callback(null, response);

                case "admin-orders":
                    if (isAdmin == "true") {
                        payload = { "user": user, "data": req["data"] };
                        functionName = "DVSA-ADMIN-GET-ORDERS";
                        break;
                    }
                    else {
                        const response = {
                            statusCode: 403,
                            headers: {
                                "Access-Control-Allow-Origin" : "*"
                            },
                            body: JSON.stringify({"status": "err", "message": "Unauthorized"})
                        };
                       callback(null, response);

                    }

                default:
                    isOk = false;
            }

            if (isOk == true) {

                var params = {
                    FunctionName: functionName,
                    InvocationType: 'RequestResponse',
                    Payload: JSON.stringify(payload)
                };
                const lambda_client = new LambdaClient();
                const command = new InvokeCommand(params);
                lambda_client.send(command).then((lambda_response) => {
                    const data = JSON.parse(Buffer.from(lambda_response.Payload).toString());
                    const response = {
                        statusCode: 200,
                        headers: {
                            "Access-Control-Allow-Origin" : "*"
                        },
                        body: JSON.stringify(data)
                    };
                    callback(null, response);
                });
            }
            
            else {
                var data = {"status": "err", "msg": "unknown action"};
                const response = {
                    statusCode: 200,
                    headers: {
                        "Access-Control-Allow-Origin" : "*"
                    },
                    body: JSON.stringify(data),
                };
                callback(null, response);
                
            }

        });
    }
    catch (e){
        console.log(e);
    }
};
