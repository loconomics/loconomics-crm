# Loconomics CRM Environment

This configuration launches [SuiteCRM](https://suitecrm.com) for testing and development purposes. It also contains organization-specific scripts for scraping data from Yelp, Bing, and Instagram. Our [production configuration](./production) is slightly different, running fewer services and including configuration for automatic hourly database backups.

## Setup

Start by creating a file called _.env_ in the current directory. This file sets up several environment variables. You'll need to fill in the area after the `=` with data relevant to your specific credentials:

```
MYSQL_PASSWORD=suitecrm
SUITECRM_DATABASE_PASSWORD=
BING_SUBSCRIPTION_KEY=
YELP_CONSUMER_KEY=
YELP_CONSUMER_SECRET=
YELP_TOKEN=
YELP_TOKEN_SECRET=
```

Then:

1. [Install Docker CE for your platform](https://docs.docker.com/install/).
2. [Install Docker Compose for your platform](https://docs.docker.com/compose/install/).
3. From this directory, run `docker-compose up`.

## Components

### SuiteCRM

SuiteCRM is now running on ports 80 and 443. The default credentials are as follows:

Username: admin
Password: bitnami

Enter this container by running:

```bash
$ docker-compose exec crm bash
```

### Importer

This container hosts a Python environment which runs our various importer scripts. To enter it and run the importers, run:

```bash
$ docker-compose exec importer bash
```

### Database

This container holds MySQL and its associated utilities. To enter and more easily access the database, run:

```bash
$ docker-compose exec db bash
```

The root password is random, and can be viewed in the container's logs by running:

```bash
$ docker-compose logs db
```
