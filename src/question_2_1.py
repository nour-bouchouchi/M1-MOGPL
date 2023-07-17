from gurobipy import *

#nombre de personnes 
n=3
#nombre d'objets 
p=6

w=[10,3,1]
w=[3,2,1]
#w = [1/3,1/3,1/3]

w_prim = [w[i]-w[i+1] for i in range(len(w)-1)]+[w[-1]]
k_w_prim = [w_prim[i]*(i+1) for i in range(len(w))]

#valeurs des objets
c_z=[325,225,210,115,75,50]


m = Model("question_2_1")

# declaration variables de decision
r = []
for i in range(n):
    r.append(m.addVar(vtype=GRB.CONTINUOUS,lb=-GRB.INFINITY, name="r%d" % (i+1)))

b = []
for i in range(n):
    bi = []
    bi.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="b%d1" % (i+1)))
    bi.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="b%d2" % (i+1)))
    bi.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="b%d3" % (i+1)))
    b.append(bi)
    
x = []    
for i in range(n):
    xi=[]
    for j in range(p):
        xi.append(m.addVar(vtype=GRB.BINARY, lb=0, name="x%d%d" % ((i+1),(j+1))))
    x.append(xi)
    
# maj du modele pour integrer les nouvelles variables
m.update()

obj = LinExpr();
obj = 0
for k in range(n):
    obj += k_w_prim[k] * r[k]
for k in range(n):
    obj += - w_prim[k] * quicksum(b[i][k] for i in range(n))

# definition de l'objectif
m.setObjective(obj,GRB.MAXIMIZE)

# Definition des contraintes
for j in range(p):
    m.addConstr(quicksum(x[i][j] for i in range(n)) <= 1, "Contrainte%d" % (i+n))

for i in range(n):
    for k in range(n):
        m.addConstr(r[k]-b[i][k] <= quicksum(c_z[j]*x[i][j] for j in range(p)), "Contrainte%d" % (p+j+i*n))

# Resolution
m.optimize()

print('Solution optimale:')
for i in range(n):
    print('r',i, '=', r[i].x)
for i in range(n):
    for j in range(n):
        print('b',i,j,' = ', b[i][j].x)
print("Affectation des objets aux agents :")
for i in range(n):
    for j in range(p):
        print('x',i+1,j+1,' = ', x[i][j].x)
print("Somme des valeurs des objets attribués pour chaque agent : ")
for i in range(n):
    print('z',(i+1),' = ', quicksum(c_z[j]*x[i][j].x for j in range(p)))


