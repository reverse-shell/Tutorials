
1. *Valid State* `eventNoExists` => owner == 0 && ticketPrice == 0 && ticketsRemaining == 0
2. *Valid State* `eventExists` => owner != 0
3. *Valid State* `offeringNoExists` => buyer == 0 && price == 0 && deadline == 0
4. *Valid State* `offeringExists` => deadline != 0
5. *State Transition* `eventNoExists` => `eventExists` via createEvent
6. *State Transition* `offeringNoExists` => `offeringExists` via offerTicket
7. *State Transition* `offeringExists` => `offeringNoExists` via buyOfferedTicket
8. *Variable Transition* `numEvents` should increase only
9. *Variable Transition* `owner` should not change
10. *Variable Transition* `transactionFee` should not change
11. *Variable Transition* `Event.owner` should not change
12. *Variable Transition* `Event.ticketPrice` should not change
13. *Variable Transition* `Event.ticketsRemaining` should only decrease
14. *High-Level Property* Sum of all attendees equal number of sold tickets
15. *High-Level Property* Sum of all eth equals or higher to number of `attendees * ticketPrice`
16. *Unit Test* ticketDepot
17. *Unit Test* createEvent
18. *Unit Test* buyNewTicket
19. *Unit Test* offerTicket
20. *Unit Test* buyOfferedTicket