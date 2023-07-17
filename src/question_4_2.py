from gurobipy import *

nb_scena=2
nb_arcs=12

w = [2,1]
w_prim = [w[i]-w[i+1] for i in range(len(w)-1)]+[w[-1]]
k_w_prim = [w_prim[i]*(i+1) for i in range(len(w))]

t = [[5,10,2,1,4,4,1,3,3,1,1,1], # scénario 1
     [3,4,6,3,6,2,4,1,5,2,1,1]] #scénario 2

noms_arcs = ['ab', 'ac', 'ad', 'bd', 'be', 'bc', 'dc', 'ce', 'df', 'cf', 'eg', 'fg']

# Coefficients de la fonction objectif
#c = k_w_prim + [-w_prim[0] for i in range(nb_scena)] + [-w_prim[1] for i in range(nb_scena)] + [0 for i in range(nb_arcs)]
 
m = Model("question_4_2")

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
