Section 1: Requirements Pack
1.1 Problem Summary

PayLink is a bill-payment and digital wallet system, similar to Fawry or Vodafone Cash in Egypt. Customers keep money in a wallet and use it to pay their electricity, water, mobile, and internet bills, either from the mobile app or through agents at small shops. PayLink earns a small fee on every payment and pays agents a commission for the payments they handle.

The problem it solves is simple: nobody wants to stand in line at a utility office, and the utility companies want to be paid quickly and correctly. So the system serves customers who want to pay from their phones, agents who help customers in person, and billers who receive the money. Inside the company, support staff and admins also need it to look into payments, manage billers, and adjust fees and limits. The goal is a backend that handles money correctly, makes it easy to add new billers, and stays reliable on the busiest day of the month.

Here is how it works at a high level. The customer enters a meter or phone number, and PayLink asks the biller how much is owed. PayLink adds its fee, runs fraud checks, and puts the total on hold in the wallet. It then sends the payment to the biller. When the biller confirms, the hold becomes a final charge, the customer gets an SMS and a push notification, and every night PayLink compares its records with the biller's settlement file to catch any mismatch. Every money movement is written to a ledger, so balances are always calculated from records and never changed directly.

The hardest part is what happens when something goes wrong. A slow network can send the same payment twice, two payments can arrive at the same moment, a biller can take too long to answer, or the SMS service can go down. PayLink must never charge a customer twice, never let a balance go below zero, and never refund money until it is sure the biller did not receive it. On top of that, each biller works differently (fast or slow, live or delayed, JSON or XML), and the system has to absorb changes in one biller without touching the rest.



1.2 Stakeholder 

Stakeholder	Who They Are	How They Interact with PayLink	What They Expect
Customers	Individuals who pay their utility bills (electricity, water, mobile, internet) using a digital wallet.	Register (basic verification) and optionally upgrade to verified; top up wallet (card or agent cash); check available/held balances and history; look up billers and run bill inquiries; pay bills and receive SMS/push notifications; request refunds for completed payments.	To be charged exactly once, receive clear failure messages, get refunded when a payment fails, and have their funds kept safe.
Agents	Small shop owners operating a PayLink terminal who serve customers in person.	Pay bills on behalf of walk-in customers through the terminal; accept cash from customers to top up wallets; earn a 40% commission on service fees credited to their wallet upon completion.	Fast, reliable payment processing at the terminal and accurate, timely commission payouts.
Administrators	PayLink staff responsible for configuring and managing the platform.	Add, edit, and disable billers and services; edit fee rules, limits, and promotion periods without redeploying; view daily totals (payments, fees earned, commissions paid, failures per biller); have all actions logged in the audit trail.	Easy-to-update configuration without code changes and a clear audit record of every modification.
Support Employees	Customer service staff who handle complaints and investigate payment issues.	Search payments by reference and view full state history; block and unblock accounts; review differences flagged by nightly reconciliation; approve or reject refund requests.	Complete, trustworthy payment histories to explain issues clearly to customers and resolve disputes quickly.
Billers	Utility and telecom companies that issue bills and receive payments (ElectroCo, AquaCo, TopUpNet, NetCo).	Answer bill inquiries and receive payment requests; send confirmations (immediately, via callbacks, or via batch files); send daily settlement files listing received payments.	Accurate payments, no duplicate requests, and end-of-day records that match PayLink's records.
Finance Team	Staff responsible for company accounting and financial oversight.	Monitor service fees earned and commissions paid; review daily reconciliation reports; follow up on mismatches between PayLink records and biller settlement files.	Accurate financial figures, a complete audit trail, and reliable reports for accounting and regulators.
PayLink Management	Company leadership responsible for strategy and business growth.	Monitor overall platform performance and business results; review transaction totals, fee revenue, and biller failure rates; decide when to onboard new billers or adjust business rules.	A reliable, scalable platform that handles peak monthly traffic and protects the company's reputation and regulatory standing.
Development Team	Engineers who build, test, deploy, and maintain the backend system.	Design and implement modules, APIs, and the database; write automated tests and maintain the CI/CD pipeline; onboard new billers and handle API changes (e.g., ElectroCo v2).	A modular, well-tested, well-documented codebase where changes in one area do not break others, with safe automated deployments.


1.3 Functional Requirements (28 User Stories) 
All 28 functional requirements from Section 3.2 are structured below as user stories with Must / Should / Could priorities and Given / When / Then acceptance criteria.


