certoraRun MeetingSchedulerFixed.sol:MeetingScheduler \
--verify MeetingScheduler:meetings.spec \
--solc solc8.7 \
--rule monotonousIncreasingNumOfParticipants \
--msg "test message"