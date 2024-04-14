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
        domang_dir.append((1,0)) #아래 보고 시작

for _ in range(h):
    tx, ty = map(int, input().split())
    tree.append((tx,ty))

soollae = (n//2+1, n//2+1)
soollae_dir = 0 #처음 시작에는 위를 보고 있음
soollae_move = 0
soollae_reverse = False
soollae_i = 0
point = 0
d = [(-1,0),(0,1),(1,0),(0,-1)]
i = 0
j = 1
turn = []
while i<=(n*n):
    for _ in range(2):
        i+=j
        if i >= n*n:
            break
        turn.append(i)
    j+=1
turn += [n*n-1]

def dist(x,y):
    global soollae
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
    global soollae, soollae_move, soollae_i, soollae_dir, d, soollae_reverse
    
    curR, curC = soollae
    dr, dc = d[soollae_dir]
    #print("술래cur:",curR,curC)
    #print(soollae_move)
    newR, newC = curR + dr, curC + dc
    if not soollae_reverse:
        soollae_move += 1
    else:
        soollae_move -= 1
        
    soollae = (newR, newC) #위치 업데이트
    #print("술래 이동:",newR,newC)
    #이동하다가 맨 처음으로 오면
    if newR == 1 and newC == 1:
        #d = [(-1,0),(0,1),(1,0),(0,-1)] #원래
        d = [(1,0),(0,1),(-1,0),(0,-1)] #거꾸로
        soollae_reverse = True
        soollae_dir = -1 #밑에서 +1되는 55번째 줄 있으므로
        
    elif newR == n//2+1 and newC == n//2+1:
        d = [(-1,0),(0,1),(1,0),(0,-1)]
        soollae_reverse = False
        soollae_dir = -1

    if soollae_move == turn[soollae_i]:
        soollae_dir = (soollae_dir+1)%4
        if not soollae_reverse :
            soollae_i += 1
        else:
            soollae_i -= 1
            

def catch_domang(t):
    global point, d, soollae_dir
    
    curR, curC = soollae
    in_range = [(curR, curC)]
    dr, dc = d[soollae_dir]
    
    for _ in range(2):
        curR += dr
        curC += dc
        in_range.append((curR, curC))
    #print("잡는 범위:",in_range)
    for catchR, catchC in in_range:
        for i in range(m):
            domangR, domangC = domang[i]
            
            if (domangR, domangC) == (-1,-1):
                continue
                
            #나무에 숨었으면 안잡힘     
            if catchR == domangR and catchC == domangC and (domangR, domangC) not in tree:
                #print(t)
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