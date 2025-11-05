# MacSecurity
A security app using facial recognition that locks your mac when needed. This code also works on windows.

## Instructions

### Prepare

Prepare one photo of the target. Name it "my_portrait.jpeg" and put it in the running directory.

Install the dependents:
```
pip3 install -r requirements.txt
```

### Run
normal run:
```
python3 main.py
```
run with low interval (high speed):
```
python3 main.py -s high
```
Or use "low" to run with higher interval

### Find-tune for Camera

You need to turn off all the unnecessary plug-ins on the mac book to reduce the possiblity for causing unexpected problems.

It's good and recommend to open the "Stage light" function on mac to boost the recognition. 

## Contribute

This respository accepts and welcome your contribution.

## Info

These codes belong to ThomasB. Open-source under Apache License 2.0.

Codes are been tested on a MacBook Pro, might don't work for windows or other cameras instead of the build-in one.
