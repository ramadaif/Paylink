//first prompt
Write all posible Non-functional Requirements with this structure
For each NFR:
* Give it an ID.
* Write its description.
* Define its measurable target.
* Explain how you will verify or measure it.
Don't use vague statements such as "the system should be fast" or "the system should be secure."
Use measurable conditions wherever possible.
use this as an example:
NFR-1: Correctness	 [Requirement] Prevent duplicate charges and negative balances		[Measurable target] Zero double charges and zero negative balances in duplicate and concurrency tests

//second prompt
You are a software architect. We are building PayLink, a bill-payment backend
like Fawry, where customers pay electricity, water, mobile and internet bills
from a wallet. I attached the project brief and our requirements.

Please write the design pack as PlantUML files, one file per diagram:
1. Use-case diagram
2. Domain class diagram
3. Sequence diagram for paying a bill
4. Sequence diagram for refunding a failed payment
5. State diagram of the payment
6. ER diagram of the database (at least 10 tables)

Rules:
- Use only the payment states and transitions from the brief.
- A payment in Unknown is never refunded automatically.
- The wallet has no balance field; balances come from ledger entries.
- Money uses exact decimals, never float.
- All diagrams must use the same names and states.

//third prompt (wrong)
Create UML diagrams for a Bill Payment System. Include a Use Case Diagram, Class Diagram, and ER Diagram. Show the main users, system functions, classes, and database relationships.
the problems was:I didn't provide enough details about the system requirements. I only asked for the main UML diagrams without explaining the payment process, business rules, or relationships between the system components.
Because of that, the AI had to make some assumptions, which could lead to incorrect relationships and missing details in the diagrams. so i reviewed them and changed the prompt

// fourth prompt (wrong)
Write user stories for all the functional requirements of the PayLink system. Include acceptance criteria and priorities for each story.
the problem was:The prompt didn't explain that all user stories must follow the payment life cycle in Section 2.5. As a result, the AI wrote an incorrect refund scenario where a Completed payment could become Refunded.
How I improved the prompt:I added a constraint asking the AI to follow the payment life cycle and identify any conflicts between the requirements instead of making assumptions.

//fifth prompt 
Rewrite Scenario 2 of US-28. Make sure that when the admin approves a refund, the money is added to the customer's wallet, the refund request is marked as Approved, and the customer is notified. The payment status must remain Completed.
Use Given/When/Then format.
