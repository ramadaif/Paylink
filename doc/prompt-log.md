//first prompt
| Date | Author | Stage | Tool | Prompt | Answer | Verdict |
|---|---|---|---|---|---|---|
| 25 Nov | Rama | CI | Claude | write a github actions workflow for my fastapi project, on every push install requirements, run ruff, run pytest, build the docker image | workflow with the 4 steps, runs on push only | fixed, I used my own file and added pull_request so PRs get checked too 

| 25 Nov | Rama | Docker | Claude | write a docker-compose for my fastapi app and postgres 16, app should wait for the db to be healthy | app and db with a db healthcheck | Accepted: it matched what the project needs, The pg_isready healthcheck and the wait for a healthy database are correct

//second prompt
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
