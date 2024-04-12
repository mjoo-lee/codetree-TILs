from collections import deque

L,N,Q = map(int, input().split())
board = [[-1 for _ in range(L+1)]] + [[-1] + list(map(int, input().split())) for _ in range(L)]
location = [(-1,-1) for _ in range(N+1)]
shield = [(-1,-1) for _ in range(N+1)]
hp = [0 for _ in range(N+1)]



for i in range(1,N+1):
    r,c,h,w,k = map(int, input().split())
    location[i] = (r,c)
    shield[i] = (h,w)
    hp[i] = k

starthp = hp[:]

order = [list(map(int, input().split())) for _ in range(Q)]
d = [(-1,0),(0,1),(1,0),(0,-1)] #상,우,하,좌
is_live = [True for _ in range(N+1)]

####input 작업 완료

def check(idx, dir): # 큐로 바꿔보기
    global is_live
    dr, dc = d[dir][0], d[dir][1]
    newR, newC = location[idx][0] + dr, location[idx][1] + dc
    
    q = deque()
    q.append((newR, newC, idx))
    visited = set()

    while q:
        curR, curC, curidx = q.popleft() #dr, dc 밀린 값 
        #print(curR, curC, idx)
        curH, curW = shield[curidx][0], shield[curidx][1]

        #이 중 하나라도 걸리면 불가
        if curR < 1 or curR + curH - 1 > L or curC < 1 or curC + curW - 1 > L:
            return False
        
        #이동 가능한 경우
        for i in range(1,N+1):
            #게임오버 시 건너뜀
            if not is_live[i]:
                continue

            #명령받은 기사랑 다르면
            if i != curidx and i not in visited:
                neighR, neighC = location[i][0], location[i][1]
                neighH, neighW = shield[i][0], shield[i][1]

                if curR <= neighR <= curR + curH - 1 or curR <= neighR + neighH - 1 <= curR + curH - 1 or curC <= neighC <= curC + curW - 1 or curC <= neighC + neighW - 1 <= curC + curW - 1:   #겹쳐서
                    #옮겨보니 범위 벗어나거나
                    if 1 > neighR+dr or neighR+dr > L or neighR+neighH+dr-1 < 1 or neighR+neighH+dr-1 > L:
                        return False

                    if neighC+dc < 1 or neighC+dc > L or neighC+neighW+dc-1 < 1 or neighC+neighW+dc-1 > L:
                        return False

                    #옮겼더니 벽 있으면 
                    for sr in range(neighR+dr, neighR+dr+neighH):
                        for sc in range(neighC+dc, neighC+dc+neighW):
                            if board[sr][sc] == 2:
                                return False

                    q.append((neighR, neighC, i))
                    visited.add(i)               

    return True

def move(idx, dir):
    global is_live
    dr, dc = d[dir][0], d[dir][1]
    newR, newC = location[idx][0] + dr, location[idx][1] + dc
    newH, newW = shield[idx][0], shield[idx][1]
    location[idx] = (newR, newC) #새로운 곳으로 옮김

    for i in range(1,N+1):
            #게임오버 시 건너뜀
            if not is_live[i]:
                continue
            
            if i != idx:     
                neighR, neighC = location[i][0], location[i][1]
                neighH, neighW = shield[i][0], shield[i][1]

                #겹치면
                if newR <= neighR < newR + newH or newR <= neighR + neighH - 1 < newR + newH or newC <= neighC < newC + newW or newC <= neighC + neighW - 1 < newC + newW:
                    #print(i,"랑 ",idx,"겹침")
                    location[i] = (neighR + dr, neighC + dc) #위치 업데이트

                    #이동한 곳에 함정있는지 확인
                    for sr in range(location[i][0], location[i][0]+neighH): 
                        for sc in range(location[i][1], location[i][1]+neighW):
                            if board[sr][sc] == 1:
                                #print("함정",sr,sc)
                                hp[i] -= 1

                                if hp[i] <= 0:
                                    #print("죽음",i)
                                    is_live[i] = False
                                    break


for q in range(Q):
    #print(q+1,"번째 명령")
    idx, dir = order[q]
    #print(idx,"를",dir,"방향으로")
    #print("위치확인", location)
    canmove = check(idx, dir)
    if canmove:
        #print("move ", idx)
        move(idx, dir)
    
    
    # print("체력확인", hp)

    #print("생존확인", is_live)

ans = 0
# print(starthp)
# print(hp)
for i in range(1,N+1):
    if is_live[i]:
        #print(i)
        ans += starthp[i] - hp[i]

print(ans)