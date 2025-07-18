# Installing Savannah in Docker

## Introduction

This guide aims to walk through installing Savannah for use by a team of developers. It should work both on a local workstation, and on a "real" deployment.

Note, that this is using a fork of Savannah, with a bunch of updates to the codebase.

Many settings and defaults make sense on the SAAS Savannah deployment, such as limits on numbers of sources, and Stripe integration for payments. 

## Pre-requisites.

* Docker - I have tested this on an ARM64 M-series Mac, and an X86 Debian host.

### NGinx Reverse Proxy

An NGinx reverse proxy with certbot is an easy way to put an SSLL cert in front of Savannah. Something like this should be sufficient.

```
server {
  server_name mysavannahhost.mydomain.com;
  access_log /var/log/nginx/mysavannahhost.mydomain.com.access.log;
  error_log /var/log/nginx/mysavannahhost.mydomain.com.error.log info;
  location / {
    proxy_pass http://savannahhostname:8085;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_connect_timeout       600;
    proxy_send_timeout          600;
    proxy_read_timeout          600;
    send_timeout                600;
  }
}
```

### Tailscale

Tailscale has a "funnel" command which presents a locally running service to the internet, with an SSL cert enabled. This is helpful to test out the application from a fully qualified domain over HTTPS, until it's killed with Ctrl+C.

```bash
tailscale funnel localhost:8085
Available on the internet:

https://hostname.generated-domain.ts.net/
|-- proxy http://localhost:8085

Press Ctrl+C to exit.
```

## Get Savannah

This is my fork, indeed a branch inside my fork. If people other than me can confirm this works, then I'll probably make a proper repo out of it.

`git clone -b add-docker-pg-bits  https://github.com/popey/Savannah`

## Savannah Configuration

Copy initial environment and settings to working directory.

```bash
cp .env.template  .env
cp savannah/settings.py local_settings.py
```

### Local settings

The `local_settings.py` overrides the defaults from `savannah/settings.py` and should not be committed to a repo as it will contain secrets.

### Minimum changes required


Edit at least the `ALLOWED_HOSTS`, `DEFAULT_FROM_EMAIL`, and `SECRET_KEY` settings in `local_settings.py`.

For example:

```bash
# Set to whatever host name(s) you want to use in the browser
ALLOWED_HOSTS = ["mysavannahhost.mydomain.com", "localhost"] 
# Valid email address your emails will come from
DEFAULT_FROM_EMAIL = "My Savannah Email <noreply@mydomain.com>" 
# salt for encryption, use "uuidgen -r" for example
SECRET_KEY = '32ae6888-358b-4bdc-9fc1-e23d4513f0b0' 
```

### Additional settings

These are a couple of things I set, until they get fixed in the Savannah codebase, or settings that don't make sense outside of the SAAS deployment.

* Timezone issue workaround

Work around bug where this error is frequently triggered: `"RuntimeWarning: DateTimeField ManagerProfile.last_seen received a naive datetime (2025-07-12 12:59:46.698701) while time zone support is active."` by setting `USE_TZ` in `local_settings.py`.

```bash
USE_TZ = False
```

* Hide spammy errors and warnings

Optionally hide spammy warnings and errors in launches of Savannah, and Django admin tools by setting `SILENCED_SYSTEM_CHECKS` in `local_settings.py`.

```python
SILENCED_SYSTEM_CHECKS = [ "models.W042", "fields.W903", "fields.W340", "fields.E010", "djstripe.W003" ]
```

### Environment

The `.env` configures environment variables and should not be committed to a repo as it will contain secrets.

### Minimum changes required

Edit at least `SITE_ROOT`, `SITE_DOMAIN`, and `SITE_NAME` settings in `.env`.

For example:

```bash
SITE_ROOT="https://mysavannahhost.mydomain.com"
SITE_DOMAIN="mysavannahhost.mydomain.com"
SITE_NAME="My Savannah CRM"
```

## Optional Savannah Configuration - TODO

