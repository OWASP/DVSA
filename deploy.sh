echo '>>> (1/9) Verifying npm is installed... \c'
if ! [[ "$(npm -v)" =~ .*[0-9][0-9]?[0-9]?[.].* ]]; then
	echo "\n[!] please install npm and run again [!] "
	exit 1
else
	echo "[OK]"
fi

echo '>>> (2/9) Verifying python is installed... \c'
if ! [[ "$(python3 --version)" =~ Python[[:space:]]3[.].* ]]; then
	echo "\n[!] please install python3 and run again."
	exit 1
else
	echo "[OK]"
fi

echo '>>> (3/9) Verifying aws-cli is installed... \c'
if ! [[ "$(aws --version)" =~ aws[-]cli.* ]]; then
	echo "\n[!] Not found. Installing aws-cli..."
	pip3 install awscli --user
else
	echo "[OK]"
fi


echo '>>> (4/9) Verifying python dependencies... \c'
if ! [[ "$(pip3 freeze | grep boto3)" =~ boto3[=][=][1-9][.].* ]]; then
	echo "\nInstalling boto3...\c"
	pip3 install boto3 --user --upgrade
	# if ! [[ "$(pip3 freeze | grep virtualenv)" =~ virtualenv[=][=].* ]]; then
	#	echo "\n[Installing virtualenv...\c"
	#	pip3 install virtualenv --user --upgrade
	# fi
else
	echo "[OK]"
fi


echo '>>> (5/9) Verifying Serverless is installed... \c'
if ! [[ "$(sls --version)" =~ .*Framework.* ]]; then
	echo "\n[!] please install Serverless and run again."
	exit 1
else
	echo "[OK]"
fi

echo '>>> (6/9) Installing dependencies...'
npm i


echo '>>> (7/9) Deploying backend...'
rm -rf /tmp/dvsa.out
sls deploy | tee /tmp/dvsa.out;

if grep -R "Serverless: Stack Output saved to file: ./client/src/be-stack.json" /tmp/dvsa.out; then
	echo '>>> (8/9) Building client ...'
	npm run-script client:build
	echo '>>> (9/9) Deploying client...'
	sls client deploy --no-confirm
fi

