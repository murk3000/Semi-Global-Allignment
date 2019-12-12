import pandas as pd

def u_input():
    # --- User Input ---
    seq1 = "ACTAEEWTCGHAT"    # Sequence 1
    seq2 = "WEETCHTAWEA"      # Sequence 2
    gp = -2                 # gap penalty

    # --- Format input correctly ---
    arr1 = ['gap'] + [c for c in seq1]
    arr2 = ['gap'] + [c for c in seq2]
    return arr1, arr2, gp

def initialize(seq1, seq2, gp): 

    # --- Creating two matrices and initializing them to known values ---
    scoring = pd.DataFrame(columns=seq1, index=seq2)
    direct = pd.DataFrame(columns=seq1, index=seq2)
    sc = 0
    for p in seq1:
        scoring.loc['gap', p] = sc
        direct.loc['gap', p] = "none"
        sc = sc # add gp for global assignment
    sc = 0 
    for p in seq2:
        scoring.loc[p, 'gap'] = sc
        direct.loc[p, 'gap'] = "none"
        sc = sc # add gp for global assignment
    # print(scoring) # DEBUG
    # print(direct) # DEBUG
    return scoring, direct 

def allign(seq1, seq2, gp, score, direct, blossom):

    # --- creating the square matrice of maximum scores ---
    for i in (range(1, len(seq2))):
        # print(score) # DEBUG
        # print(direct) # DEBUG
        for j in range(1, len(seq1)):
            # print(i, ' ', j) # DEBUG
            diag = score.iloc[i-1,j-1] + blossom[seq1[j]][seq2[i]]
            horz = score.iloc[i, j-1] + gp
            vert = score.iloc[i-1, j] + gp
            # print('line:\t', diag, '\t', vert, '\t', horz) # DEBUG
            val = max(zip([diag, vert, horz, 0], ['d', 'v','h', 'none'])) # remove the zero to use global allignment
            score.iloc[i,j] = val[0]
            direct.iloc[i,j] = val[1]

def semi_glob_index(score, i_max, j_max):

    # --- finding the maximum index in the last row and column ---
    max_c = (i_max, j_max)
    max_v = score.iloc[i_max,j_max]

    for i in range(0, i_max):
        if max_v < score.iloc[i, j_max]:
            max_v = score.iloc[i, j_max]
            max_c = (i, j_max)
    for j in range(0, j_max):
        if max_v < score.iloc[i_max, j]:
            max_v = score.iloc[i_max, j]
            max_c = (i_max, j)
    return max_c
            
def pair(i, j, direct, score):

    # --- creating the allignment by backtracing ---
    allg1 = []
    allg2 = []
    while (direct.iloc[i,j] != 'none'):
        c = direct.iloc[i,j]
        # print(score.iloc[i,j], ' ', c, ' ', i, ' ', j) # DEBUG
        if c=='d':
            allg1 = [direct.columns[j]]+allg1
            allg2 = [direct.index[i]]+allg2
            i = i-1
            j = j-1
        elif c=='h':
            allg1 = [direct.columns[j]]+allg1
            allg2 = ['-']+allg2
            j = j-1
        elif c=='v':
            allg1 = ['-']+allg1
            allg2 = [direct.index[i]]+allg2
            i = i-1
        elif c=='none':
            break
    return allg1, allg2

def score_matrix():
    blossom = pd.read_csv("blossom.csv")
    seq1, seq2, gp = u_input()
    score, direct = initialize(seq1, seq2, gp)
    allign(seq1, seq2, gp, score, direct, blossom)
    i, j = semi_glob_index(score, len(seq2)-1, len(seq1)-1) # compare all values for maximum for local allignment
    allg1, allg2 = pair(i, j, direct, score) # pass the bottom-right index for global allignment
    print("Your scoring matrix is:\n", score)
    print("Your directions are:\n", direct)
    print("The respective allignment is:\n", allg1,'\n', allg2)
    
score_matrix()