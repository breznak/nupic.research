# Algebraic

Demonstration of HTM performing (basic) arithmetic operations (currently '+' only), on N numbers. 

## Goals

* can HTM express arithmetic operations? 
* can develop 'sense' for natural numbers? Eg. 1 < 2 << 6, or 1+2=3
* does "transfer" happen? Able to answer unmet expression? 
* simulate different strategies for teaching algebra

## Run

1. Generate data: `python generateData.py 2000 0 5 "random" 5`
2. (you can see `./data.csv` created)
3. Run model: `python run.py`

## Problems

- performance for learning sequences is very low
  - do/do not call `sequenceReset()` after each sequence? 
    - better speed with reset
    - similar (low) performance
  - have I missed some setting in model/experiment that causes the problem?
  - does CLA have issue with learning `very short` sequences?


