//const Alexa = require('ask-sdk-core');
const mysql = require('mysql');
const util = require('util');


/* 
* this Lambda function is not currently at use and is only here for backup.
*/


function getOrder(user_id, order_id) {
    
    console.log("trying: " + user_id + " and " + order_id);

  var connection = mysql.createConnection({
    host      : process.env.db_url,
    user      : process.env.db_user,
    password  : process.env.db_pw,
    database  : process.env.db_name,
  });

  connection.connect();
  
    return new Promise(function (resolve, reject) {
        connection.query("SELECT * from orders where orderId = '" + order_id + "' and userId = '" + user_id + "'", function (error, results, fields) {
          if (error) {
              connection.end();
              console.log(error);
              reject("wrong credentials");
          }
          else {
            connection.end();
            resolve(results);
          }
        });
  });
}


// ToDo
function parseDB2JSON(result) {
    return result;
}


exports.handler = async (event) => {
    let parsed_result;
    let qsp = event.queryStringParameters;
    try {
        var user_id = qsp.userId;
        var order_id = qsp.orderId;
        var result = await getOrder(user_id, order_id);
        console.log("order: " + result);

        parsed_result = parseDB2JSON(result);
    }
    catch (e){
        console.log(e);
    }
  
    const response = {
        statusCode: 200,
        body: JSON.stringify(parsed_result)
    };
    return response;
};
