"""Builds a 10x10 clue word search whose unused letters spell a hidden message (read row by row)."""
import random, json, sys
N=10
WORDS=["AUTOMATIC","AUTOPILOT","CONSISTENT","CONTEXT","WILLPOWER","MYTH","STREAK","ROUTINE","JOURNAL","BRIDGE"]
MSG="THEGRASSDOESNTGROWBACKOVERNIGHT"
DIRS=[(0,1),(1,0),(1,1),(-1,1)]
def attempt(rng):
    g=[[None]*N for _ in range(N)];pos={}
    for w in sorted(WORDS,key=len,reverse=True):
        opts=[]
        for dr,dc in DIRS:
            for r in range(N):
                for c in range(N):
                    er,ec=r+dr*(len(w)-1),c+dc*(len(w)-1)
                    if not(0<=er<N and 0<=ec<N):continue
                    ov=0;ok=True
                    for i,ch in enumerate(w):
                        x=g[r+dr*i][c+dc*i]
                        if x is None:continue
                        if x!=ch:ok=False;break
                        ov+=1
                    if ok and ov<len(w):opts.append((ov,r,c,dr,dc))
        if not opts:return None
        rng.shuffle(opts)
        if rng.random()<.6:opts.sort(key=lambda o:-o[0])
        ov,r,c,dr,dc=opts[0]
        for i,ch in enumerate(w):g[r+dr*i][c+dc*i]=ch
        pos[w]=(r,c,dr,dc)
    return g,pos
rng=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 1)
for t in range(400000):
    res=attempt(rng)
    if not res:continue
    g,pos=res
    empty=[(r,c) for r in range(N) for c in range(N) if g[r][c] is None]
    if len(empty)!=len(MSG):continue
    # need some variety of directions
    if len({(p[2],p[3]) for p in pos.values()})<4:continue
    for (r,c),ch in zip(empty,MSG):g[r][c]=ch
    json.dump({"grid":g,"pos":pos},open("ws.json","w"))
    for row in g:print(" ".join(row))
    print(t,pos);break
else:print("none")
