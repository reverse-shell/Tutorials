methods {
    ticketDepot(uint64);
	createEvent(uint64,uint16) returns uint16;        
    buyNewTicket(uint16,address) returns uint16;
	offerTicket(uint16,uint16,uint64,address,uint16);
	buyOfferedTicket(uint16,uint16,address);

    /* HARNESS */
    getNumEvents() returns uint16 envfree;
    getOwner() returns address envfree;
    getTransactionFee() returns uint64 envfree;
    getEventOwner(uint16) returns address envfree;
    getEventTicketPrice(uint16) returns uint64 envfree;
    getEventTicketsRemaining(uint16) returns uint16 envfree;
    getOfferingBuyer(bytes32) returns address envfree;
    getOfferingPrice(bytes32) returns uint64 envfree;
    getOfferingDeadline(bytes32) returns uint256 envfree;
    getNumEvent() returns uint16 envfree;
}

definition eventNoExists(uint16 eventId) returns bool =
    getEventOwner(eventId) == 0 &&
    getEventTicketPrice(eventId) == 0 &&
    getEventTicketsRemaining(eventId) == 0;

definition eventExists(uint16 eventId) returns bool =
    getEventOwner(eventId) != 0;

definition offeringNoExists(bytes32 offeringId) returns bool =
    getOfferingBuyer(offeringId) == 0 &&
    getOfferingPrice(offeringId) == 0 &&
    getOfferingDeadline(offeringId) == 0;

definition offeringExists(bytes32 offeringId) returns bool =
    getOfferingDeadline(offeringId) != 0;

rule eventNoExistsToExists(method f, uint16 eventId) {
    env e;
    calldataarg args;

    require eventNoExists(eventId);
    f(e, args);
    assert eventExists(eventId) => f.selector == createEvent(uint64,uint16).selector,
        "failed created event via not createEvent";
}

rule offeringNoExistsToExists(method f, bytes32 offeringId) {
    env e;
    calldataarg args;

    require offeringNoExists(offeringId);
    f(e, args);
    assert offeringExists(offeringId) => f.selector == offerTicket(uint16,uint16,uint64,address,uint16).selector,
        "failed created offering not via offerTicket";
}

rule offeringExistsToNoExists(method f, bytes32 offeringId) {
    env e;
    calldataarg args;

    require offeringExists(offeringId);
    f(e, args);
    assert offeringNoExists(offeringId) => f.selector == buyOfferedTicket(uint16,uint16,address).selector,
        "failed deleted offering not via buyOfferedTicket";
}

rule increaseNumEvents(method f) {
    env e;
    calldataarg args;

    uint16 numEventsBefore = getNumEvents();
    f(e, args);
    uint16 numEventsAfter = getNumEvents();
    assert numEventsBefore <= numEventsAfter, "failed, numEvents decreased";
}

rule ownerCannotChange(method f) {
    env e;
    calldataarg args;

    address ownerBefore = getOwner();
    f(e, args);
    address ownerAfter = getOwner();
    assert ownerBefore == ownerAfter, "failed, owner has changed";
}

rule transactionFeeCannotChange(method f) {
    env e;
    calldataarg args;

    uint64 transactionFeeBefore = getTransactionFee();
    f(e, args);
    uint64 transactionFeeAfter = getTransactionFee();
    assert transactionFeeBefore == transactionFeeAfter,
        "failed, transactionFee has changed";
}

rule eventOwnerCannotChange(method f, uint16 eventId) {
    env e;
    calldataarg args;

    require eventExists(eventId);
    address eventOwnerBefore = getEventOwner(eventId);
    f(e, args);
    address eventOwnerAfter = getEventOwner(eventId);
    assert eventOwnerBefore == eventOwnerAfter,
        "failed, event.owner has changed";
}

rule eventTicketPriceCannotChange(method f, uint16 eventId) {
    env e;
    calldataarg args;

    require eventExists(eventId);
    address eventTicketPriceBefore = getEventTicketPrice(eventId);
    f(e, args);
    address eventTicketPriceAfter = getEventTicketPrice(eventId);
    assert eventTicketPriceBefore == eventTicketPriceAfter,
        "failed, event.ticketPrice has changed";
}

rule decreaseEventTicketsRemaining(method f, uint16 eventId) {
    env e;
    calldataarg args;

    require eventExists(eventId);
    address eventTicketsRemainingBefore = getEventTicketsRemaining(eventId);
    f(e, args);
    address eventTicketsRemainingAfter = getEventTicketsRemaining(eventId);
    assert eventTicketsRemainingBefore >= eventTicketsRemainingAfter,
        "failed, event.ticketsRemaining increased";
}

