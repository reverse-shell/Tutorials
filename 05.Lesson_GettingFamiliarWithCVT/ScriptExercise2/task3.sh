certoraRun MeetingSchedulerFixed.sol:MeetingScheduler \
--verify MeetingScheduler:meetings.spec \
--solc solc8.7 \
--rule monotonousIncreasingNumOfParticipants \
--method "startMeeting(uint256)" \
--msg "test message"