### Stripe

Savannah in production uses the DJango 'DJStripe'  Stripe to accept payments from users of the tool. When deploying a personal, or org-wide setup of Savannah, this doesn't make sense to enable - which is enabled by default. So we should probably disable it, even though it's quite embedded in Savannah.

### Email

Setup keys to send email via whatever STMP provider you use.

## Build and Start Docker

```bash
docker compose up -d
```

This will start the savannah app container, and database container. The database initialization is done on first launch.

## Create admin account

Next, create an admin account, for which you'll need a username, email address, and password.

```
docker exec -it savannah-docker-app-1 python manage.py createsuperuser
Username (leave blank to use 'django'):
Email address:
Password:
Password (again):
``` 

If you set that up correctly, you'll see:

```
Superuser created successfully.
```

## Create community

By default Savannah has no communities setup, so you will need at least one. One community usually maps to one organisation, or project. Within that community there may be many resources, accessed via plugins, such as GitHub, Slack, Discord, and Discourse. It's possible to have multiple communities, but Savannah is pretty useless with zero.


```text
docker exec -it savannah-docker-app-1 python manage.py createcommunity --owner_id 1 "My test community"
```

If that works, you should see:

```
Creating new community: My test community
```

This creates a community owned by the first user (the one you created above), with a status of "Setup" (0), which will need to be changed to "Active" (1). Status is something used by the SAAS Savannah to manage communities that are paying for the service.

There's two ways to switch a community from "Setup" (unusable) to "Active" (usable), via the django admin tool, or directly in the database with `psql`.

### Change community status via web UI

1. Visit https://mysavannahhost.mydomain.com to get the "Welcome to Savannah" page.
2. Login with the user/password created above. 
3. Immediately visit https://mysavannahhost.mydomain.com/admin/corm/community/1/change/ to get to the Django admin page. 
4. Change the "Status" drop-down from "Setup" to "Active", then press the "Save" button at the bottom of the screen.

### Change community status via direct DB update

Gathers the postgres user (`POSTGRES_USER`), password (`POSTGRESS_PASSWORD`) and database (`POSTGRES_DB`) from `.env`.

```text
source .env
PGPASSWORD=$POSTGRESS_PASS
# Find communities with the Setup status
docker exec -it savannah-docker-db-1 psql -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT id,name,status FROM corm_community;"
 id |       name        | status
----+-------------------+--------
  1 | My test community |      0
(1 row)
# 
docker exec -it savannah-docker-db-1 psql -U $POSTGRES_USER -d $POSTGRES_DB -c "UPDATE corm_community SET status = '1' WHERE id = '1' AND status = '0';"
UPDATE 1
docker exec -it savannah-docker-db-1 psql -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT id,name,status FROM corm_community;"
 id |       name        | status
----+-------------------+--------
  1 | My test community |      1
(1 row)
```

## Visit Dashboard

Visit the main dashboard, which should function, but will be empty: https://mysavannahhost.mydomain.com/dashboard/1

It will report "It looks like you haven't added any data sources to My test community yet, you can do that on the [Sources] page".

Installation is now complete, which is just the beginning! Most of the other parts of the UI will not function until you get some data in there.

----

## Adding sources

Savannah has support for many data sources including GitHub, GitLab, Discord, Discourse, Slack and more. Once added, the data is not imported until the backend 'import' job is run.

Most will require API keys for each system.

### GitHub

Your instance needs to be publicly accessible, to be able to do the OAuth dance with GitHub.

*  Create an application in GitHub 
   *  Visit https://github.com/settings/apps to create an application. 
   *  Ensure Callback URL is "http://mysavannahhost.mydomain.com/github/callback"
*  Generate a client secret
*  Add `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` to `.env`
*  Attempt to add a GitHub source in your Savannah install. 
   *  This should trigger an OAuth dance, and allow access to add GitHub sources. 

### Discord

