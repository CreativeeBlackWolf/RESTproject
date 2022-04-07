# RESTproject

bank api via django rest framework

basic url is `/api/v1`

---
## Users

### /api/v1/users

#### Overview

Returns users list by GET request and creates a user by POST request.

##### POST Parameters

- `user`: username for new user.

### /api/v1/users/\<int:userid\>

#### Requests

**GET**: Returns a user.
**PUT**: Updates username.
**DELETE**: Deletes a user.

---

## Wallets

### /api/v1/wallets/

#### Requests

**GET**: Returns a list of wallets.
**POST**: Creates a wallet for user.

##### GET Parameters

- `name`: wallet name
- `user`: user id
- `balance`: wallet balance
- `max_balance`: less or equal balance
- `min_balance`: greater or equal balance

##### POST Parameters

- `user`: user id
- `name`: wallet name


### /api/v1/wallets/\<UUID:wallet_id\>

#### Requests

**GET**: Returns a wallet.
**PUT**: Renames a wallet.
**DELETE**: Deletes a wallet.

##### PUT Parameters

- `name`: New wallet name
- `user`: User ID who owns a wallet

---

## Transactions

### /api/v1/transactions/

#### Requests

**GET**: Returns a list of transactions.
**POST**: Creates a transaction.

##### GET Parameters

- `from_wallet`: UUID for wallet that initialized transaction
- `from_wallet_name`: wallet name (wow)
- `to_wallet`: wallet UUID for wallet that got payment
- `payment`: amount of money
- `whence`: where/from the money were sent/received
- `max_payment`: less or equal payment
- `min_payment`: greater or equal payment
- `comment`: comment for transaction

##### POST Parameters

- `from_wallet`: wallet UUID
- _OR_ `to_wallet`: wallet UUID that receives payment
- _OR_ `whence`: where to send money
- `payment`: amount of money to send
- `comment`: payment comment

**IMPORTANT**: One of `to_wallet` or `whence` fields should have value!

### /api/v1/transactions/\<int:transaction_id\>

#### Requests

**GET**: Returns a single transaction
**DELETE**: Deletes a transaction

### /api/v1/transactions/ATM_action

#### Requests

**POST**: Create an ATM transaction.

##### POST Parameters

- `from_wallet`: wallet UUID
- `whence`: `ATM Deposit` OR `ATM Withdraw`
- `payment`: amount of money
