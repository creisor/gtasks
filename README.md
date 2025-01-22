# gtasks

A commandline tool for managing my tasks.

This is based upon: https://developers.google.com/tasks/quickstart/python

## Credentials

### Google API
Go to https://console.cloud.google.com/apis/credentials?project=gtasks-377215

Under `Credentials` --> `OAuth 2.0 Client IDs` --> `gtasks-oauth-2.0` click the download icon and click `DOWNLOAD JSON` and save it as `credentials.json`.

### Jira API
You can get a Jira API key by visiting [this Atlassian link](https://atlas-trk.prd.msg.ss-inf.net/f/a/mpRE0Zs_G8APsPuZLxKFGg~~/AAAAAQA~/RgRpZuawP0RJaHR0cHM6Ly90cmFjay5hdGxhc3NpYW4uY29tL3RyYWNraW5nL2JmNDk0NDNlLTEwOGItNDliYy05OGE1LTdlOTkwZWYxMWEzNFcLYXRsYXNzaWFudXNCCmd_sGGEZ_APB5dSFmNocmlzLnJlaXNvckBwcm92aS5jb21YBAAAAAA~)

You can pass args or set the following environment variables:
`GTASKS_CHOOSE_JIRA_TOKEN`
`GTASKS_CHOOSE_EMAIL`
`GTASKS_CHOOSE_JIRA_SERVER` (although this is defaulted to the Provi Jira server, so you don't need to do this)

## API Reference

https://developers.google.com/tasks/v1/reference

Python SDK:
https://developers.google.com/resources/api-libraries/documentation/tasks/v1/python/latest/tasks_v1

## Development

```
. ./venv/bin/activate
pip3 install --editable .
```
