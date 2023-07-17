from gurobipy import *

nbcont=5
nbvar=11

# Range of plants and warehouses
lignes = range(nbcont)
colonnes = range(nbvar)

# Matrice des contraintes
a = [[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
     [1, 0, -1, 0, 0, 0, -5, -6, -4, -8, -1],
     [1, 0, 0, 0, -1, 0, -3, -8, -6, -2, -5],
     [0, 1, 0, -1, 0, 0, -5, -6, -4, -8, -1],
     [0, 1, 0, 0, 0, -1, -2, -8, -6, -2, -5]]

# Second membre
b = [3, 0, 0, 0, 0, 0,0]

# Coefficients de la fonction objectif
c = [1, 2, -1, -1, -1, -1, 0, 0, 0, 0, 0]

m = Model("question_1_4")

# declaration variables de decision
x = []
x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY,name="r1"))
x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="r2"))
for i in range(2):
    x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="b%d1" % (i+1)))
    x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="b%d2" % (i+1)))
for i in range(5):
    x.append(m.addVar(vtype=GRB.BINARY, lb=0, name="x%d" % (i+1)))

# maj du modele pour integrer les nouvelles variables
m.update()

obj = LinExpr();
obj =0
for j in colonnes:
    obj += c[j] * x[j]

# definition de l'objectif
m.setObjective(obj,GRB.MAXIMIZE)

# Definition des contraintes
m.addConstr(quicksum(a[0][j]*x[j] for j in colonnes) == b[0], "Contrainte0")
for i in range(1,5):
    m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)

# Resolution
m.optimize()

print("")
print('Solution optimale:')
print('r1', '=', x[0].x)
print('r2', '=', x[1].x)
print('b11', '=', x[2].x)
print('b12', '=', x[3].x)
print('b21', '=', x[4].x)
print('b22', '=', x[5].x)
print("\nSelection des objets : ")
for j in range(6,11):
    print('x%d'%(j-5), '=', x[j].x)
print("")
print('Valeur de la fonction objectif :', m.objVal)
print("z1 =", 5*x[6].x + 6*x[7].x + 4*x[8].x + 8*x[9].x + x[10].x )
print("z2 =", 3*x[6].x + 8*x[7].x + 6*x[8].x + 2*x[9].x + 5*x[10].x )
