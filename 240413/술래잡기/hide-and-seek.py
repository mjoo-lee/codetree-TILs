n,m,h,k = map(int, input().split())

board = [[0 for _ in range(n+1)] for _ in range(n+1)]
domang = []
domang_dir = []
tree = []

for _ in range(m):
    x,y,d = map(int, input().split())
    domang.append([x,y])
    if d == 1:
        domang_dir.append((0,1)) #오른쪽부터 시작
    else:
        domang_dir.append((-1,0)) #아래 보고 시작

for _ in range(h):
    tx, ty = map(int, input().split())
    tree.append((tx,ty))

soollae = (n//2+1, n//2+1)
soollae_dir = 0 #처음 시작에는 위를 보고 있음
soollae_move = 0
soollae_i = 0
point = 0
d = [(-1,0),(0,1),(1,0),(0,-1)]
turn = [1]
i = 1
j = 1
while i<(n*n):
    cnt = j
    while cnt > 0:
        i += j
        if i >= (n*n):
            break
        turn.append(i)  
        cnt -=1
    j += 1
    
def dist(x,y):
    (sr, sc) = soollae
    return abs(sr-x)+abs(sc-y)
    
def move_domang():
    for i in range(m):
        (curR, curC) = domang[i]
        dr,dc = domang_dir[i]
        #거리 3 초과면 건너뜀
        if dist(curR, curC) > 3:
            continue
        if (curR, curC) == (-1,-1): #game over
            continue
    
        newR, newC = curR + dr, curC + dc
        #범위 안에 있는 경우
        if 1<=newR<=n and 1<=newC<=n:
            #술래 없는 경우만 이동
            if (newR, newC) != soollae:
                domang[i] = (newR, newC)
        else:
            dr *= -1
            dc *= -1
            domang_dir[i] = (dr,dc) #방향 틀어줌
            newR, newC = curR + dr, curC + dc #새로운 위치
            if (newR, newC) != soollae:
                domang[i] = (newR, newC)
            
def move_soollae():
    global soollae, soollae_move, soollae_i, soollae_dir, d
    
    curR, curC = soollae
    dr, dc = d[soollae_dir]
    
    newR, newC = curR + dr, curC + dc
    soollae_move += 1
    soollae = (newR, newC) #위치 업데이트
    
    if soollae_move == turn[soollae_i]:
        soollae_dir = (soollae_dir+1)%4
        soollae_i += 1
    
    #이동하다가 맨 처음으로 오면
    if curR == 1 and curC == 1:
        soollae_move = 0
        soollae_i = 0
        d = d[::-1] #거꾸로

def catch_domang(t):
    global point
    
    curR, curC = soollae
    in_range = [(curR, curC)]
    dr, dc = d[soollae_dir]
    
    for i in range(2):
        curR += dr
        curC += dc
        if 1<=curR<=n and 1<=curC<=n:
            in_range.append((curR, curC))
    
    for catchR, catchC in in_range:
        for i in range(m):
            domangR, domangC = domang[i]
            #나무에 숨었으면 안잡힘
            if (domangR, domangC) in tree:
                continue
                
            if catchR == domangR and catchC == domangC:
                point += t
                domang[i] = (-1,-1)

for t in range(1,k+1):
    move_domang()
    #print(domang)
    move_soollae()
    #print(soollae)
    catch_domang(t)
    #print(domang)

print(point)