from borg import *

borg = Borg(2, 2, 0, lambda x,y : [x**2 + y**2, (x-2)**2 + y**2],
        bounds=[[-50, 50], [-50, 50]],
        epsilons=[0.01, 0.01])
result = borg.solve({"maxEvaluations":10000})
result.display()

for solution in borg.solve({'maxEvaluations':10000}):
        solution.display()
  