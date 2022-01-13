# reddit_monitor

## Docker 
### Build

```shell
sh build.sh
```

### Run
Create a .env_list file
```shell
CLIENT_ID=...
CLIENT_SECRET=...
USER_AGENT=...
SUBREDDIT_NAME=...
RATELIMIT_SECONDS=30
ALERTZY_KEY=...
```

Execute
```shell
docker run  --env-file .env_list maxjacu/reddit_monitor
```


## Python
Create a .env file
```shell
export CLIENT_ID=...
export CLIENT_SECRET=...
export USER_AGENT=...
export SUBREDDIT_NAME=...
export RATELIMIT_SECONDS=30
export ALERTZY_KEY=...
```

Execute
```shell
python src/main.py 
```