1. Registration and Accounts
US-01: Register an Account
Requirement ID: FR-1 | Priority: Must
User story: As a new customer, I want to register an account so that I can use PayLink to pay my bills.
Acceptance Criteria
Scenario 1: Successful registration
•	Given: The person provides a valid name, phone number, and password, and the phone number is not already registered.
•	When: They submit the registration request.
•	Then: The system creates the customer account with the "basic" verification level and an empty wallet with a 0.00 EGP balance.
Scenario 2: Phone number already registered
•	Given: An account already exists with the same phone number.
•	When: Someone tries to register with that number.
•	Then: The system rejects the request and shows a message that the number is already in use.
Scenario 3: Invalid data
•	Given: The registration request has a missing or badly formatted field.
•	When: The request is submitted.
•	Then: The system rejects it and names the invalid fields. No account is created.
US-02: Upgrade to Verified
Requirement ID: FR-2 | Priority: Should
User story: As a customer, I want to be upgraded to a verified account so that I can pay more per day.
Acceptance Criteria
Scenario 1: Successful upgrade
•	Given: A basic customer has submitted verification and it has been approved.
•	When: The upgrade is applied.
•	Then: The customer's level becomes "verified" and their daily limit changes from 5,000 EGP to 30,000 EGP.
Scenario 2: Already verified
•	Given: The customer is already verified.
•	When: An upgrade is requested again.
•	Then: The system makes no change and informs the user that the account is already verified.
Scenario 3: Verification not approved
•	Given: The verification request was rejected or is still pending.
•	When: The customer tries to pay above 5,000 EGP in a day.
•	Then: The system still applies the basic limit.
________________________________________
2. Wallet Management
US-03: View Wallet Balance and History
Requirement ID: FR-3 | Priority: Must
User story: As a customer, I want to see my available balance, held balance, and transaction history so that I know how much money I have and where it went.
Acceptance Criteria
Scenario 1: View balance
•	Given: The customer is logged in and has a wallet.
•	When: They request their wallet balance.
•	Then: The system shows the available balance and the held balance separately.
Scenario 2: View history
•	Given: The wallet has past transactions.
•	When: The customer requests their transaction history.
•	Then: The system lists the entries (top-ups, holds, charges, refunds) with date, amount, and type, newest first.
Scenario 3: No wallet
•	Given: The customer is logged in but has no wallet.
•	When: They request their balance.
•	Then: The system shows an appropriate message and no balance.
Scenario 4: Another customer's wallet
•	Given: Customer A is logged in.
•	When: A requests the wallet of Customer B.
•	Then: The system denies access.
US-04: Top Up the Wallet
Requirement ID: FR-4 | Priority: Must
User story: As a customer, I want to top up my wallet by simulated card or agent cash so that I have money available to pay bills.
Acceptance Criteria
Scenario 1: Card top-up
•	Given: A customer has a wallet with an available balance of 100.00 EGP.
•	When: They top up 200.00 EGP with a valid simulated card.
•	Then: The available balance becomes 300.00 EGP and a top-up entry appears in the history.
Scenario 2: Agent cash top-up
•	Given: An agent hands over cash for a customer's wallet.
•	When: The agent submits a top-up of 150.00 EGP for that customer.
•	Then: The customer's wallet is credited with 150.00 EGP and the entry records the agent who made it.
Scenario 3: Invalid amount
•	Given: A customer starts a top-up.
•	When: The amount is zero or negative.
•	Then: The system rejects the top-up and the balance does not change.
Scenario 4: Card declined
•	Given: The simulated card payment is declined.
•	When: The customer submits the top-up.
•	Then: No money is added and the customer is told the card was declined.
US-05: Ledger-Based Balances
Requirement ID: FR-5 | Priority: Must
User story: As a finance team member, I want every balance change recorded as a ledger entry so that balances can always be traced and verified.
Acceptance Criteria
Scenario 1: Entry created for every movement
•	Given: A wallet with a known set of ledger entries.
•	When: A top-up, hold, charge, release, refund, fee, or commission happens.
•	Then: A new ledger entry is created with the amount, type, wallet, reference, and timestamp.
Scenario 2: Balance computed from entries
•	Given: A wallet has entries of +500.00, −100.00, and −50.00.
•	When: The balance is calculated.
•	Then: The available balance is 350.00 EGP, equal to the sum of the entries.
Scenario 3: No direct overwrite
•	Given: A wallet exists.
•	When: Any code path tries to change the balance without creating a ledger entry.
•	Then: The change is not possible, and tests confirm that no balance column is updated directly.
Scenario 4: Entries are not edited
•	Given: A ledger entry exists.
•	When: A correction is needed.
•	Then: A new reversing entry is added and the original entry stays unchanged.
________________________________________
3. Biller Management
US-06: Manage Billers and Services
Requirement ID: FR-6 | Priority: Must
User story: As an administrator, I want to add, edit, and disable billers and services so that I can control what customers can pay.
Acceptance Criteria
Scenario 1: Add a biller
•	Given: The admin is logged in.
•	When: They add a biller with a name, service type, required input fields, and minimum and maximum amounts.
•	Then: The biller is saved and appears in the catalog as active.
Scenario 2: Edit a biller
•	Given: A biller exists.
•	When: The admin changes its minimum amount.
•	Then: The new value is saved and used for later payments.
Scenario 3: Disable a biller
•	Given: An active biller exists.
•	When: The admin disables it.
•	Then: Customers can no longer start payments to it, and its existing payment history is kept.
Scenario 4: Non-admin user
•	Given: A customer is logged in.
•	When: They try to add or edit a biller.
•	Then: The system denies the request.
US-07: Browse Billers and Required Fields
Requirement ID: FR-7 | Priority: Must
User story: As a customer, I want to see the list of billers and the information each one needs so that I know what to enter before paying.
Acceptance Criteria
Scenario 1: List active billers
•	Given: The catalog has active and disabled billers.
•	When: The customer requests the biller list.
•	Then: Only active billers are shown, each with its service type.
Scenario 2: Show required fields
•	Given: A customer selects ElectroCo.
•	When: They open its details.
•	Then: The system shows the required field (meter number) and the minimum and maximum amounts.
Scenario 3: Different biller, different fields
•	Given: A customer selects TopUpNet.
•	When: They open its details.
•	Then: The required field shown is the phone number.
________________________________________
4. Bill Inquiry and Payments
US-08: Bill Inquiry with Fee and Total
Requirement ID: FR-8 | Priority: Must
User story: As a customer, I want to see the bill amount, fee, and total before paying so that I know exactly what I will be charged.
Acceptance Criteria
Scenario 1: Successful inquiry
•	Given: A customer enters a valid meter number for ElectroCo, and the bill is 350.00 EGP.
•	When: They run a bill inquiry.
•	Then: The system shows the bill amount 350.00, the fee 2.50, and the total 352.50 EGP.
Scenario 2: Bill not found
•	Given: The meter number does not exist at the biller.
•	When: The customer runs an inquiry.
•	Then: The system shows a clear "bill not found" message and creates no payment.
Scenario 3: Biller unavailable
•	Given: The biller does not respond.
•	When: The customer runs an inquiry.
•	Then: The system tells the customer to try again later, and no money is moved.
US-09: Pay a Bill from the Wallet
Requirement ID: FR-9 | Priority: Must
User story: As a customer, I want to pay a bill from my wallet so that I don't have to queue at the biller's office.
Acceptance Criteria
Scenario 1: Successful payment
•	Given: A wallet has 1,000.00 EGP available and the bill total is 352.50 EGP.
•	When: The customer confirms the payment and the biller confirms it.
•	Then: The payment is Completed, the wallet is charged 352.50 EGP, and the held balance returns to 0.
Scenario 2: Insufficient funds
•	Given: A wallet has 100.00 EGP and the total is 352.50 EGP.
•	When: The customer confirms the payment.
•	Then: The payment is Rejected with an "insufficient funds" reason and the biller is not called.
Scenario 3: Biller refuses
•	Given: The biller refuses the payment.
•	When: The system receives the refusal.
•	Then: The payment becomes Failed, the hold is released, and the customer is told why.
________________________________________
5. Payment Safety
US-10: Idempotent Payment Requests
Requirement ID: FR-10 | Priority: Must
User story: As a customer, I want a repeated request to be treated as the same payment so that a slow network never charges me twice.
Acceptance Criteria
Scenario 1: Duplicate request
•	Given: A payment was submitted with idempotency key K1 and processed.
•	When: The same request with K1 arrives again.
•	Then: The system returns the original result, and only one payment and one charge exist.
Scenario 2: Simultaneous duplicates
•	Given: Two identical requests with the same key arrive at the same moment.
•	When: Both are processed.
•	Then: Only one payment is created, and both requests receive the same result.
Scenario 3: Same key, different data
•	Given: Key K1 was used for a payment of 350.00 EGP.
•	When: A request with K1 arrives for a different amount or biller.
•	Then: The system rejects it as a key conflict.
Scenario 4: Missing key
•	Given: A payment request has no idempotency key.
•	When: It is submitted.
•	Then: The system rejects it with an error asking for the key.
US-11: Enforced Payment Life Cycle
Requirement ID: FR-11 | Priority: Must
User story: As a support employee, I want every payment to follow the defined life cycle so that its status can always be trusted.
Acceptance Criteria
Scenario 1: Valid transition
•	Given: A payment is in SentToBiller.
•	When: The biller confirms it.
•	Then: The payment moves to Completed.
Scenario 2: Invalid transition
•	Given: A payment is in Completed.
•	When: Any code tries to move it to Failed.
•	Then: The system refuses the change and the state stays Completed.
Scenario 3: Final states
•	Given: A payment is in Completed, Rejected, or Refunded.
•	When: Any further transition is attempted.
•	Then: The system refuses it.
Scenario 4: Transition history
•	Given: A payment moves through several states.
•	When: Support views its history.
•	Then: Every transition is listed with a timestamp.
US-12: Hold Funds Before Calling the Biller
Requirement ID: FR-12 | Priority: Must
User story: As a customer, I want my money held before the biller is called and released if the payment fails so that I am never charged for a payment that did not happen.
Acceptance Criteria
Scenario 1: Funds held first
•	Given: A wallet has 1,000.00 EGP and passes the fraud checks.
•	When: A payment of 352.50 EGP starts.
•	Then: The available balance becomes 647.50, the held balance becomes 352.50, and only then is the biller called.
Scenario 2: Hold released on failure
•	Given: A payment is Failed after the biller refused it.
•	When: The system processes the failure.
•	Then: The 352.50 EGP is returned to the available balance, the held balance returns to 0, and the payment becomes Refunded.
Scenario 3: Balance never negative
•	Given: Two payments of 800.00 EGP arrive at the same time on a wallet with 1,000.00 EGP.
•	When: Both are processed.
•	Then: One succeeds, the other is Rejected, and the balance never goes below zero.
US-13: Handle Biller Timeouts
Requirement ID: FR-13 | Priority: Must
User story: As a customer, I want a slow biller response to be handled safely so that I am not charged wrongly or refunded wrongly.
Acceptance Criteria
Scenario 1: Timeout becomes Unknown
•	Given: A payment is SentToBiller and the biller takes 12 seconds to answer (the timeout is 10 seconds).
•	When: The timeout is reached.
•	Then: The payment becomes Unknown, the money stays held, and the customer is told the payment is being processed.
Scenario 2: Re-query schedule
•	Given: A payment is Unknown.
•	When: 1, 5, and 15 minutes pass.
•	Then: The system re-queries the biller at each of those times, up to 3 times.
Scenario 3: Later confirmation
•	Given: A payment is Unknown.
•	When: A re-query shows the biller received the payment.
•	Then: The payment becomes Completed and the hold becomes a final charge.
Scenario 4: No automatic refund
•	Given: A payment is Unknown and all 3 re-queries gave no answer.
•	When: Time passes.
•	Then: The payment stays Unknown and held until reconciliation or the biller confirms the result, and it is never refunded automatically.
US-14: Asynchronous Callbacks with Duplicate Protection
Requirement ID: FR-14 | Priority: Must
User story: As a customer, I want TopUpNet's delayed result to be applied exactly once so that my top-up is not completed or charged twice.
Acceptance Criteria
Scenario 1: Success callback
•	Given: A TopUpNet payment is SentToBiller after TopUpNet replied "accepted".
•	When: The callback arrives with "success".
•	Then: The payment becomes Completed.
Scenario 2: Failed callback
•	Given: A TopUpNet payment is waiting for a result.
•	When: The callback arrives with "failed".
•	Then: The payment becomes Failed and the hold is released.
Scenario 3: Duplicate callback
•	Given: A payment is already Completed from a "success" callback.
•	When: A second "success" callback arrives.
•	Then: The payment is not changed, no second charge or fee is made, and the duplicate is logged.
Scenario 4: Unknown reference
•	Given: A callback arrives with a reference that does not match any payment.
•	When: The system receives it.
•	Then: It is rejected and logged, and no payment changes.
________________________________________
6. Biller Integrations
US-15: Support Billers with Different Formats
Requirement ID: FR-15 | Priority: Must
User story: As a PayLink manager, I want the system to work with billers that use different protocols so that customers can pay many kinds of bills.
Acceptance Criteria
Scenario 1: ElectroCo (REST/JSON)
•	Given: ElectroCo is active.
•	When: A customer pays an electricity bill.
•	Then: The system sends a JSON request, receives an immediate confirmation, and completes the payment.
Scenario 2: AquaCo (XML)
•	Given: AquaCo is active.
•	When: A customer pays a water bill.
•	Then: The system sends an XML request, converts AquaCo's fields and error codes into PayLink's own format, and handles the 2 to 4 second reply.
Scenario 3: TopUpNet (asynchronous)
•	Given: TopUpNet is active.
•	When: A customer buys a top-up.
•	Then: The system handles the "accepted" reply and waits for the later callback.
Scenario 4: Biller outage isolated
•	Given: AquaCo is down.
•	When: A customer pays an ElectroCo bill.
•	Then: The ElectroCo payment completes normally.
Scenario 5 (optional): NetCo batch
•	Given: NetCo is active and payments are waiting.
•	When: The daily batch runs.
•	Then: A CSV file is uploaded and the next morning's result file updates each payment.
________________________________________
7. Fees and Commissions
US-16: Calculate Fees
Requirement ID: FR-16 | Priority: Must
User story: As a customer, I want the correct fee to be calculated so that I only pay what the rules say.
Acceptance Criteria
Scenario 1: Fixed fee
•	Given: An electricity or water payment of any amount.
•	When: The fee is calculated.
•	Then: The fee is 2.50 EGP.
Scenario 2: Percentage fee
•	Given: A mobile top-up of 100.00 EGP, then one of 20.00 EGP.
•	When: The fee is calculated.
•	Then: The fee is 1.50 EGP for the first (1.5%) and 1.00 EGP for the second (the minimum, since 1.5% would be 0.30).
Scenario 3: Tiered fee
•	Given: An internet bill of 200.00 EGP, then one of 200.01 EGP.
•	When: The fee is calculated.
•	Then: The fee is 2.00 EGP for the first and 4.00 EGP for the second.
Scenario 4: Promotion
•	Given: A promotion is set for one biller from a start date to an end date.
•	When: A payment to that biller is made inside, and then outside, the period.
•	Then: The fee is 0.00 EGP inside the period and the normal fee outside it.
Scenario 5: Exact decimals
•	Given: Any fee calculation.
•	When: The result is computed.
•	Then: The value is exact to two decimal places, with no floating-point error.
US-17: Agent Commission
Requirement ID: FR-17 | Priority: Should
User story: As an agent, I want to pay bills on behalf of customers and earn a commission so that I am rewarded for serving them.
Acceptance Criteria
Scenario 1: Agent payment completes
•	Given: An agent pays a bill for a customer, and the service fee is 2.50 EGP.
•	When: The payment is Completed.
•	Then: 1.00 EGP (40% of the fee) is credited to the agent's wallet and PayLink keeps the remaining 1.50 EGP.
Scenario 2: Payment fails
•	Given: An agent-assisted payment becomes Failed.
•	When: The failure is processed.
•	Then: No commission is paid.
Scenario 3: Customer payment without an agent
•	Given: A customer pays directly in the app.
•	When: The payment completes.
•	Then: No commission is recorded.
Scenario 4: Zero fee
•	Given: A promotion makes the fee 0.00 EGP.
•	When: An agent-assisted payment completes.
•	Then: The commission is 0.00 EGP.
________________________________________
8. Fraud and Limits
US-18: Payment and Daily Limits
Requirement ID: FR-18 | Priority: Must
User story: As a PayLink manager, I want payments over the limits to be rejected with a clear reason so that the platform stays safe.
Acceptance Criteria
Scenario 1: Above single-payment maximum
•	Given: A customer tries to pay 10,000.01 EGP.
•	When: The payment is submitted.
•	Then: The payment is Rejected with the reason "above maximum single payment".
Scenario 2: Below minimum
•	Given: A customer tries to pay 4.99 EGP.
•	When: The payment is submitted.
•	Then: The payment is Rejected with the reason "below minimum payment".
Scenario 3: Basic daily limit
•	Given: A basic customer has already paid 4,800.00 EGP today.
•	When: They try to pay 300.00 EGP more.
•	Then: The payment is Rejected with the reason "daily limit exceeded".
Scenario 4: Verified daily limit
•	Given: A verified customer has paid 4,800.00 EGP today.
•	When: They pay 300.00 EGP more.
•	Then: The payment is accepted, since the limit is 30,000 EGP.
Scenario 5: No money moved
•	Given: A payment is Rejected by a limit.
•	When: The rejection is complete.
•	Then: No hold is made and the biller is not called.
US-19: Velocity Rule
Requirement ID: FR-19 | Priority: Should
User story: As a PayLink manager, I want accounts that make too many payments too quickly to be blocked so that fraud and abuse are stopped early.
Acceptance Criteria
Scenario 1: Within the limit
•	Given: An account makes 5 payments within 60 seconds.
•	When: The fifth payment is processed.
•	Then: All 5 are processed normally.
Scenario 2: Limit exceeded
•	Given: An account has made 5 payments in the last 60 seconds.
•	When: A sixth payment is submitted.
•	Then: The payment is Rejected and the account is blocked for 10 minutes.
Scenario 3: Block expires
•	Given: An account was blocked by the velocity rule.
•	When: 10 minutes have passed.
•	Then: The account can make payments again.
Scenario 4: During the block
•	Given: An account is blocked.
•	When: It tries to pay.
•	Then: The payment is Rejected with the reason "account blocked".
________________________________________
9. Support and Administration
US-20: Search Payment by Reference
Requirement ID: FR-20 | Priority: Must
User story: As a support employee, I want to search for a payment by its reference and see its full history so that I can answer customer complaints.
Acceptance Criteria
Scenario 1: Payment found
•	Given: A payment with reference PL-1001 exists.
•	When: Support searches for PL-1001.
•	Then: The system shows its current state, amounts, biller, customer, and every state transition with timestamps.
Scenario 2: Payment not found
•	Given: No payment has the searched reference.
•	When: Support searches for it.
•	Then: The system shows a "not found" message.
Scenario 3: Unauthorized user
•	Given: A customer is logged in.
•	When: They try to use the support search.
•	Then: The system denies access.
US-21: Block and Unblock Accounts
Requirement ID: FR-21 | Priority: Should
User story: As a support employee, I want to block and unblock accounts so that I can stop suspicious activity and restore normal accounts.
Acceptance Criteria
Scenario 1: Block
•	Given: An active customer account.
•	When: Support blocks it and enters a reason.
•	Then: The account is blocked and later payments are Rejected.
Scenario 2: Unblock
•	Given: A blocked account.
•	When: Support unblocks it.
•	Then: The customer can pay again.
Scenario 3: Audit
•	Given: Support blocks or unblocks an account.
•	When: The action completes.
•	Then: The audit log records who did it, when, and why.
US-22: Edit Fees and Limits Without Redeploying
Requirement ID: FR-24 | Priority: Should
User story: As an administrator, I want to change fee and limit values without redeploying so that business rules can change quickly and safely.
Acceptance Criteria
Scenario 1: Change a limit
•	Given: The basic daily limit is 5,000 EGP.
•	When: The admin changes it to 6,000 EGP.
•	Then: New payments use 6,000 EGP immediately, with no redeploy.
Scenario 2: Change a fee
•	Given: The fixed electricity fee is 2.50 EGP.
•	When: The admin changes it to 3.00 EGP.
•	Then: New inquiries show the 3.00 EGP fee, and payments already in progress keep their original fee.
Scenario 3: Invalid value
•	Given: The admin enters a negative fee.
•	When: They save it.
•	Then: The system rejects it and keeps the old value.
Scenario 4: Audit
•	Given: The admin saves a change.
•	When: The change is applied.
•	Then: The audit log stores the old value, new value, user, and time.
US-23: Audit Log
Requirement ID: FR-25 | Priority: Must
User story: As a finance team member, I want every money movement and admin action recorded in an audit log so that anything can be traced and proven.
Acceptance Criteria
Scenario 1: Money movement
•	Given: Any top-up, hold, charge, release, fee, commission, or refund happens.
•	When: It completes.
•	Then: An audit record is saved with who, when, what, and why.
Scenario 2: Admin action
•	Given: An admin edits a biller, fee, or limit.
•	When: The change is saved.
•	Then: An audit record is saved with the user and the old and new values.
Scenario 3: Full coverage
•	Given: A test run with many money movements.
•	When: Audit records are compared with ledger entries.
•	Then: 100% of movements have an audit record.
Scenario 4: Records protected
•	Given: An audit record exists.
•	When: Anyone tries to edit or delete it through the application.
•	Then: The system does not allow it.
________________________________________
10. Notifications
US-24: Payment Notifications
Requirement ID: FR-22 | Priority: Must
User story: As a customer, I want an SMS and a push notification when my payment completes or fails so that I always know the result.
Acceptance Criteria
Scenario 1: Completion
•	Given: A payment becomes Completed.
•	When: The completion is recorded.
•	Then: The customer receives an SMS and a push notification with the amount, biller, and reference.
Scenario 2: Failure
•	Given: A payment becomes Failed.
•	When: The failure is recorded.
•	Then: The customer receives an SMS and a push notification with a clear reason.
Scenario 3: Notification failure
•	Given: The SMS provider is down when a payment completes.
•	When: The system tries to send the SMS.
•	Then: The payment still stays Completed.
US-25: Retry Failed Notifications
Requirement ID: FR-23 | Priority: Should
User story: As a customer, I want failed notifications to be retried so that I still get my receipt when the provider recovers.
Acceptance Criteria
Scenario 1: Retry then success
•	Given: An SMS fails on the first attempt.
•	When: A retry succeeds.
•	Then: The notification is marked delivered and no more retries are made.
Scenario 2: All retries fail
•	Given: An SMS fails on the first attempt and on all 3 retries.
•	When: The third retry fails.
•	Then: The notification is marked "undelivered" and the payment is not affected.
Scenario 3: Retry limit
•	Given: A notification has been retried 3 times.
•	When: The system checks it.
•	Then: No fourth retry is made.
________________________________________
11. Reconciliation and Reporting
US-26: Daily Reconciliation Report
Requirement ID: FR-26 | Priority: Should
User story: As a finance team member, I want PayLink's payments compared with the biller's settlement file every night so that mismatches are found and reviewed.
Acceptance Criteria
Scenario 1: Everything matches
•	Given: A settlement file lists exactly the payments PayLink has as Completed.
•	When: The reconciliation runs.
•	Then: The report shows zero differences.
Scenario 2: Biller has a payment PayLink marked Failed
•	Given: The settlement file lists a payment that PayLink has as Failed.
•	When: The reconciliation runs.
•	Then: The difference is flagged in the report for support to review, and no money moves automatically.
Scenario 3: PayLink has a payment the biller does not
•	Given: PayLink has a Completed payment that is missing from the file.
•	When: The reconciliation runs.
•	Then: The payment is flagged as missing at the biller.
Scenario 4: Unknown payments resolved
•	Given: A payment is Unknown and the settlement file lists it.
•	When: The reconciliation runs.
•	Then: The payment becomes Completed. If the file does not list it, the payment becomes Failed.
Scenario 5: Invalid file
•	Given: The settlement file is malformed.
•	When: The reconciliation runs.
•	Then: The run stops with a clear error and no payment is changed.
US-27: Daily Totals Dashboard
Requirement ID: FR-28 | Priority: Could
User story: As an administrator, I want to see daily totals so that I can monitor the business.
Acceptance Criteria
Scenario 1: View totals
•	Given: Payments were made on a given day.
•	When: The admin requests that day's totals.
•	Then: The system shows the number and value of payments, fees earned, commissions paid, and failures per biller.
Scenario 2: Correct numbers
•	Given: A day has 3 Completed payments with 2.50 EGP fees each, and 1 Failed payment.
•	When: The totals are displayed.
•	Then: Fees earned are 7.50 EGP and failures are 1.
Scenario 3: No payments
•	Given: No payments were made on the selected day.
•	When: The admin requests the totals.
•	Then: The system shows zeros and no error.
US-28: Request and Approve a Refund
Requirement ID: FR-27 | Priority: Could
User story: As a customer, I want to request a refund of a completed payment, and have support approve it, so that I can recover money paid by mistake.
Acceptance Criteria
Scenario 1: Request
•	Given: A customer has a Completed payment.
•	When: They submit a refund request with a reason.
•	Then: The request is saved as "pending" and support is notified.
Scenario 2: Approval
•	Given: A refund request is "pending" for a Completed payment.
•	When: Support approves it.
•	Then: The system adds a new ledger entry that credits the refunded amount to the customer's wallet, marks the refund request as "approved," and notifies the customer. The payment stays in the Completed state, and the audit log records who approved it, when, and why.
Scenario 3: Rejection
•	Given: A refund request is "pending."
•	When: Support rejects it with a reason.
•	Then: No money moves, the refund request is marked "rejected," the payment stays Completed, and the customer is told why.
Scenario 4: Payment not eligible
•	Given: A payment is Failed, Rejected, or Unknown.
•	When: The customer requests a refund.
•	Then: The request is refused, because these payments are handled by the normal failure flow.

