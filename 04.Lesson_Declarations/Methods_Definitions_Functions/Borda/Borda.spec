
methods {
    getPointsOfContender(address contender) returns(uint256) envfree;
    hasVoted(address voter) returns(bool) envfree;
    getWinner() returns(address, uint256) envfree;
    getFullVoterDetails(address voter) returns(uint8 age, bool registered, bool voted, uint256 vote_attempts, bool black_listed) envfree;
    getFullContenderDetails(address contender) returns(uint8 age, bool registered, uint256 points) envfree;
    registerVoter(uint8 age) returns (bool);
    registerContender(uint8 age) returns (bool);
    vote(address first, address second, address third) returns(bool);
}

function getAge(address voter) returns uint256 {
    uint256 age; bool voterRegBefore; bool voted; uint256 vote_attempts; bool blocked;
    age, voterRegBefore, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return age;
}

function getRegistered(address voter) returns bool {
    uint256 age; bool registered; bool voted; uint256 vote_attempts; bool blocked;
    age, registered, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return registered;
}

function getBlocked(address voter) returns bool {
    uint256 age; bool registered; bool voted; uint256 vote_attempts; bool blocked;
    age, registered, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    return blocked;
}

definition unRegisteredVoter(address voter) returns bool = !getRegistered(voter);
definition registeredYetVotedVoter(address voter) returns bool = getRegistered(voter) && !hasVoted(voter);
definition legitRegisteredVotedVoter(address voter) returns bool = getRegistered(voter) && hasVoted(voter) && !getBlocked(voter);
definition blockedVoter(address voter) returns bool = getRegistered(voter) && hasVoted(voter) && getBlocked(voter);


// Checks that a voter's "registered" mark is changed correctly - 
// If it's false after a function call, it was false before
// If it's true after a function call, it either started as true or changed from false to true via registerVoter()
rule registeredCannotChangeOnceSet(method f, address voter){
    env e; calldataarg args;
    uint256 age; bool voterRegBefore; bool voted; uint256 vote_attempts; bool blocked;
    age, voterRegBefore, voted, vote_attempts, blocked = getFullVoterDetails(voter);
    f(e, args);
    bool voterRegAfter;
    age, voterRegAfter, voted, vote_attempts, blocked = getFullVoterDetails(voter);

    assert (!voterRegAfter => !voterRegBefore, "voter changed state from registered to not registered after a function call");
    assert (voterRegAfter => 
        ((!voterRegBefore && f.selector == registerVoter(uint8).selector) || voterRegBefore), 
            "voter was registered from an unregistered state, by other function then registerVoter()");
}

// Checks that each voted contender receieves the correct amount of points after each vote
rule correctPointsIncreaseToContenders(address first, address second, address third){
    env e;
    uint256 firstPointsBefore = getPointsOfContender(first);
    uint256 secondPointsBefore = getPointsOfContender(second);
    uint256 thirdPointsBefore = getPointsOfContender(third);

    vote(e, first, second, third);
    uint256 firstPointsAfter = getPointsOfContender(first);
    uint256 secondPointsAfter = getPointsOfContender(second);
    uint256 thirdPointsAfter = getPointsOfContender(third);
    
    assert (firstPointsAfter - firstPointsBefore == 3, "first choice receieved other amount than 3 points");
    assert (secondPointsAfter - secondPointsBefore == 2, "second choice receieved other amount than 2 points");
    assert ( thirdPointsAfter- thirdPointsBefore == 1, "third choice receieved other amount than 1 points");

}

// Checks that a blocked voter cannot get unlisted
rule onceBlockedNotOut(method f, address voter){
    env e; calldataarg args;
    uint256 age; bool registeredBefore; bool voted; uint256 vote_attempts; bool blocked_before;
    //age, registeredBefore, voted, vote_attempts, blocked_before = getFullVoterDetails(voter);
    registeredBefore = getRegistered(voter);
    blocked_before = getBlocked(voter);
    require blocked_before => registeredBefore;
    f(e, args);
    bool registeredAfter; bool blocked_after;
    //age, registeredAfter, voted, vote_attempts, blocked_after = getFullVoterDetails(voter);
    registeredAfter = getRegistered(voter);
    blocked_after = getBlocked(voter);

    assert blocked_before => blocked_after, "the specified user got out of the blocked users' list";
}

// Checks that a contender's point count is non-decreasing
rule contendersPointsNondecreasing(method f, address contender){
    env e; calldataarg args;
    uint8 age; bool registeredBefore; uint256 pointsBefore;
    age, registeredBefore, pointsBefore = getFullContenderDetails(contender);
    require pointsBefore > 0 => registeredBefore; 
    f(e,args);
    bool registeredAfter; uint256 pointsAfter;
    age, registeredAfter, pointsAfter = getFullContenderDetails(contender);

    assert (pointsAfter >= pointsBefore);
}

