from timeit import default_timer as timer
import math

TEST_FAIL_DATA = [
    "3?5?7????",
    "4?1?2?6?8",
    "???1??3??",
    "?5???9?16",
    "1??8?6??4",
    "64?2???8?",
    "??4??1???",
    "8?7?6?4?1",
    "????3?7?9"
    ]

TEST_PASS_DATA = [
    "827154396",
    "965327148",
    "341689752",
    "593468271",
    "472513689",
    "618972435",
    "786235914",
    "154796823",
    "239841567"
]

def clockit(function):
    start = timer()
    f_ret = function
    end = timer()
    time = end - start
    return (time, f_ret)
    
def checker1(data):
    group3 = lambda x: zip(*(iter(x),) * 3)
    check = lambda x: True if sorted(list(x)) == [str(n+1) for n in range(9)] else False
    cols = ["" for x in range(9)] # LOL
    for trio in group3(data):
        blocks = ["","",""]  
        for row in trio:
            for i, r in enumerate(group3(row)):
               blocks[i] += "".join(r)
            for i, c in enumerate(row):
                cols[i] += c
            if not check(row): 
                return False
        for block in blocks:
            if not check(block):
                return False
    for col in cols:
        if not check(col):
            return False
    return True

def checker2(data):
    group3 = lambda x: zip(*(iter(x),) * 3)
    check = lambda x: True if sorted(list(x)) == [str(n+1) for n in range(9)] else False
    nonets = []
    cols = ["" for x in range(9)] # LOL
    for trio in group3(data):
        blocks = ["","",""]  
        for row in trio:
            for i, r in enumerate(group3(row)):
               blocks[i] += "".join(r)
            for i, c in enumerate(row):
                cols[i] += c
            nonets.append(row)
        nonets += blocks
    nonets += cols
    for nonet in nonets:
        if not check(nonet):
            return False
    return True

def checker3(data):
    # Broken
    true_hash = -88554707735888606
    group3 = lambda x: zip(*(iter(x),) * 3)
    check = lambda x: True if hash("".join(sorted(x))) == -88554707735888606 else False
    nonets = []
    for trio in group3(data):
        blocks = ["","",""]  
        for row in trio:
            for i, r in enumerate(group3(row)):
               blocks[i] += "".join(r)
        nonets += blocks
    for nonet in nonets:
        if not check(nonet):
            return False
    return True

if __name__ == "__main__":
    data = TEST_PASS_DATA
    print("Checker 1: ", clockit(checker1(data)))
    print("Checker 2: ",clockit(checker2(data)))   # WINNER
    #print("Checker 3: ",clockit(checker3(data)))
