from gurobipy import *
import numpy as np
import time
import random



def PL(n, p):
    # n nombre de personnes
    # p nombre d'objets

    w = random.sample(range(1,2*n), n) # on tire n nombre distincts entre 1 et 2*n
    w.sort(reverse=True)
    w_prim = [w[i]-w[i+1] for i in range(n-1)]+[w[-1]]
    k_w_prim = [w_prim[i]*(i+1) for i in range(n)]
    
    
    # matrice d'utilité, coûts et budget
    U = np.random.randint(1, 20, (n,p)) #matrice d'utilité (note entre 1 et 20)
    ck = np.random.randint(50, 500, p)  #matrice de coût (coût entre 50 et 500)
    bu = ck.sum()/2 #budget alloué
    
    
    m = Model("question_3_2_")

    #déclaration des variables de décision 
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
    for i in range(p):
        x.append(m.addVar(vtype=GRB.BINARY, name="x%d" % (i+1)))
    
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
    m.addConstr(quicksum(ck[j]*x[j] for j in range(p)) <= bu, "Contrainte0")

    cpt=1
    for i in range(n):
        for k in range(n):
            m.addConstr(r[k] - b[i][k] - quicksum(U[i][j]*x[j] for j in range(p)) <= 0, "Contrainte%d" % cpt)
            cpt+=1
            

    
    t1 = time.time()
    m.optimize()
    t = time.time() - t1
    
    print('Solution optimale pour n = %d :' %n)
    for i in range(n):
        print('z',(i+1),' = ', quicksum(U[i][j]*x[j].x for j in range(p)))
        
    return t


N=[2,5,10]
P=[5,10,15,20]



TIMES = np.zeros((len(N),len(P)))

for i in range(len(N)):
    for j in range(len(P)):
        TIMES[i][j] = np.mean([PL(N[i], P[j]) for _ in range(10)])
    
print("================TIMES===========")
print(TIMES)

import matplotlib.pyplot as plt
plt.style.use("seaborn-whitegrid")

fig = plt.figure()
plt.title("Temps en fonction de n et de p")
for i in range(len(N)):
    plt.plot(P, TIMES[i], label=f"n = {N[i]}")
plt.xlabel("p")
plt.xticks(P)
plt.ylabel("Temps")
plt.legend()
plt.show()