# Production Setup

This production SuiteCRM setup offers the following benefits:

 * Easily reproduceable. Run a standard set of commands to bring up the server.
 * Easy upgrades via Bitnami's procedure [documented here](https://github.com/bitnami/bitnami-docker-suitecrm/#upgrade-this-application).
 * Hourly deduplicated MySQL backups to Azure Storage.

Unfortunately, Azure's hosted MySQL offering timed out with both Bitnami's standard installation, and with a vanilla SuiteCRM installation. It may be worth periodically checking on whether that remains the case, as using a hosted database is certainly preferable to maintaining our own backup infrastructure.

## Setup

### Launch SuiteCRM

1. Provision a VM on your provider of choice.
2. Copy all the files in this directory to the remote server.
3. On the remote server, create a file called _.env_ with the following content, substituting appropriate values for `SOMETHING`:

```
MYSQL_PASSWORD=SOMETHING
SUITECRM_DATABASE_PASSWORD=SOMETHING
SUITECRM_PASSWORD=SOMETHING
SUITECRM_EMAIL=SOMETHING
SUITECRM_HOST=SOMETHING
ACME_EMAIL_ADDRESS=SOMETHING
RESTIC_PASSWORD=SOMETHING
AZURE_ACCOUNT_NAME=SOMETHING
AZURE_ACCOUNT_KEY=SOMETHING
RESTIC_REPOSITORY=SOMETHING
```

4. Install Docker and Docker-compose.
5. Run `docker-compose up -d` to launch the stack.

### Set up Backups

This setup uses [Restic](https://restic.net) for backing up MySQL database dumps.

Edit _backup.sh_, if necessary, to set correct container names and such. Once complete, run the following commands to set up hourly database backups:

```bash
$ docker pull restic/restic
$ docker run -i --rm -e RESTIC_REPOSITORY=$RESTIC_REPOSITORY -e RESTIC_PASSWORD=$RESTIC_PASSWORD -e AZURE_ACCOUNT_NAME=$AZURE_ACCOUNT_NAME -e AZURE_ACCOUNT_KEY=$AZURE_ACCOUNT_KEY restic/restic init
$ cp backup.service backup.timer /etc/systemd/system
$ systemctl enable backup.service
$ systemctl start backup.service
```

#### Listing Snapshots

```bash
$ source .env
$ docker run -i --rm -e RESTIC_REPOSITORY=$RESTIC_REPOSITORY -e RESTIC_PASSWORD=$RESTIC_PASSWORD -e AZURE_ACCOUNT_NAME=$AZURE_ACCOUNT_NAME -e AZURE_ACCOUNT_KEY=$AZURE_ACCOUNT_KEY restic/restic snapshots
```

#### Accessing/restoring Backups

Backup snapshots are raw database dumps. After identifying a snapshot to access, dump the database to stdout by running the following:

```bash
$ docker run -i --rm -e RESTIC_REPOSITORY=$RESTIC_REPOSITORY -e RESTIC_PASSWORD=$RESTIC_PASSWORD -e AZURE_ACCOUNT_NAME=$AZURE_ACCOUNT_NAME -e AZURE_ACCOUNT_KEY=$AZURE_ACCOUNT_KEY restic/restic dump <snapshot ID> stdin
```

This dump can then be reloaded into the _db_ container.

See [this documentation](https://restic.readthedocs.io/en/latest/050_restore.html) for more details on restoring backups.
