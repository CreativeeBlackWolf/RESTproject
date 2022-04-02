# RESTproject

bank api via django rest framework

basic url is `/api/v1`

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

## Transactions

### /api/v1/transactions/

#### Requests

**GET**: Returns a list of transactions.
**POST**: Creates a transaction.

##### GET Parameters

- `wallet`: wallet UUID
- `wallet_name`: wallet name (wow)
- `payment`: amount of money
- `whence`: where/from the money were sent/recieved
- `max_payment`: less or equal payment
- `min_payment`: greater or equal payment
- `comment`: comment for transaction

##### POST Parameters

- `wallet`: wallet UUID
- `payment`: amount of money to send
- `whence`: where to send money
- `comment`: payment comment

### /api/v1/transactions/\<int:transaction_id\>

#### Requests

**GET**: Returns a single transaction
**DELETE**: Deletes a transaction

## Transfers

### /api/v1/transfers

#### Requests

**GET**: Returns a transfers list
**POST**: Creates a transfer

##### GET Parameters

- `from_wallet`: UUID field for wallet that initialized transaction
- `from_wallet_name`: wallet name for wallet that initialized transaction
- `to_wallet`:  UUID field for wallet that got payment
- `to_wallet_name`: wallet name for wallet that got payment
- `payment`: amount of money
- `max_payment`: payment but less or equal
- `min_payment`: payment but greater or equal
- `comment`: comment for transaction

##### POST Parameters

- `from_wallet`: UUID field for wallet that transfers money
- `to_wallet`: UUID field for wallet that receives payment
- `payment`: amount of money
- `comment`: comment for transfer

### /api/v1/transfers/\<int:transfer_id\>

#### Requests

**GET**: Returns a single transfer
**DELETE**: Deletes a transfer
