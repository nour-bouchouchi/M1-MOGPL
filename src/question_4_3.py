from gurobipy import *
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')


nb_scena = 2
nb_arcs = 12
noms_arcs = ['ab', 'ac', 'ad', 'bd', 'be', 'bc', 'dc', 'ce', 'df', 'cf', 'eg', 'fg']

def PL(w,t):
        
    w_prim = [w[i]-w[i+1] for i in range(len(w)-1)]+[w[-1]]
    k_w_prim = [w_prim[i]*(i+1) for i in range(len(w))]
    
    m = Model("question_4_3")

    # declaration variables de decision
    r = []
    for i in range(nb_scena):
        r.append(m.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY,name="r%d" % (i+1)))

    b = []
    for i in range(nb_scena):
        bi=[]
        for j in range(nb_scena):
            bi.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="b%d%d" % ((i+1),(j+1))))
        b.append(bi)
        
    x = []    
    for i in range(nb_arcs):
        x.append(m.addVar(vtype=GRB.BINARY, lb=0, name="x%s" % noms_arcs[i]))
        
    # maj du modele pour integrer les nouvelles variables
    m.update()

    obj = LinExpr();
    obj = 0
    for k in range(nb_scena):
        obj += k_w_prim[k] * r[k]
    for k in range(nb_scena):
        obj += - w_prim[k] * quicksum(b[i][k] for i in range(nb_scena))


    # definition de l'objectif
    m.setObjective(obj,GRB.MAXIMIZE)

    # Definition des contraintes
    for k in range(nb_scena):
        for i in range(nb_scena):
            m.addConstr(r[k]-b[i][k] <= -quicksum(t[i][j]*x[j] for j in range(nb_arcs)), "Contrainte%d" % (i*nb_arcs+k))
        
    m.addConstr(x[0] + x[1] + x[2] == 1, "Contrainte_a")    #depuis a
    m.addConstr(-x[10] - x[11] == -1, "Contrainte_g")    #vers g
    #nombre d'arcs sortant - nombre d'arcs sortant = 0(pour les noeuds autre que a et g)
    m.addConstr(x[3] + x[4] + x[5] - x[0] == 0, "Contrainte_b")    # b
    m.addConstr(x[7] + x[9] - x[1] - x[5] - x[6] == 0, "Contrainte_c")    # c
    m.addConstr(x[6] + x[8] - x[2] - x[3] == 0, "Contrainte_d")    # d
    m.addConstr(x[10] - x[4] - x[7] == 0, "Contrainte_e")    # e
    m.addConstr(x[11] - x[8] - x[9]  == 0, "Contrainte_f")    # f


    m.optimize()

    print('\nSolution optimale pour %d scenarios ' % nb_scena)
    print("\nTemps pour parcourir le chemin de a à g :")
    for i in range(nb_scena):
        print('t',(i+1),' = ', quicksum(t[i][j]*x[j].x for j in range(nb_arcs)))
    print("\nArcs empruntés :")
    for i in range(nb_arcs):
        print(noms_arcs[i],' = ', x[i].x)
    
    z1 = sum(t[0][j]*x[j].x for j in range(nb_arcs))
    z2 = sum(t[1][j]*x[j].x for j in range(nb_arcs))
    
    return z1, z2


nb_inst = 20
ResT=[]
t = [np.random.randint(1, 20, (nb_scena, nb_arcs)) for _ in range(nb_inst)]
for alpha in range(1,6):    
    T1 = np.zeros(nb_inst)
    T2 = np.zeros(nb_inst)
    w = np.array([1 - (1/2)**alpha, (1/2)**alpha])
    for i in range(nb_inst):
        z1, z2 = PL(w,t[i])
        T1[i] = z1
        T2[i] = z2
    print("T1 :",T1)
    print("T2 :",T2)
    ResT.append([w,T1,T2])
    plt.title(f'Chemin robuste alpha = {alpha} (w = {w})')
    plt.scatter(T1, T2)
    plt.xlabel('Scénario 1')
    plt.ylabel('Scénario 2')
    plt.xticks(range(0, 51, 5))
    plt.yticks(range(0, 51, 5))
    plt.savefig(f'FigureQuestion4_3_alpha{alpha}')
    plt.show()
    plt.clf()

for i in range(1,5):
    print("\nalpha : ",i)
    print("w : ", ResT[i-1][0])
    print("t1 : ",ResT[i-1][1])
    print("t2 : ",ResT[i-1][2])
        
    
