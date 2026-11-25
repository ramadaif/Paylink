
| Date | Author | Stage | Tool | Prompt | Answer | Verdict |
|---|---|---|---|---|---|---|
| 25 Nov | Rama | CI | Claude | write a github actions workflow for my fastapi project, on every push install requirements, run ruff, run pytest, build the docker image | workflow with the 4 steps, runs on push only | fixed, I used my own file and added pull_request so PRs get checked too 

| 25 Nov | Rama | Docker | Claude | write a docker-compose for my fastapi app and postgres 16, app should wait for the db to be healthy | app and db with a db healthcheck | Accepted: it matched what the project needs, The pg_isready healthcheck and the wait for a healthy database are correct
