# RESTproject

bank api via django rest framework

basic url is `/api/v1`

## Users

### /api/v1/users

#### Overview

Returns users list by GET request and creates a user by POST request.

##### POST Parameters

- `user`: username for new user.

## Wallets

### /api/v1/wallets/\<userid\>

#### Overview

Returns a wallets list for current user by GET request.

### /api/v1/wallets/\<userid\>/get_by_name

#### Overview

Returns a wallet by name for current user by GET request.

##### GET Parameters

- `wallet_name`: unique wallet name.

### /api/v1/wallets/\<userid\>/\<create_wallet\> OR <delete_wallet\>

#### Overview

Creates or deletes a wallet by POST request.

##### POST Parameters

- `wallet_name`: unique wallet name.

## Transactions

### /api/v1/transactions/

#### Overview

Returns a list of transactions by GET request.

##### GET Parameters

- `from_wallet`: UUID field for wallet that initialized transaction.
- `from_wallet_name`: wallet name for wallet that initialized transaction.
- `to_wallet`:  UUID field for wallet that got payment.
- `to_wallet_name`: wallet name for wallet that got payment.
- `payment`: amount of money.
- `max_payment`: payment but less or equal.
- `min_payment`: payment but greater or equal.
- `comment`: comment for transaction.
