from sys import *
from math import *
from borg import *

nvars = 11
nobjs = 2
k = nvars - nobjs + 1

def DTLZ2(*vars):
	g = 0

	for i in range(nvars-k, nvars):
		g = g + (vars[i] - 0.5)**2

	objs = [1.0 + g]*nobjs

	for i in range(nobjs):
		for j in range(nobjs-i-1):
			objs[i] = objs[i] * cos(0.5 * pi * vars[j])
		if i != 0:
			objs[i] = objs[i] * sin(0.5 * pi * vars[nobjs-i-1])

	return objs

borg = Borg(nvars, nobjs, 0, DTLZ2)
borg.setBounds(*[[0, 1]]*nvars)
borg.setEpsilons(*[0.01]*nobjs)
result = borg.solve({"maxEvaluations":10000})
result.display()
for solution in result:
	print(solution.getObjectives())


