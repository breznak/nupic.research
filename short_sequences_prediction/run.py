#!/usr/bin/env python

# run python run.py
# reads ./data.csv
# train model on algebraic (for now only '+') expressions,
# should demonstrate 
# (1) HTM capability for learning many short sequences 
# (2) "transfer", create onderstanding of numbers and '+' operation
# (3) able to "compute" unmet expression
# FIXME performance even on training sequences is very bad!?

import csv
import re
import random

from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.data import SENTINEL_VALUE_FOR_MISSING_DATA as NA_VALUE
import model_params
from nupic.utils import MovingAverage

_PRED_FIELD = 'number'
DATAFILE = './data.csv'
AHEAD = 1 # 1 step

# num = 0..100
# op = N/A, '+'

def _format(inference, sample):
  s = ""
  inf = int(round(inference['multiStepBestPredictions'][AHEAD]))
  s += "best=%i %s\tconfidences: " % (inf, "OK" if inf == sample[2] else "WRONG")
  inf = inference['multiStepPredictions'][AHEAD]
  for k in inf.keys():
    s += (" %i: %.4f, " % (round(k), float(inf[k])))
  return s

def train(testset=[]):
  # create model
  model = ModelFactory.create(model_params.MODEL_PARAMS)
  model.enableInference({'predictedField': _PRED_FIELD})
  model.enableLearning()

  avg = MovingAverage(500)

  with open(DATAFILE, 'r') as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    for row in reader:
      i += 1
      sample = (int(row[0]), int(row[1]), int(row[2]))
      (model, result) = runSingleExample(model, sample)
      # accuracy
      best = int(round(result.inferences['multiStepBestPredictions'][AHEAD]))
      if best == sample[2]:
        avg.next(1)
      else:
        avg.next(0)
      if (random.randint(0,10000) % 100) == 0:
        print "[%i]\t %s ==> acc=%.2f  %s" % (i, sample, avg.getCurrentAvg(),  _format(result.inferences, sample))

  model.disableLearning()
  return model


def test(model, testset):
  """feed startSent sequence and then continue to generate the story by the CLA. 
    param model: the trained CLA model
    param startSent: starting sequence as a string, eg \"And so he raised the gun\" 
    param lenght: #sequences to generate. """
  model.disableLearning()
  for s in testset:
    print "testing on ", s
    (_, result) = runSingleExample(model, s)
    print _format(result.inferences, s)


def runSingleExample(model, sample):
  (arg1, arg2, res) = sample
  try:
    model.run({'number': arg1})
    result = model.run({'number': arg2}) # predictions stored from here
    if res is not None:
      model.run({'number': res})
  except:
    print sample
    raise
  model.resetSequenceStates() #FIXME with or without - performance is low. Speed much higher when reseting on each new seq.
  return (model, result)

###################################################################
if __name__ == "__main__":
    testset = [(2,1,3), (4,2,6)]
    print "training..." 
    model = train(testset)
    print('==========================================')
    print "testing on: ", testset
    test(model, testset)
