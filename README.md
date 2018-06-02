Tool to automate the reservation of [DMM英会話](http://eikaiwa.dmm.com/)

## Usage

Set up `config.yaml`
```
id: <dmm id>
pass: <password>
time: 08:30                       # the time to start the lesson
lessonStyle: Free Conversation    # if omitted, defaults to Original Materials
```

- `./reserve.py` reserves a lesson at the specified time of the nearest day
- `./setup.sh` sets up cronjob to reserve a lesson every day
