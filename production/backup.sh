#!/bin/bash

cd /home/loconomics
source ./.env
docker exec loconomics_db_1 mysqldump -u suitecrm --password=$MYSQL_PASSWORD suitecrm |
  docker run -i --rm -e RESTIC_REPOSITORY=$RESTIC_REPOSITORY -e RESTIC_PASSWORD=$RESTIC_PASSWORD -e AZURE_ACCOUNT_NAME=$AZURE_ACCOUNT_NAME -e AZURE_ACCOUNT_KEY=$AZURE_ACCOUNT_KEY restic/restic backup --stdin
