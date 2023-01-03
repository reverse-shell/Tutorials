# Properties
## States
* UNINITIALIZED - before creation:
    * start = 0
    * end = 0
    * numOfParticipents = 0
    * organizer = 0
    * status = 0

* PENDING - at creation:
    * start != 0
    * end != 0
    * start < end
    * numOfParticipents = 0
    * organizer != 0
    * status = 1

* STARTED:
    * start != 0
    * start < now
    * end != 0
    * start < end
    * numOfParticipents = any
    * organizer != 0
    * status = 2
* ENDED:
    * start != 0
    * end != 0
    * start < end
    * end < now
    * numOfParticipents = any
    * organizer != 0
    * status = 3

* CANCELLED
    * start != 0
    * end != 0
    * start <= now
    * start < end
    * numOfParticipents = 0
    * organizer != 0
    * status = 4

## States Transitions
* UNINITIALIZED => PENDING (ANY)
* PENDING => STARTED if start < now
* STARTED => ENDED if end < now
* PENDING => CANCELLED

## Variables Transitions
* ScheduledMeeting.numOfParticipents - can only increase
* ScheduledMeeting.status - can only increase

## High-level properties
* ScheduledMeeting.startTime < ScheduledMeeting.endTime
* Not possible to cancel the meeting if it has started 

## Unit Tests
* scheduleMeeting changes UNINITIALIZED => PENDING
* startMeeting changes PENDING => STARTED
* cancelMeeting changes PENDING => CANCELLED
* endMeeting changes STARTED => ENDED
* joinMeeting changes increases numOfParticipents


# Prioritizing
All properties are important for now