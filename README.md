[![forthebadge](https://forthebadge.com/images/badges/made-with-crayons.svg)](https://forthebadge.com)

# Audit-AWS

This is the repo for our AWS Game

# Description

Every product team can choose whether they are confident enough to be audited or not. If they are, then they allow read-only access to the (internal only) auditors for 48 hours. During this time the auditors will take a snapshot of the team’s AWS configuration and associated repos. They will then run scripts against the snapshot to mark the configuration out of 100. All scripts and marks will then be published.
*Only teams who volunteer will be audited and only their AWS infrastructure and code.*
 
## Approach

There are a few ways of gathering the data and a few ways of mining it. For example:
- Use the existing state file

   This is neat, because the data is already there and always available

   but holy crap it's a hard slog to parse it; every environment for every product team will have *thousands* of lines of JSON to wade through

- Whip up some bash scripts to use the CLI locally

   Quick and painless to develop

   but it forces us to use JSON and it implies lots of role-switching, which seems a bit dumb

   it will also inevitably leads to IAM problems and life is too short for this type of pain

- Whip up a CLI script to run on an existing host e.g. a transit host or jumpbox

   Quick and painless to develop

   Dumb. Painful to implement and to support

- Write the data-gathering as a shared lambda, then competitor teams can run it themselves

   hmmm seems to be a decent option. We'd be able to choose what we looked at and choose an appropriate output format and location

   we'd also need to write custom code to mine the data, either that or drag it into Excel as a CSV

## Criteria for v1

| Metric Name | Description | Possible Calculation
|---|---|---
| Security | Does the code follow AWS' security best practices. What are these? | % practices followed
| Scalability | The instances scale up and down | % of instances in ASGs where the des is less than max?
| Reliability | The inbuilt AWS reliability features are utilised | % of instances that are in 3-AZ ASGs?
| Tagged | Taggable resources have RI standard tags | % of tags in place and correct
| Serverlessness | Code is run serverless | % of workloads that COULD be servless that actually ARE serverless
| DRability | Critical/sensitive data is copied to another region | % of Production stores in multiple regions? 

## Criteria backlog

| Metric Name | Description | Possible Calculation
|---|---|---
| IaC | The infra is in Terraform | % of discovered resources formed by Terraform | ?
| Standards conformance | Sounds good, but we don't actually have standards | n/a
| Elegance | ? | ? 
| CostEfficiency | ? | ? 
| RightSizedness | The instance types are correct | ? 
| UptoDateness | The Code is running up to date (major version only) of software | ?
| Supportability | ? | ? 
| Documentation | Every component is documented | ?
| Interoperability | Can the code be run on another errrr  something? | 

## Actors

At the moment the vteam of auditors consists of 
- virtual mikec
- virtual ginge
- virtual dand

## Design

![pic](https://github.com/RIMikeC/Audit-AWS/blob/master/images/Picture1.png)
