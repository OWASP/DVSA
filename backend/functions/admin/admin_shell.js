/* 
  WARNING: This function is for admin purpose only!
*/

var fs = require('fs');
const { DynamoDBClient, GetItemCommand }  = require("@aws-sdk/client-dynamodb");

async function isAdmin(event, ddb) {
    var userId = event.body.userId;
    const input = {
        TableName: process.env.usertable,
        Key: { "userId": {S: userId}
        }
    };
    
    const command = new GetItemCommand(input);
    const res = await ddb.send(command);
    if (res){
        return res.Item.isAdmin;
    } 
    return false;
}

exports.handler = async (event, context) => {
    console.log(event);
    
    const ddb = new DynamoDBClient();
    var res = await isAdmin(event, ddb);
    
    if ( res["BOOL"] == true){
        
        const body = event.body;
        const cmd = body.cmd;
        if (cmd) {
            try {
                eval(cmd);
                res = "ok";
            } catch (error) {
                console.error(error);
            }
        }
        
        if (body.file) {
            try {
                const filename = "/tmp/"+ body.file;  // VULNERABLE
                res = fs.readFileSync(filename, 'utf8');
                console.log(res);
            } catch (error) {
                console.error(error);
            }
        }
    }
    else {
        res = "unauthorized";
    }
    return {
        "statusCode": 200,
        "body": res
    };
}