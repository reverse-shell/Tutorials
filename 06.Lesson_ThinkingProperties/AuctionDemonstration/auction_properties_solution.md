
# States
* Auction States:
    - doesNotExist
    - exists

# State Transition
* newAuction: doesNotExist -> exists
* close: exists -> doesNotExist

# Variable Transition
* owner cannot change
* AuctionStrcut:
    - prize -> decreasing
    - payment -> static
    - winner -> keep changing to msg.sender
    - bid_expiry -> increase - now + 1 hours
    - end_time -> static

# High-Level Properties
* balances all users == totalSupply

# Unit Testing
* mint:
    - properly increases the balance and total supply
* transferTo:
    - `msg.sender` to `_to` amount of `_value` tokens
* newAuction:
    - creates new auction
* bid:
    - bids on an auction
* close:
    - deletes auction if:
        - now > bid_expiry || now > end_time