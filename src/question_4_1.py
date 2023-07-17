from gurobipy import *

nb_arcs=12

# Coefficients de la fonction objectif (coût de chaque arc)
t = [5,10,2,1,4,4,1,3,3,1,1,1] # scénario 1
t = [3,4,6,3,6,2,4,1,5,2,1,1] #scénario 2

noms_arcs = ['ab', 'ac', 'ad', 'bd', 'be', 'bc', 'dc', 'ce', 'df', 'cf', 'eg', 'fg']

m = Model("question_4_1")

# declaration variables de decision
x=[]
for i in range(nb_arcs):
    x.append(m.addVar(vtype=GRB.BINARY, name="x%s" % noms_arcs[i]))

# maj du modele pour integrer les nouvelles variables
m.update()

obj = LinExpr();
obj = 0
for j in range(nb_arcs):
    obj += t[j] * x[j]
    
# definition de l'objectif
m.setObjective(obj,GRB.MINIMIZE)

# Definition des contraintes
m.addConstr(x[0] + x[1] + x[2] == 1, "Contrainte_a")    #depuis a
m.addConstr(x[10] + x[11] == 1, "Contrainte_g")    #vers g
#nombre d'arcs sortant - nombre d'arcs sortant = 0(pour les noeuds autre que a et g)
m.addConstr(x[3] + x[4] + x[5] - x[0] == 0, "Contrainte_b")    # b
m.addConstr(x[7] + x[9] - x[1] - x[5] -x[6] == 0, "Contrainte_c")    # c
m.addConstr(x[6] + x[8] - x[2] - x[3] == 0, "Contrainte_d")    # d
m.addConstr(x[10] - x[4] - x[7] == 0, "Contrainte_e")    # e
m.addConstr(x[11] - x[8] - x[9]  == 0, "Contrainte_f")    # f

# Resolution
m.optimize()

#solution optimale 
print("Arcs empruntés :")
for i in range(nb_arcs):
    print(" arc %s = %d"% (noms_arcs[i],x[i].x))
print("Temps pour parcourir le chemin de a à g :", quicksum([t[j] * x[j].x for j in range(nb_arcs)]))
