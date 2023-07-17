from gurobipy import *
import random
import time
import numpy as np

def PL(n):
    #n : nombre de personnes 
    #p : nombre d'objets 
    p=5*n
    U = np.random.randint(1, 20, (n,p)) #matrice d'utilité (note etre 1 et 20)
    
    w = random.sample(range(0,2*n), n) # on tire n nombre distincts entre 1 et 2n
    w.sort(reverse=True)
    w_prim = [w[i]-w[i+1] for i in range(len(w)-1)]+[w[-1]]
    k_w_prim = [w_prim[i]*(i+1) for i in range(len(w))]
    
    
    m = Model("question_2_2")
    m.setParam("TimeLimit",5*60)
    
    # declaration variables de decision
    r = []
    for i in range(n):
        r.append(m.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="r%d" % (i+1)))

    b = []
    for i in range(n):
        bi = []
        for k in range(n):
            bi.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="b%d%d" % ((i+1),(k+1))))
        b.append(bi)

    x = []    
    for i in range(n):
        xi=[]
        for j in range(p):
            xi.append(m.addVar(vtype=GRB.BINARY, lb=0, name="x%d,%d" % ((i+1),(j+1))))
        x.append(xi)
        
    # maj du modele pour integrer les nouvelles variables
    m.update()

        
    obj = LinExpr();
    obj = 0
    for k in range(n):
        obj += k_w_prim[k] * r[k]
    for k in range(n):
        for i in range(n):
            obj += - w_prim[k] * b[i][k] 

    
    # definition de l'objectif
    m.setObjective(obj,GRB.MAXIMIZE)
    
    # Definition des contraintes
    for j in range(p):
        m.addConstr(quicksum(x[i][j] for i in range(n)) <= 1, "Contrainte%d" % (i+n))
    
    for i in range(n):
        for k in range(n):
            m.addConstr(r[k]-b[i][k] <= quicksum(U[i][j]*x[i][j] for j in range(p)), "Contrainte%d" % (p+j+i*n))


    t1 = time.time()
    m.optimize()
    t = time.time() - t1
    
    print('Solution optimale pour n = %d :' %n)
    for i in range(n):
        print('z',(i+1),' = ', quicksum(U[i][j]*x[i][j].x for j in range(p)))
        
    return t


N=[4,8,12,16]

TIMES = np.zeros(len(N))

for i in range(len(N)):
    TIMES[i] = np.mean([PL(N[i]) for _ in range(10)])
    
print("================TIMES===========")
print(TIMES)

import matplotlib.pyplot as plt
plt.style.use("seaborn-whitegrid")

fig = plt.figure()
plt.title("Temps en fonction de n")
plt.plot(N, TIMES)
plt.xlabel("n")
plt.xticks(N)
plt.ylabel("Temps")
plt.legend()
plt.show()