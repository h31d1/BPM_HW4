# Business Process Mining
## Homework 4: Predictive process monitoring

Preprocessed event log: [BPIC15](https://owncloud.ut.ee/owncloud/index.php/s/8DC9KXyTnJWNRgJ/download/HW4-BPIC15.csv) 

Aim: to train and use predictive process monitoring techniques to predict the outcome of a process from a log of events. 

Framework: by [Teinemaa et al.](https://github.com/Mcamargo85/predictive-monitoring-benchmark.git)

Tasks:

1. (2 points) As part of the log preprocessing, it is necessary to **categorize** the process traces as _deviant_ or _regular_. A case is deviant if its duration is greater than the mean case duration of the log by 10% (i.e., mean-case-duration * 1.10). Otherwise, the case is regular. You must create a new column in the log that contains a case attribute called **label** that must take a value of 1 for deviant cases or 0 for **regular** ones.
2. (2 points) Add a column to the event log that describes the **WIP** of the process in each event. Remember that the WIP refers to the number of active cases that have started but not been completed.
3. (3 points) Given the WIP column in Task 2 and the outcome (label) in Task 1, **train** an **XGboost** and a **Random Forest** models using single bucketing and combined encoding.
4. (3 points) Repeat Task 3 **without the WIP column**. 
  - Compare the resulting models with the previous step and explain the differences in the results. 
  - Did the use of the WIP attribute affect the accuracy of the models? If so, explain why this effect can occur.

Submission: 
- A **report** in **PDF** format containing the _explanation_ of the modifications made to the approach, the _evaluation_ of the changes, and the link to a repository. You must submit this document via the Submit link on the course website.
- A **repository** containing the made changes. 

## Files

Folders `bucketer` and `transformers` and files `BucketFactory.py` and `EncoderFactory.py` are lended from framework by Teinemaa.

Functions in file `preprocesses.py` are collected from practice session notebooks.

**Solution** of the homework can be found in notebook `hw4_notebook_hc.ipynb`.