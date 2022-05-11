import sys
import numpy as np
import random
import math

n = 50
m = 50
q = 997

message = 0

#A = np.array([[5,3,-1],[6,1,-13],[1,-11,1],[-7,4,0]])
#s = np.array([2,3,-2])
#e = np.array([1,-1,0,1])


A = np.random.randint(low=-q,high=q,size=(m,n))
s = np.random.randint(low=-q,high=q,size=n)
e = np.random.randint(-1,1,size=m)

s = np.transpose(s)
e = np.transpose(e)

B = np.mod(np.add(np.dot(A,s), e), q)
#print(f'As ={np.add(np.dot(A,s), e)}')
print(f'Private key ({s}, {e})')


print(f'Public key ({A}, {B})')
ap = np.mod(A.sum(axis=0),q)
pp = (B.sum() + message * q//2) % q

print(f'Ciphertext ({ap}, {pp})')
ep = (pp - np.dot(ap, s)) % q

print(f'Range ({(q//2-q//4)}, {(q//2+(q//4))})')
decrypted = 1 if (q//2-(q//4)) <= ep <= (q//2+(q//4)) else 0
#print(ep)
print(f'Decrypted message from {ep} is {decrypted}')


####################################################