1.4 Measurable Non-Functional Requirements
NFR-1: Correctness
•	Description: Prevent duplicate charges and negative balances, even when the same request is sent twice or two payments arrive at the same moment.
•	Measurable target: Zero double charges and zero negative balances in the duplicate-request and concurrency tests.
•	Verification: Automated tests for hard cases 1 and 4. One test sends the same idempotency key 50 times in parallel and checks that exactly 1 payment and 1 charge exist. Another sends 100 simultaneous payments against a wallet that can afford only one and checks that exactly 1 succeeds, 99 are Rejected, and the balance never goes below 0.00. Both run in CI on every push.
NFR-2: Performance
•	Description: The system must handle the busiest day of the month by processing payments at a high, steady rate.
•	Measurable target: At least 100 payments per second sustained for 1 minute against the mock billers, with an error rate below 1%. 95% of internal API requests (balance, biller list, fee calculation) complete in under 500 ms.
•	Verification: A load test (for example k6 or Locust) runs for 60 seconds at 100 requests per second. The report shows at least 6,000 completed payments, the error rate, and the 95th percentile latency per endpoint.
NFR-3: Resilience
•	Description: A problem with one biller must not stop payments to the others, and slow billers must be handled safely.
•	Measurable target: While one biller is completely down, payments to the other billers keep a success rate of at least 99%. Every biller call that takes longer than 10 seconds becomes Unknown within 10.5 seconds, with the money still held and 0 automatic refunds.
•	Verification: A test shuts down the AquaCo mock and sends 200 ElectroCo payments, then checks the success rate. A second test (hard case 2) uses a mock ElectroCo that answers after 12 seconds and checks the payment state, the held balance, and the absence of a refund.
NFR-4: Data Integrity
•	Description: Every balance must be calculated from ledger entries, all money must use exact decimal types, and payments may only follow the life cycle in section 2.5.
•	Measurable target: 0 differences between any wallet balance and the sum of its ledger entries. 0 floating-point money fields in code and database. 100% of invalid state transitions refused, including all changes from final states.
•	Verification: A consistency check runs after the integration and load tests and compares each wallet's balance with its ledger sum. A lint rule or code search fails the build if a float type is used for money. A parameterized unit test tries all 64 state pairs (8 × 8) and checks that only the allowed transitions succeed.
NFR-5: Security
•	Description: Each role may only use the functions it is allowed to use, and sensitive data must be protected.
•	Measurable target: 100% of admin and support endpoints reject customer tokens with a 403 response. 0 successful reads of another customer's wallet. 0 plain-text passwords in the database, 0 secrets in the repository, and 0 passwords or tokens in logs.
•	Verification: An automated authorization test calls every protected endpoint with each role (customer, agent, support, admin) and checks the status codes. A secret-scanning tool (for example gitleaks) runs in CI, and a database check confirms that passwords are hashed.
NFR-6: Auditability
•	Description: Every money movement and admin action must leave a record showing who did it, when, what, and why, so that support and finance can trace any payment.
•	Measurable target: 100% of ledger entries and admin changes have an audit record with all four fields filled. A payment search by reference returns its full history in under 1 second.
•	Verification: After the integration tests, a query compares ledger entries and admin actions with audit records and fails if any are missing or incomplete. A test pays through several states and checks that every transition is stored with a timestamp, and the search time is measured under load.
NFR-7: Modifiability
•	Description: Adding a new biller or changing a biller's API must only affect the Biller Integration module and configuration, and business rules must live in configuration, not in code.
•	Measurable target: Adding a biller, and applying the ElectroCo v2 change, changes 0 files in other modules. 100% of the values in section 2.6 (limits, fees, timeouts, retries, velocity rule, promotion dates) can be changed without redeploying, and 0 are hard-coded.
•	Verification: A git diff of each change is checked in the pull request, and the final report lists the changed files. A test changes a limit and a fee through the admin API and checks that the next request uses the new values.
NFR-8: Testability and Deployability
•	Description: The domain logic must be well tested, and the full system must be easy to build, deploy, and roll back from a clean clone.
•	Measurable target: At least 70% line coverage on domain logic, measured in CI, with at least 1 automated test for each of the 8 hard cases. The full stack (application, database, mock billers, broker) starts with 2 commands or fewer and reports healthy within 3 minutes. A rollback to the previous version completes in under 5 minutes.
•	Verification: The pipeline generates a coverage report and fails the build if coverage is below 70%. A traceability table maps each hard case to its test. A teammate clones the repository on a clean machine, follows the README, and times the steps. The pipeline deploys on every push to main, runs the health check, and the rollback step is tested once and documented.


