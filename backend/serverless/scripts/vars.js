const execSync = require('child_process').execSync;
const output = execSync('aws sts get-caller-identity', { encoding: 'utf-8' });  // the default is 'buffer'
const awsInfo = JSON.parse(output);

exports.accountId = function() {
    return awsInfo.Account;
};
