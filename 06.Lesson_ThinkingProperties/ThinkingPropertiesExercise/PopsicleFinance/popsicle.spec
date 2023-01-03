methods {
    balanceOf(address) returns uint256 envfree;
    transfer(address,uint256);
    transferFrom(address,address,uint256);
    approve(address,uint256);
    allowanceOf(address,address) returns uint256 envfree;
    deposit();
    withdraw(uint256);
    collectFees();
    OwnerDoItsJobAndEarnsFeesToItsClients();
    getUserFeesCollectedPerShare(address) returns uint256 envfree;
    getUserRewards(address) returns uint256 envfree;
    getTotalFeesEarnedPerShare() returns uint256 envfree;
    totalSupply() returns uint256 envfree;
}

definition noUser(address user) returns bool =
    balanceOf(user) == 0 &&
    getUserFeesCollectedPerShare(user) == 0 &&
    getUserRewards(user) == 0;

definition isUser(address user) returns bool =
    balanceOf(user) > 0 ||
    getUserFeesCollectedPerShare(user) > 0 &&
    getUserRewards(user) > 0;

ghost ghostSupply() returns uint256;
hook Sstore balances[KEY address a] uint256 balance (uint256 old_balance) STORAGE {
    havoc ghostSupply assuming ghostSupply@new() == ghostSupply@old() + (balance - old_balance);
}

rule totalSupplyEqualSumOfBalances(method f) {
    env e;
    calldataarg args;
    require totalSupply() == ghostSupply();
    f(e, args);
    assert totalSupply() == ghostSupply(), "failed totalSupply different than sum of balances";
}

rule fromNoUserToUser(method f, address user) {
    env e;
    calldataarg args;

    require noUser(user);
    f(e, args);
    assert isUser(user) => 
        (
            f.selector == deposit().selector ||
            f.selector == transferFrom(address,address,uint256).selector ||
            f.selector == transfer(address,uint256).selector),
        "became user via wrong method";
}

rule increaseTotalFeesEarnedPerShare(method f) {
    env e;
    calldataarg args;
    uint256 totalFeesEarnedPerShareBefore = getTotalFeesEarnedPerShare();
    f(e, args);
    uint256 totalFeesEarnedPerShareAfter = getTotalFeesEarnedPerShare();

    assert totalFeesEarnedPerShareBefore <= totalFeesEarnedPerShareAfter,
        "failed totalFeesEarnedPerShare should only increase";
}

rule increaseFeesCollectedPerShare(method f, address user) {
    env e;
    calldataarg args;
    uint256 feesCollectedPerShareBefore = getUserFeesCollectedPerShare(user);
    f(e, args);
    uint256 feesCollectedPerShareAfter = getUserFeesCollectedPerShare(user);

    assert feesCollectedPerShareBefore <= feesCollectedPerShareAfter,
        "failed feesCollectedPerShare should only increase";
}

rule feesCollectedPerShareSmallerThanTotal(method f, address user) {
    env e;
    calldataarg args;
    require getUserFeesCollectedPerShare(user) <= getTotalFeesEarnedPerShare();
    f(e, args);
    assert getUserFeesCollectedPerShare(user) <= getTotalFeesEarnedPerShare(),
        "failed feesCollectedPerShare bigger than totalFees";
}

rule unitDeposit() {
    env e;

    uint256 balanceBefore = balanceOf(e.msg.sender);
    deposit(e);
    uint256 balanceAfter = balanceOf(e.msg.sender);

    assert balanceAfter == balanceBefore + e.msg.value,
        "failed to deposit eth";
}

rule unitWithdraw(uint256 amount) {
    env e;

    uint256 balanceBefore = balanceOf(e.msg.sender);
    withdraw(e, amount);
    uint256 balanceAfter = balanceOf(e.msg.sender);

    assert balanceAfter == balanceBefore - amount,
        "failed to withdraw";
}

rule uintCollectFees() {
    env e;

    uint256 rewardBefore = getUserRewards(e.msg.sender);
    collectFees(e);
    uint256 rewardAfter = getUserRewards(e.msg.sender);
    assert rewardAfter == 0, "failed to collect fees";
}

rule unitOwnerDoItsJobAndEarnsFeesToItsClients() {
    env e;
    uint256 totalFeesEarnedPerShareBefore = getTotalFeesEarnedPerShare();
    OwnerDoItsJobAndEarnsFeesToItsClients(e);
    uint256 totalFeesEarnedPerShareAfter = getTotalFeesEarnedPerShare();
    assert totalFeesEarnedPerShareAfter == totalFeesEarnedPerShareBefore + 1,
        "failed to OwnerDoItsJobAndEarnsFeesToItsClients";
}

rule unitTransfer(address recipient, uint256 amount) {
    env e;
    require e.msg.sender != recipient;
    uint256 balanceBeforeSender = balanceOf(e.msg.sender);
    uint256 balanceBeforeRecipient = balanceOf(recipient);
    transfer(e, recipient, amount);
    uint256 balanceAfterSender = balanceOf(e.msg.sender);
    uint256 balanceAfterRecipient = balanceOf(recipient);
    assert balanceBeforeSender - amount == balanceAfterSender, "failed balance sender";
    assert balanceBeforeRecipient + amount == balanceAfterRecipient, "failed balance recipient";
}

rule unitApprove(address spender, uint256 amount) {
    env e;
    uint256 allowanceBefore = allowanceOf(e.msg.sender, spender);
    approve(e, spender, amount);
    uint256 allowanceAfter = allowanceOf(e.msg.sender, spender);

    assert allowanceAfter != allowanceBefore => allowanceAfter == amount, "failed to approve";
}

rule unitTransferFrom(address sender, address recipient, uint256 amount) {
    env e;
    require sender != recipient;
    uint256 balanceBeforeSender = balanceOf(sender);
    uint256 balanceBeforeRecipient = balanceOf(recipient);
    transferFrom(e, sender, recipient, amount);
    uint256 balanceAfterSender = balanceOf(sender);
    uint256 balanceAfterRecipient = balanceOf(recipient);
    assert balanceBeforeSender - amount == balanceAfterSender, "failed balance sender";
    assert balanceBeforeRecipient + amount == balanceAfterRecipient, "failed balance recipient";  
}