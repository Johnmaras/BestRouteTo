import pickle

f = open("col_visited", 'br')
# f = open("col_paths", 'br')
# f = open("parsed_list", 'br')
# f = open("neighbors", 'br')

l = pickle.load(f)

f.close()

for p in l:
    if not (l.count(p) == 1):
        print(p)

print("hi")
