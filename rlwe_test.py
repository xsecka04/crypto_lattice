import numpy as np

q= 13
A = [4,1,11,10]
sA = [6,9,11,11]
eA =[0,-1,1,1]
n = np.size(A)


print(A,sA,eA)
xN_1 = [1] + [0] * (n-1) + [1]
print(xN_1)
A = np.floor(np.polydiv(A,xN_1)[1])
bA = np.polymul(A,sA)%q
bA = np.floor(np.polydiv(bA,xN_1)[1])
bA = np.polyadd(bA,eA)%q
bA = np.floor(np.polydiv(bA,xN_1)[1])
print ("Print output\n",bA)


import random
import hashlib
#from secp256k1 import curve,scalar_mult,point_add
import sys

# Alice's secret key
#s = random.randint(0, curve.n-1)
s = np.gen_poly(n,q)


# Alice random value for signature
#y = random.randint(0, curve.n-1)
y = np.gen_poly(n,q)

#G= curve.g
#Y = scalar_mult(y,G)
#S = scalar_mult(s,G)

bA = np.polymul(A,sA)%q
bA = np.floor(np.polydiv(bA,xN_1)[1])
bA = np.polyadd(bA,eA)%q
bA = np.floor(np.polydiv(bA,xN_1)[1])



M="hello"
if (len(sys.argv)>1):
	M=str(sys.argv[1])

M=M.encode()
Y_x,Y_y = Y
S_x,S_y = S

e=hashlib.sha256(Y_x.to_bytes(32,'big')+Y_y.to_bytes(32,'big')+M)

digest = e.hexdigest()
e = int(digest, 16)

z=(y-s*e) % curve.n

print (f"Message: {M.decode()}")
print (f"Alice secret key (s)={s}")
print (f"Alice public key (S)={S}\n")
print (f"Alice random (y)={y}\n\n")

