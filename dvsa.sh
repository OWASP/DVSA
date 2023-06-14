#!/bin/bash

case $1 in

  package-template)
    python3 scripts/package.py
    ;;


  client-connect)
    python3 scripts/client_connect.py "${@:2}"
    ;;


  client-build)
    npm run-script client:build
    clear
    if grep -rnq "<UserPoolClientId>" client/src/be-stack.json
    then
        echo "[X] Your client file is not connected to your backend."
        echo "If you already deployed the client run: ./dvsa.sh connect"
        exit 0
    else
        DIST_FOLDER=backend/deployment/dist_s3
        echo "[-] Copying new client to $DIST_FOLDER"
        if [ -d "$DIST_FOLDER" ]; then
            rm -rf $DIST_FOLDER
        fi
        cp -r client/dist/* $DIST_FOLDER
        echo "All done! You can now run update-client to update the website."
    fi
    ;;

  
  client-update)
    python3 scripts/client_update.py "${@:2}"
    ;;


   *)
    echo -n "unknown command. options are: package|connect|update. See github.com/owas/dvsa for more information."
    exit 0
    ;;

esac


