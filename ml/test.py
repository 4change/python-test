#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# import numpy as np
# import matplotlib.pyplot as plt

# %matplotlib inline

# import pandas as pd

from sklearn import tree
from sklearn2pmml.pipeline import PMMLPipeline
from sklearn2pmml import sklearn2pmml

import os

os.environ["PATH"] += os.pathsep + '/usr/local/jdk1.8.0_181/bin'

X = [[1, 2, 3, 1], [2, 4, 1, 5], [7, 8, 3, 6], [4, 8, 4, 7], [2, 5, 6, 9]]
y = [0, 1, 0, 2, 1]
pipeline = PMMLPipeline([("classifier", tree.DecisionTreeClassifier(random_state=9))]);
pipeline.fit(X, y)

sklearn2pmml(pipeline, "./demo.pmml", with_repr=True)
