# judge

This module is the judge for my AWS Game

It awards marks for AWS implemntation, not for applications or for code


## Criteria

### Scalability of tyhe infrastructure

This is measured as 

(#instances in ASGs where min, des and max are identical) x100
--------------------------------------------------------------
 (#instances in ASGs where min, des and max are not identical)


