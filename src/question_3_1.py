from gurobipy import *

nbcont=5
nbvar=10

w = [2,1]
#w = [10,1]
#w = [1/2,1/2]

# Range of plants and warehouses
lignes = range(nbcont)
colonnes = range(nbvar)

# Matrice des contraintes
a = [[0, 0, 0 , 0 , 0 , 0 , 40 , 50 , 60 , 50 ],
     [1, 0, -1, 0 , 0 , 0 , -19, -6 , -17, -2 ],
     [0, 1, 0 , -1, 0 , 0 , -19, -6 , -17, -2 ],
     [1, 0, 0 , 0 , -1, 0 , -2 , -11, -4 , -18],
     [0, 1, 0 , 0 , 0 , -1, -2 , -11, -4 , -18]]

# Second membre
b = [100, 0, 0, 0, 0]

# Coefficients de la fonction objectif
c = [w[0]-w[1], 2*w[1], -(w[0]-w[1]), -w[1], -(w[0]-w[1]), -w[1], 0, 0, 0, 0]

m = Model("question_3_1")

# declaration variables de decision
x = []
x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="r1"))
x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="r2"))
for i in range(2):
    x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="b%d1" % (i+1)))
    x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="b%d2" % (i+1)))
for i in range(4):
    x.append(m.addVar(vtype=GRB.BINARY, lb=0, name="x%d" % (i+1)))


# maj du modele pour integrer les nouvelles variables
m.update()

obj = LinExpr();
obj = 0
for j in colonnes:
    obj += c[j] * x[j]

# definition de l'objectif
m.setObjective(obj,GRB.MAXIMIZE)

# Definition des contraintes
m.addConstr(quicksum(a[0][j]*x[j] for j in colonnes) <= b[0], "Contrainte0")
for i in range(1,5):
    m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)

# Resolution
m.optimize()


print('Solution optimale:')
print('r1', '=', x[0].x)
print('r2', '=', x[1].x)
print('b11', '=', x[2].x)
print('b12', '=', x[3].x)
print('b21', '=', x[4].x)
print('b22', '=', x[5].x)
print("Selection des projets :")
for j in range(6,10):
    print('x%d'%(j-5), '=', x[j].x)
print('Valeur de la fonction objectif :', m.objVal)
print("z1 =", 19*x[6].x + 6*x[7].x + 17*x[8].x + 2*x[9].x )
print("z2 =", 2*x[6].x + 11*x[7].x + 4*x[8].x + 18*x[9].x )
 
