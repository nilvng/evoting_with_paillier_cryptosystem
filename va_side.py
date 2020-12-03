import math
import json
from random import randrange
# election properties
paillier_keys_filename = "paillier_props.json"
bb_filename = "bulletin_board_paillier.txt"
with open(paillier_keys_filename) as p_file:
  data = json.load(p_file)
n = data["n"]
meu = data["meu"]
lamb = data["lamb"]
noCandidate = data["noCandidate"]

# useful functions
def lFunction(u, n):
    return int ((u-1)/n)

def paillier_decryption(cipher, meu, lamb, n):
  u = pow(cipher, lamb, n**2)
  return int(lFunction(u,n) * meu % n)

# SERVER SIDE: tallying vote without decryption
print("\n===== VOTING SERVER OPERATION =======")
print("Here is all the encrypted vote we have in the file: ")
with open(bb_filename, "r") as b_file:
  f_votes = b_file.readlines()
votes = []
for line in f_votes:
    vote = line.split()
    votes.append(vote)
print(votes)
print("Compute tally of votes over the encrypted votes")
# tally of votes
tally = []
for i in range(noCandidate):
    sum_ci = 1
    for j in range(len(votes)):
        sum_ci = pow(sum_ci * int(votes[j][i]), 1, n*n)
    tally.append(pow(sum_ci, 1, n*n))
print("the computed tally: {}\nIt still appear to be an intelligible number as it has not been decrypted yet".format(tally))
print("Not until it's sent to the voting authority...")

#   VOTING AUTHORITY
print("\n=====  VOTING AUTHORITY OPERATION =======")
print("System's private key is (lambda,meu)=({},{})".format(lamb,meu))
print("VA will decrypt the message with their private key...")
print("Here is the result: ")
for i in range(noCandidate):
    print("Candidate #{}: {}".format(i + 1, paillier_decryption(tally[i], meu,lamb,n)))  
