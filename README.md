Tool to automate reservation of [DMM英会話](http://eikaiwa.dmm.com/)

## Usage

Set up `config.yaml`
```
id: <dmm id>
pass: <password>
time: 06:00
```

- `./reserve.py` reserves a lesson at the specified time of the next day
- `./setup.sh` sets up cronjob to reserve a lesson every day
