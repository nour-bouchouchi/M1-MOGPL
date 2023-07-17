from gurobipy import *
import numpy as np

def PL(k):
    # valeur de k (varie de 1 à 6)
    
    
    nbcont=6
    nbvar=7
    
    # Range of plants and warehouses
    lignes = range(nbcont)
    colonnes = range(nbvar)
    
    
    # Matrice des contraintes
    a = [[1, -1, 0, 0, 0, 0, 0],
         [1, 0, -1, 0, 0, 0, 0],
         [1, 0, 0, -1, 0, 0, 0],
         [1, 0, 0, 0, -1, 0, 0],
         [1, 0, 0, 0, 0, -1, 0],
         [1, 0, 0, 0, 0, 0, -1]]
    
    # Second membre
    b = [4, 7, 1, 3, 9, 2]
    
    # Coefficients de la fonction objectif
    c = [k, -1, -1, -1, -1, -1, -1]
    
    m = Model("question_1_2")
    
    # declaration variables de decision
    x = []
    x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="r%d" % k))
    for i in range(1,nbvar):
        x.append(m.addVar(vtype=GRB.INTEGER, lb=0, name="b%d%d" % ((i), k)))
    
    # maj du modele pour integrer les nouvelles variables
    m.update()
    
    obj = LinExpr();
    obj =0
    for j in colonnes:
        obj += c[j] * x[j]
    
    # definition de l'objectif
    m.setObjective(obj,GRB.MAXIMIZE)
    
    # Definition des contraintes
    for i in lignes:
        m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)
    
    # Resolution
    m.optimize()
    
    
    print("")
    print('Solution optimale:')
    
    print('r%d'%(k), '=', x[0].x)
    for j in range(1,nbvar):
        print('b%d%d'%((j),k), '=', x[j].x)
    print("")
    print('Valeur de la fonction objectif :', m.objVal)
    return m.objVal


z=np.zeros(6)
for i in range(1,7):
    z[i-1]=PL(i)
print("\nz = ", z)
