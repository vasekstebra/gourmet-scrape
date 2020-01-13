# gourmet-scrape

Script that parses menu from http://ponavka.gourmetrestaurant.cz/ and posts it to Slack using incoming webhook

## Install dependencies 

```
pip3 install -r requirements.txt
```

## Run

Set env variable SLACK_GOURMET_URL and run the script

```
SLACK_GOURMET_URL=<url to Slack incoming webhook > /home/vstebra/devel/gourmet-scrape/gourmet_scrape.py
```
