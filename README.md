# Audit-AWS

This is the repo for our AWS Game

# Description

Every product team can choose whether they are confident enough to be audited or not. If they are, then they allow read-only access to the (internal only) auditors for 48 hours. During this time the auditors will take a snapshot of the team’s AWS configuration and associated repos. They will then run scripts against the snapshot to mark the configuration out of 100. All scripts and marks will then be published.
*Only teams who volunteer will be audited and only their AWS infrastructure and code.*
 
## Approach

There are a few ways of gathering the data and a few ways of mining it. For example:
- Use the existing state file

   This is neat, because the data is already there and always available

   but holy crap its hard slog to parse it, every env for every product team will have thousands of lines of JSON to wade through

- Whip up some bash scripts to use the CLI

   Quick and painless to develop

   but it forces us to use JSON and is impractical unless run locally, which implies lots of role-switching, which seems a bit dumb

   it will also inevitably lead to IAM problems and life is too short for this type of pain

- Write the data-gathering as a shared lambda, then teams can run it themselves

   hmmm seems to be a decent option. We'd be able to choose what we looked at and choose an appropriate output format and location

   we'd also need to write custom code to mine the data, either that or drag it into Excel as a CSV

## Criteria

Here are some possible criteria. I suggest we pick the ones that will be simplest to code. Any others that look interesting
can go onto a backlog.
 
| Criteria | Description | Metric
|---|---|---
| Security | Does the code follow AWS' security best practices | ? |
| Scalability | Do the instances scale up and down | % of instances in ASGs |
| Reliability | The inbuilt AWS reliability features are utilised | % of AZs that are used |
| Tagged | ? | ? 
| IaC | ? | ? 
| Standards conformance | ? | ? 
| UptoDateness | ? | ? 
| Documentation | ? | ? 
| Supportability | ? | ? 
| CostEfficiency | ? | ? 
| Serverlessness | ? | ? 
| RightSizedness | ? | ? 
| Elegance | ? | ? 
| DRability | ? | ? 

## Actors

At the moment the vteam of auditors consists of 
- virtual mikec
- virtual ginge
- virtual dand
