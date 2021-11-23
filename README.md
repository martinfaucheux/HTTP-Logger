# HTTP Monitor

This is a simple monitoring tool which read csv http log files and output messages
* periodically display statistics about requests in the last period (most hit section)
* display a message when the throuput has reached a certain rate during a specified window
* display a message when the previous alert is recovered (throuput went back to normal)

# Getting started

You only require
* python >= 3.6
* pip

To install the library
* Clone the repository
* Go the the root of the project
* Install the package with `pip install ./`
* You can now use http_monitor running `http_monitor <command>`

For development, you can alternatively use pipenv
* `pipenv install --dev; pipenv shell`
* You can now use http_monitor running `python http_monitor/main.py <command>`

# Usage
To read directly from a file, just pass it as an argument of the command
```
http_monitor sample_csv.txt
```
Alternatively, you can read directly you can pipe the logs
```
cat some_file | http_monitor
```
You can adjust the period at which the hit summary is displayed (default is 10s)
```
http_monitor sample_csv.txt -p 20
```
Change the window used to raise alert (default is 120s)
```
http_monitor sample_csv.txt -w 180
```
Change the minimum request rate to display the alert (default is 10 rps)
```
http_monitor sample_csv.txt -r 100
```
## Sample result
```
most hit: /api 54 (66.67%)
most hit: /api 61 (67.03%)
most hit: /api 138 (82.14%)
most hit: /api 152 (83.52%)
most hit: /api 149 (83.24%)
High traffic generated an alert - hits = 10.00, triggered at 2019-02-07 21:12:36
most hit: /api 160 (84.21%)
most hit: /api 139 (82.25%)
most hit: /api 160 (84.21%)
most hit: /api 21 (65.62%)
most hit: /api 20 (66.67%)
Traffic went back to normal at 2019-02-07 21:14:04
High traffic generated an alert - hits = 10.00, triggered at 2019-02-07 21:14:04
Traffic went back to normal at 2019-02-07 21:14:05
most hit: /api 18 (66.67%)
most hit: /api 20 (66.67%)
most hit: /api 22 (66.67%)
most hit: /api 20 (66.67%)
most hit: /api 20 (66.67%)
most hit: /api 249 (89.25%)
most hit: /api 249 (89.25%)
High traffic generated an alert - hits = 10.00, triggered at 2019-02-07 21:16:03
most hit: /api 249 (89.25%)
most hit: /api 251 (89.32%)
most hit: /api 250 (89.29%)
most hit: /report 11 (50.0%)
most hit: /report 10 (52.63%)
most hit: /api 10 (50.0%)
most hit: /api 10 (52.63%)
most hit: /report 10 (50.0%)
Traffic went back to normal at 2019-02-07 21:18:24
most hit: /report 10 (52.63%)
most hit: /api 11 (50.0%)
most hit: /api 11 (52.38%)

```

# Improvements

1. Currently, the mean request is computed using the watched window. Spikes in throughput will be smoothed on this window and can trigger alert eventhough the event was way shorter than the window. The current rate computation could be improve by working on the sliding period.
2. This tool could also raise alerts whenever the number of server error raise another (smaller) rate. This could be done similarly than throughput monitor but lookin only at 5** requests.