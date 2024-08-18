# Inside Elevator

A single elevator has the following interfaces - both human and APIs...

## Controls

* destination floor push buttons
* close door push button
* open door push button

## Sensors

* open doors sensor
* load sensor - see attribute load below

## Indicators

Min:

* floor push buttons indicator
* ceiling light

Better:

* current floor indicator
* movement direction indicator

## Attributes

* load: none, some, too-much
* ceiling light: some, on
* current floor
* destination floor(s)

## State Machine

* idle - no movements, no load
* going - target floors, load can be none
* doors opening
* doors closing
