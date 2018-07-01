# judge

This module is the judge for my AWS Game

It awards marks for AWS implementation, not for applications or for code


## Criteria

### Scalability of the infrastructure

This is measured as 

#### (#instances in ASGs where min, des and max are identical) x100
#### --------------------------------------------------------------
#### (#instances in ASGs where min, des and max are not identical)

### serverlessness

This is measured as 

#### (Number of serverless workloads) x100
#### -------------------------------------
####      (Total number of workloads)

