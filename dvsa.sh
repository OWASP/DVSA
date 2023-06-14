#!/bin/bash

PYHTON_VER=$(python -c 'import sys; print(sys.version_info.major)')
if [ $PYHTON_VER -ne 3 ]; then
    PY_CMD=python3
else
    PY_CMD=python
fi


case $1 in

  package-template)
    echo "[-] Will execute SAM with default commands. To modify, update file: scripts/package_template.py"
    $PY_CMD scripts/package_template.py "${@:2}"
    ;;


  client-connect)
    $PY_CMD scripts/client_connect.py "${@:2}"
    ;;


  client-build)
    BE_STACK=client/src/be-stack.json
    if [ ! -f "$BE_STACK" ]; then
        echo "[X] Could not identify $BE_STACK."
        echo "If you already deployed a backend, please first run: $ ./dvsa.sh client-connect"
        exit 0
    fi
    npm run-script client:build
    clear
    if grep -rnq "<UserPoolClientId>" $BE_STACK
    then
        echo "[X] Your client file is not connected to your backend."
        echo "If you already deployed the client run: $ ./dvsa.sh client-connect"
        exit 0
    else
        DIST_FOLDER=backend/deployment/dist_s3
        echo "[-] Copying new client to $DIST_FOLDER"
        if [ -d "$DIST_FOLDER" ]; then
            rm -rf $DIST_FOLDER
        fi
        mkdir $DIST_FOLDER
        cp -r client/dist/* $DIST_FOLDER
        echo "All done! You can now run update-client to update the website."
    fi
    ;;

  
  client-update)
    $PY_CMD scripts/client_update.py "${@:2}"
    ;;


   *)
    echo "[X] Unknown command."
    echo "Options are: package|connect|update. See github.com/owas/dvsa for more information."
    exit 0
    ;;

esac