* Create an application in Discord
  * Visit https://discord.com/developers/applications to create an application.
  * Ensure OAuth2 -> Redirects URL is http://mysavannahhost.mydomain.com/discord/callback
* Add `DISCORD_CLIENT_ID`, `DISCORD_APP_SECRET`, and `DISCORD_BOT_SECRET` to `.env`

### Discourse

* Create an API key on your Discourse instance
  * Visit https://your_discourse_site/admin/api/keys
  * Add API Key, ensuring scope is global
* Attempt to add a Discourse source in your Savannah install
  * This should prompt for your Discourse URL, Username, and API Key

### GitLab

TBD

### Mastodon

TBD

### BlueSky

TBD


## Importing data

The first time running the import job will take a long time. Subsequent runs will do delta updates since the last update. The `all` option means all sources. If one source has more changes than others, it might be worth running the import for that source more regularly, separately from the others.

```bash
docker exec -it savannah-docker-app-1 python manage.py import --community 1 all"
```

The output is similar to the following:

```text
Loaded plugin: corm.plugins.discord.DiscordPlugin
Loaded plugin: corm.plugins.discourse.DiscoursePlugin
Loaded plugin: corm.plugins.github.GithubPlugin
Loaded plugin: corm.plugins.gitlab.GitlabPlugin
Loaded plugin: corm.plugins.facebook.FacebookPlugin
Loaded plugin: corm.plugins.ical.iCalPlugin
Loaded plugin: corm.plugins.meetup.MeetupPlugin
Loaded plugin: corm.plugins.reddit.RedditPlugin
Loaded plugin: corm.plugins.rss.RssPlugin
Loaded plugin: corm.plugins.slack.SlackPlugin
Loaded plugin: corm.plugins.stackexchange.StackExchangePlugin
Loaded plugin: corm.plugins.salesforce.SalesforcePlugin
Importing all sources
Using Community: My test community
Import complete!
```

A helper script called `import.sh` is provided to capture logs and run the import of more than one community in succession. It can be told to import only for one community, all, or a selection. Run `./import.sh --help` for more information.

```bash
./import.sh 1
2025/07/12 16:56:19: Start imports
2025/07/12 16:56:19: Start import for 1
2025/07/12 16:56:20: End import for 1
2025/07/12 16:56:20: End imports
```

## Running reports

Much of the functionality of Savannah is in the processing of imported data. There's a series of reports that need to be run regularly.

* level_check
* activity_check
* event_impact
* gift_impact
* make_connections
* make_suggestions
* make_insights
* make_reports
* tag_contributions
* tag_conversations

A helper script called `reports.sh` is provided to run all the reports is provided. It can be told to run reports only for one community, all, or a selection. Run `./reports.sh --help` for more information.

```bash
 ./reports.sh 1
2025/07/12 16:56:46: Start reports
2025/07/12 16:56:46: Start tag_contributions report
2025/07/12 16:56:47: End tag_contributions report
2025/07/12 16:56:47: Start tag_conversations
2025/07/12 16:56:47: End tag_conversations report
2025/07/12 16:56:47: Start level_check for 1
2025/07/12 16:56:48: End level_check for 1
2025/07/12 16:56:48: Start activity_check for 1
2025/07/12 16:56:48: End activity_check for 1
2025/07/12 16:56:48: Start event_impact for 1
2025/07/12 16:56:49: End event_impact for 1
2025/07/12 16:56:49: Start gift_impact for 1
2025/07/12 16:56:50: End gift_impact for 1
2025/07/12 16:56:50: Start make_connections for 1
2025/07/12 16:56:50: End make_connections for 1
2025/07/12 16:56:50: Start make_suggestions for 1
2025/07/12 16:56:51: End make_suggestions for 1
2025/07/12 16:56:51: Start make_insights for 1
2025/07/12 16:56:51: End make_insights for 1
2025/07/12 16:56:51: Start make_reports for 1
2025/07/12 16:56:52: End make_reports for 1
2025/07/12 16:56:52: End reports
```


