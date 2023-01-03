
# Properties

1. *Valid state* `noUser` - balanceOf(user) == 0 and feesCollectedPerShare == 0 and rewards == 0
2. *Valid state* `user` - balanceOf(user) > 0 or feesCollectedPerShare > 0 or rewards > 0
3. *State transition* - noUser => user via deposit
4. *Variable transition* - `totalFeesEarnedPerShare` can only increase
5. *Variable transition* `UserInfo.feesCollectedPerShare` can only increase
6. *Variable transition* `UserInfo.feesCollectedPerShare` <= `totalFeesEarnedPerShare`
7. *High-level* balanceOf all users is equal to totalSupply
8. *Unit tests* `ERC20.transfer` - transfers to another user
9. *Unit tests* `ERC20.approve` approves spender to amount
10. *Unit tests* `ERC20.transferFrom` transfers other user funds
11. *Unit tests* `ERC20.increase_allowance` increases allowance
12. *Unit tests* `ERC20.decrease_allowance` - decreases allowance
13. *Unit tests* `deposit` - deposits eth and mints tokens
14. *Unit tests* `withdraw` - withdraws eth and burns tokens
15. *Unit tests* `collectFees` - collects the fees
16. *Unit tests* `OwnerDoItsJobAndEarnsFeesToItsClients` - increases `totalFeesEarnedPerShare`