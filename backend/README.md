# Backend Structure

### /Resources (serverless/resources)

YAML files of cloud resources to be deployed using the Serverless framework

- **api-gateway.yml**
  - Authorizer: used to validate incoming api calls against cognito user pools


- **cognito-indentity-pool.yml**
  - Used to create a pool name based on the stage and to prevent unauthenticated users
  - Link to cognito user pool
  - Specify the role user for authenticated users


- **cognito-user-pool.yml**
  - Sets email as user alias
  - Generate pool and client name based on stage
  - Print out the Id and user pool for client


- **dynamodb-tables.yml**:  Create the 3 DB tables used by the DVSA app:
  - DVSA-INVENTORY-DB: Holds all store items
  - DVSA-USERS-DB: Holds user profile information (email, avatar, address). Used by client
  - DVSA-ORDERS-DB: Holds orders made by users


- **funtion-roles.yml**: Defines roles for functions in the applications:
  - dvsaOrderRole: used by most functions. Allows any action on any dynamodb table (dynamodb:*)
  - dvsaAdminRole: used by the admin functions. Permissions to db and to the s3 bucket
  - dvsaCronjobsRole: used by the cornjob functions. Permissions to dbs and invoking functions

- **s3-bucket.yml**: Defines the S3 bucket to be created in the app
  - dvsa-receipts-bucket-{accountId}: used to hold all the receipts created per paid orders. 
  - A link is sent to the email to download the receipt from this bucket



### /Scripts (serverless/scripts)

- **onstart.py**: Disclaimer

- **vars.js**: Get AWS Account Id for bucket naming

- **verifysesaccount.py**: 

A script to verify the dvsa.noreply@mailsac.com email for the account. This is used to send the receipts to the users.

- **create-inventory-data.json**

This file is used to fill-in the inventory database after deployment.

- - - 
## Source Code (src/functions)

### /admin
Administration functions (backoffice). Unconnected to any UI at the moment. But can be invoked directly.

All folders hold an **sls.yml** file, used by the Serverless framework to delpoy.

- **admin_get_orders.py**

Returns list of orders based on filters (by user, date, status, etc.)

- **admin_get_receipts.py**

Creates a zip file for receipts from the S3 bucket and returns back a link to download them.

- **admin_update_inventory.py**

Update items in inventory (add, update, delete).

- **admin_update_orders.py**

Update orders (add, update, delete).

- **admin_tweet.py**

Can be used to tweet from the Twitter account (@DVSAowasp) - not completely functioning. But holds the account tokens, so it can be hacked tweeted directly to the account. 



### /cronjobs

Cronjob functions launches once daily and do some cleanup in the account.

- **cron_cleaner.py**

Runs daily and removes any order which was not completed (Status 100).

- **cron_job_update.py**

Runs daily and looks for orders which were paied but not processed (status 120). This will change the status to 200, and will trigger the order processing, which also incldues the receipt email.

- **cron_processor.py**

Runs daily. Acts as a mock processing of the orders. Changes order status from processed to shipped to delivered.


### /order-api

- **order-manager-js.js**
One NodeJS function which is tirggered by the API calls from the client. The function receives the action in the request payload and invokes the relevant function accordingly. (it is also using **vulnerable** libraries).


### /order

These functioins handle the ordering from the website.

- **cancel_order.py**

Allow users to cancel orders which are not successfully paid yet.

- **get_order.py**

Get information about a specific order. 

- **get_orders.py**

Get list of orders (status +110) of the users.

- **order_billing.py**

The function that in charge of the billing. It calls two other functions via REST API, to calucalte the total of the order and to validate the payment method (these functioins can be found under the `/processing` folder).
order status changes to 120 if sucessfull, or to 110 if payment failed.

- **new_order.py**

Create a new order in the database with the data sent by the user.

- **update_order.py**

Updates an existing order in the database.

- **order_shipping.py**

Update shipping address of an order in the database with the details sent by the user as part of the order flow.


### /user

These functions handle user account and data.

- **user_account.py**

upon login, sends account data (address, email, etc.) to client.


- **user_create.py**

Triggered when user is confirmed. create an entry in the DVSA-USERS-DB.


- **user_profile.py**

Allow users to update profile data (name, address, avatar, etc.)

- **user_inbox.py**

Allow users to receive receipts for their completed orders


### /processing

These functions handle orders, but are not triggered directly from the user (although they can be :) )

- **get_cart_total.py**

Called when billing is sent to calcualte the cart total amount to pay from the according to the prices in the inventory db.

- **payment_processing.py**

Acts as a mock for online payment processing (Stripe-like), but runs inside the account. The function verifies the credit card number according to luhn algorithm and that the expiry date is valid.
When approved, changes the order status in the db to 120.


- **create_receipt.py**

Called when an order was successfuly paied. Creates a receipt for the order and uploads it to the s3 bucket


- **send_receipt_email.py**

Triggered when a recipt was uploaded to the s3 bucket. Changes the order status to processing. In addition, it modifies the original receipt (.raw) and uploads a new receipt file (.txt). This function is **vulnerable**.
