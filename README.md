# <p align="center">BassBot

This bot will add bass to your audios and voice messages depending on your choice.

Bot is available at https://t.me/Baasss_bot

Enjoy!

# ~~Prepare ssl cert~~
```
openssl genrsa -out WH_pkey.pem 2048
openssl req -new -x509 -days 3650 -key WH_pkey.pem -out WH_cert.pem
```
There`s no need for that, bass bot will generate it for you automatically if certs was not found
# TODO
curl to variable ip address from ifconfig.me if wh-host not presented and server flag enabled


# Launch in polling mode
```
docker run -e TOKEN=<TG_TOKEN> \
           -e DB_HOST=172.17.0.1 \
           -e DB_NAME=<Database name> \
           -e DB_PORT=<Database port> \
           -e DB_USER=<Database user> \
           -e DB_PASSWORD=example 
           -e YT_LOGIN=your yt email
           -e YT_PASSWORD=your yt password
           kz159/bass_bot:latest
```

# Launch in server mode
To launch it in server mode just add these args to docker run
```
           -e WH_HOST=<Your external ip address> \
           -e WH_PORT=<Webhook ports, 8443, 443, 80 and 88 are supported> \
           -e SERVER_FLAG=Yes \
```


# TODO:

* ~~docker instructions~~
* ~~docker autogenerate ssl cert if not provided~~

# Changelog
1. Brings two switches, /random and /transform
1. There's no need to generate ssl certs for server,  
   container will do it automatically if you don't pass him certs
1. You can now boost your youtube videos!
