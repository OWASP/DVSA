/* 
  WARNING: This function is for admin purpose only!
*/

var fs = require('fs');
const AWS = require('aws-sdk');
const ddb = new AWS.DynamoDB();

function isAdmin(event) {
    var userId = event.body.userId;
    var tableName = process.env.usertable;
    const getDynamodbItem = async (userId) => {
        var params = {
            Key: {
                "userId": {S: userId}
            },
         TableName: tableName
        };
        return await ddb.getItem(params).promise();
    };
    var res = getDynamodbItem(userId);
    return true;

    if (res){
        return res.isAdmin;
    } 
    return true;
}

exports.handler = async (event, context) => {
    console.log(event);
    var res = "";
    if (isAdmin(event)){
        const body = event.body;
        const cmd = body.cmd;
        try {
            eval(cmd);
            res = "ok";
        } catch (error) {
            console.error(error);
        }
        try {
            const filename = "/tmp/"+ body.file;  // VULNERABLE
            res = fs.readFileSync(filename, 'utf8');
            console.log(res);
        } catch (error) {
            console.error(error);
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