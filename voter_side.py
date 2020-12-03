import math
import json
from random import randrange
# election properties
paillier_keys_filename = "paillier_props.json"
bb_filename = "bulletin_board_paillier.txt"
with open(paillier_keys_filename) as p_file:
  data = json.load(p_file)
n = data["n"]
g = data["g"]
noCandidate = data["noCandidate"]

# paillier operations
def paillier_encryption(m, g, r, n):
  return pow(g,m) * pow(r, n) % n**2

def encrypt_votes(vote,noCandidate):
    # encrypt 
    e_votes = []
    for i in range(1, noCandidate + 1):
        m = 0
        r = randrange(1, n)
        if vote == i:
            print(i)
            m = 1
        e_votes.append(paillier_encryption(m, g,r,n))
    return e_votes
# VOTING PHASE
print("WELCOME TO EVOTING DEMONSTRATION BOOTH!!!")
print("\n===== VOTER PROCEDURE =======")
def enter_num_from_list(mess, maxNum):
    li = [i + 1 for i in range(maxNum)]
    while True:
        print("valid number is from 1 to {}".format(maxNum))
        try:
            num = int(input(mess))
        except ValueError:
            num = -1

        if num in li:
            break
        print("please choose only number in the list!")
    return num

#1. pick vote number
print("1. You need to enter your vote for one of the candidates")
vote = enter_num_from_list("--> your vote is: ", noCandidate)
#2. choose random number
print("There will be {} encrypted voting number corresponding the number of candidates, which is {}".format(noCandidate, noCandidate))
print("The encryption of the candidate of your choice is 1 while the others' are 0, representing support or rejection")
print("Disclamer: you are supposed to provide a random number to encrypt your vote\n" +
"as an confirm for the system' transparency")
print("however for the sack of convienience, we will generate it for you using Python's speudo-random function")
# got the vote now encrypt it
print("System's public key is (n,g)=({},{})".format(n,g))
print("Encrypt your vote....")
e_votes = encrypt_votes(vote, noCandidate)    
print("Your vote has been encrypted to {}".format(e_votes))
print("Now it will be saved to voting machine....")
# write people's vote to file 
with open(bb_filename, "a+") as b_file:
    for i in e_votes:
        b_file.write("{}\t".format(i))
    b_file.write("\n")
print("Done save to file, you can check file {}\nto see your encrypted vote is saved along with others' votes ".format(bb_filename))