#!/bin/env python

# tool to generate data - algebraic examples ( 1 + 2 = 3 )
# python generateData numSamples argsMin argsMax method repeates
# eg. python generateData 2000 0 5 "random" 5 ...and creates data.csv

import csv
import sys
import random

OUTFILE = "./data.csv"

def generateExample(start=0, stop=10, skiptest=[], method="random", repeat=1):
  """
  generate 1 example as training data

  @return triplet (x,y,x+y) or None if generated sample is in 'skiptest' used for testing
  """
  if method == "random":
    return _generateExampleRand(start, stop, skiptest)
  elif method == "sequential":
    return _generateExampleSeq(start, stop, skiptest)
  else:
    raise ValueError("GenerateData: unknow method %s" % method)


n1=None
n2=None
def _generateExampleSeq(start, stop, skipset):
  global n1
  global n2
  if n1 is None:
    n1 = start
  if n2 is None:
    n2 = start - 1 # because (n2 += 1) below

  n2 += 1 # iterate

  if n2 > stop:
    n2 = start
    n1 += 1
  if n1 > stop:
    n1 = start

  ## skip test sample
  for (s1,s2,_) in skipset:
    if (n1 == s1 and n2 == s2): #TODO checks only A+B, not B+A
      return None

  return (n1, n2, n1 + n2)


def _generateExampleRand(start, stop, skipset):
  num1 = random.randint(start, stop)
  op = '+'
  num2 = random.randint(start, stop)
  if op == '+':
    res = num1 + num2

  ## skip test sample
  for (s1,s2,_) in skipset:
    if (num1 == s1 and num2 == s2):
      return None

  ex = (num1, num2, res)
  return ex



if __name__ == "__main__":
  args = sys.argv[1:]
  print "args:", args
  # parse args
  nSamples = int(args[0])
  argMin = int(args[1])
  argMax = int(args[2])
  met = str(args[3])
  repeat = int(args[4])

  # define test set
  testset = [(1,1,None), (3,4, None)]

  
  with open(OUTFILE, 'w') as csvfile:
    writer = csv.writer(csvfile)
    i = 0
    while i < nSamples:
      ex = generateExample(argMin, argMax, testset, met)
      if ex is None:
        continue # skip test-set samples
      for _ in xrange(repeat):
#        print ex
        writer.writerow(ex)
      i += 1
