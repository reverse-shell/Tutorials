methods {
    getStateById(uint256) returns uint8 envfree;
    getStartTimeById(uint256) returns uint256 envfree;
    getEndTimeById(uint256) returns uint256 envfree;
    getNumOfParticipents(uint256) returns uint256 envfree;
    scheduleMeeting(uint256,uint256,uint256);
    startMeeting(uint256);
    cancelMeeting(uint256);
    endMeeting(uint256);
    joinMeeting(uint256) envfree;
}

definition meetingUninitialized(uint256 meetingId) returns bool = 
    getStateById(meetingId) == 0 &&
    getStartTimeById(meetingId) == 0 &&
    getEndTimeById(meetingId) == 0 &&
    getNumOfParticipents(meetingId) == 0;

definition meetingPending(uint256 meetingId) returns bool =
    getStateById(meetingId) == 1 &&
    getStartTimeById(meetingId) != 0 &&
    getEndTimeById(meetingId) != 0 &&
    getStartTimeById(meetingId) < getEndTimeById(meetingId) &&
    getNumOfParticipents(meetingId) == 0;

definition meetingStarted(env e, uint256 meetingId) returns bool =
    getStateById(meetingId) == 2 &&
    getStartTimeById(meetingId) != 0 &&
    getEndTimeById(meetingId) != 0 &&
    getStartTimeById(meetingId) < getEndTimeById(meetingId) &&
    getStartTimeById(meetingId) <= e.block.timestamp;

definition meetingEnded(env e, uint256 meetingId) returns bool =
    getStateById(meetingId) == 3 &&
    getStartTimeById(meetingId) != 0 &&
    getEndTimeById(meetingId) != 0 &&
    getStartTimeById(meetingId) < getEndTimeById(meetingId) &&
    getStartTimeById(meetingId) <= e.block.timestamp &&
    getEndTimeById(meetingId) <= e.block.timestamp;

definition meetingCancelled(uint256 meetingId) returns bool =
    getStateById(meetingId) == 4 &&
    getStartTimeById(meetingId) != 0 &&
    getEndTimeById(meetingId) != 0 &&
    getStartTimeById(meetingId) < getEndTimeById(meetingId);


rule uninitializedToPending(method f, uint256 meetingId) {
    env e;
    calldataarg args;

    require meetingUninitialized(meetingId);

    uint8 statusBefore = getStateById(meetingId);
    f(e, args);
    uint8 statusAfter = getStateById(meetingId);
    
    assert statusBefore != statusAfter => meetingPending(meetingId),
        "failed from uninitiliazed to pending";
}

rule pendingToStarted(method f, uint256 meetingId) {
    env e;
    calldataarg args;

    require meetingPending(meetingId);

    uint8 statusBefore = getStateById(meetingId);
    f(e, args);
    uint8 statusAfter = getStateById(meetingId);

    assert statusBefore != statusAfter => 
        (meetingStarted(e, meetingId) || meetingCancelled(meetingId)),
        "failed from pending to started";
}

rule startedToEnded(method f, uint256 meetingId) {
    env e;
    calldataarg args;

    require meetingStarted(e, meetingId);

    uint8 statusBefore = getStateById(meetingId);
    f(e, args);
    uint8 statusAfter = getStateById(meetingId);

    assert statusBefore != statusAfter => meetingEnded(e, meetingId),
        "failed from started to ended";
}

rule pendingToCancel(method f, uint256 meetingId) {
    env e;
    calldataarg args;

    require meetingPending(meetingId);

    uint8 statusBefore = getStateById(meetingId);
    f(e, args);
    uint8 statusAfter = getStateById(meetingId);

    assert statusBefore != statusAfter =>
        (meetingCancelled(meetingId) || meetingStarted(e, meetingId)),
        "failed from pending to cancel";
}

rule endedCannotChange(method f, uint256 meetingId) {
    env e;
    calldataarg args;

    require meetingEnded(e, meetingId);
    f(e, args);
    assert meetingEnded(e, meetingId), "failed ended has changed";
}

rule cancelledCannotChange(method f, uint256 meetingId) {
    env e;
    calldataarg args;

    require meetingCancelled(meetingId);
    f(e, args);
    assert meetingCancelled(meetingId), "failed cancelled changed";

}

rule increaseNumOfParticipents(method f, uint256 meetingId) {
    env e;
    calldataarg args;

    require meetingPending(meetingId) || meetingStarted(e, meetingId) ||
        meetingCancelled(meetingId) || meetingEnded(e, meetingId);

    uint256 participentsBefore = getNumOfParticipents(meetingId);
    f(e, args);
    uint256 participentsAfter = getNumOfParticipents(meetingId);

    assert participentsBefore <= participentsAfter, "failed numOfParticipents decreased";
}

rule increaseStatus(method f, uint256 meetingId) {
    env e;
    calldataarg args;

    require !meetingUninitialized(meetingId);
    uint8 statusBefore = getStateById(meetingId);
    f(e, args);
    uint8 statusAfter = getStateById(meetingId);

    assert statusBefore <= statusAfter, "failed status decreased";
}

rule startTimeLowerThanEndTime(method f, uint256 meetingId) {
    env e;
    calldataarg args;

    require meetingPending(meetingId) || meetingStarted(e, meetingId) ||
        meetingCancelled(meetingId) || meetingEnded(e, meetingId);

    f(e, args);

    assert getStartTimeById(meetingId) < getEndTimeById(meetingId),
        "failed startTime lower than endTime";
}

rule cannotCancelMeetingIfStarted(uint256 meetingId) {
    env e;

    require meetingStarted(e, meetingId);
    cancelMeeting(e, meetingId);
    assert !meetingCancelled(meetingId),
        "failed to reject cancelling started meeting";
}

rule unitTestScheduleMeeting(uint256 meetingId, uint256 startTime, uint256 endTime) {
    env e;

    require meetingUninitialized(meetingId);
    scheduleMeeting(e, meetingId, startTime, endTime);
    assert meetingPending(meetingId), "failed to schedule meeting";
}

rule unitTestStartMeeting(uint256 meetingId) {
    env e;
    
    require meetingPending(meetingId);
    startMeeting(e, meetingId);
    assert meetingStarted(e, meetingId), "failed to start meeting";
}

rule unitTestEndMeeting(uint256 meetingId) {
    env e;

    require meetingStarted(e, meetingId);
    endMeeting(e, meetingId);
    assert meetingEnded(e, meetingId), "failed to end meeting";
}

rule unitTestCancelMeeting(uint256 meetingId) {
    env e;

    require meetingPending(meetingId);
    cancelMeeting(e, meetingId);
    assert meetingCancelled(meetingId), "failed to cancel meeting";
}

rule unitTestJoinMeeting(uint256 meetingId) {
    env e;

    uint256 numOfParticipentsBefore = getNumOfParticipents(meetingId);
    joinMeeting(meetingId);
    uint256 numOfParticipentsAfter= getNumOfParticipents(meetingId);
    assert numOfParticipentsAfter == numOfParticipentsBefore + 1,
        "failed to join the meeting";
}