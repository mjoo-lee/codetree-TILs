def is_inrange(x,y):
    return 1 <= x and x <= n and 1 <= y and y <=n

n,m,p,c,d = map(int, input().split())
rudolf = tuple(map(int, input().split()))

points = [0 for _ in range(p+1)]
pos = [(0,0) for _ in range(p+1)]
board = [[0 for _ in range(n+1)] for _ in range(n+1)]
is_live = [False for _ in range(p+1)]
stun = [0 for _ in range(p+1)]

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

board[rudolf[0]][rudolf[1]] = -1 # 방문처리

for _ in range(p): #산타 입력
    id, x, y = tuple(map(int, input().split()))
    pos[id] = (x, y)
    board[pos[id][0]][pos[id][1]] = id
    is_live[id] = True

for t in range(1, m+1): #turn
    closestX, closestY, closestIdx = float('inf'), float('inf'), 0

    for i in range(1, p+1):
        if not is_live[i]:
            continue

        #루돌프에 가장 가까운 산타 찾기
        currentBest = ((closestX - rudolf[0]) ** 2 + (closestY - rudolf[1]) ** 2, (-closestX, -closestY)) #두번째는 뭐지? 
        currentValue = ((pos[i][0] - rudolf[0]) ** 2 + (pos[i][1] - rudolf[1]) ** 2, (-pos[i][0], -pos[i][1]))

        if currentValue < currentBest:
            closestX, closestY = pos[i] #제일 가까운 애 업데이트
            closestIdx = i
        
    # 루돌프 이동 (가장 가까운 산타 방향으로)
    if closestIdx: #제일 가까운애를 찾았다면
        prevRudolf = rudolf
        moveX = 0
        if closestX > rudolf[0]: #더 오른쪽에 있으면, 오른쪽으로 한칸 이동
            moveX = 1
        elif closestX < rudolf[0]:
            moveX = -1

        moveY = 0
        if closestY > rudolf[1]:
            moveY = 1
        elif closestY < rudolf[1]:
            moveY = -1
        
        rudolf = (rudolf[0] + moveX, rudolf[1] + moveY)
        print(rudolf)
        board[prevRudolf[0]][prevRudolf[1]] = 0 # 이전 위치는 0으로 초기화

    # 루돌프로 인해 충돌
    if rudolf[0] == closestX and rudolf[1] == closestY:
        print(rudolf)
        firstX = closestX + moveX * c #가장 가까운 산타 C만큼 이동
        firstY = closestY + moveY * c
        lastX, lastY = firstX, firstY

        stun[closestIdx] = t + 1 #기절
        print("lastX:",lastX,"lastY:",lastY)
        #이동한 위치에 산타 있을 경우 산타를 연쇄적으로 이동시킴
        while is_inrange(lastX, lastY) and board[lastX][lastY] > 0 :
            lastX += moveX
            lastY += moveY
        
        #연쇄적으로 충돌이 일어난 가장 마지막 위치에서 시작
        #순차적으로 보드판에 있는 산타 한 칸 씩 이동
        #바로 이전에 충돌했던 산타 찾는 과정
        while not (lastX == firstX and lastY == firstY):
            beforeX = lastX - moveX
            beforeY = lastY - moveY 

            if not is_inrange(beforeX, beforeY):
                break
            
            idx = board[beforeX][beforeY]

            #다음에 이동할 시 범위 밖으로 벗어나면, 걔는 게임 오버
            if not is_inrange(lastX, lastY):
                is_live[idx] = False
            else:
                board[lastX][lastY] = board[beforeX][beforeY] #이동
                pos[idx] = (lastX, lastY)
            
            lastX, lastY = beforeX, beforeY #다음으로 볼 위치 업데이트 
        
        points[closestIdx] += c
        pos[closestIdx] = (firstX, firstY) #이동
        if is_inrange(firstX, firstY):
            board[firstX][firstY] = closestIdx
        else:
            is_live[closestIdx] = False
    
    board[rudolf[0]][rudolf[1]] = -1 #옮겨간 위치로 루돌프 표시

    # 산타 이동
    for i in range(1, p+1):
        if not is_live[i] or stun[i] >= t:
            continue
        
        minDist = (pos[i][0] - rudolf[0]) ** 2 + (pos[i][1] - rudolf[1]) ** 2
        moveDir = -1

        for dir in range(4):
            nx = pos[i][0] + dx[dir]
            ny = pos[i][1] + dy[dir]

            if not is_inrange(nx, ny) or board[nx][ny] > 0: 
                continue
            
            dist = (nx - rudolf[0]) ** 2 + (ny - rudolf[1]) ** 2
            if dist < minDist: #옮긴게 더 작아지는 방향으로
                minDist = dist
                moveDir = dir
        
        if moveDir != -1:
            nx = pos[i][0] + dx[moveDir]
            ny = pos[i][1] + dy[moveDir]

            #산타 이동으로 인한 충돌 시 -> 산타 D만큼 이동 & D점
            if nx == rudolf[0] and ny == rudolf[1]:
                stun[i] = t + 1

                moveX = -dx[moveDir]
                moveY = -dy[moveDir]

                firstX = nx + moveX * d
                firstY = ny + moveY * d
                lastX, lastY = firstX, firstY

                if d == 1:
                    points[i] += d  
                else:
                    #이동했는데 산타 있을 경우 -> 연쇄적 이동 시작
                    while is_inrange(lastX, lastY) and board[lastX][lastY] > 0:
                        lastX += moveX
                        lastY += moveY

                    #가장 마지막 위치에서 산타 한칸씩 옮김
                    while lastX != firstX and lastY != firstY:
                        beforeX = lastX - moveX
                        beforeY = lastY - moveY
                        
                        if not is_inrange(beforeX, beforeY):
                            break

                        idx = board[beforeX][beforeY]

                        if not is_inrange(lastX, lastY):
                            is_live[idx] = False
                        else:
                            board[lastX][lastY]= board[beforeX][beforeY] #한칸 이동
                            pos[idx] = (lastX, lastY)
                        
                        lastX, lastY = beforeX, beforeY

                    
                    points[i] += d
                    board[pos[i][0]][pos[i][1]] = 0 #초기화
                    pos[i] = (firstX,firstY)
                    if is_inrange(firstX, firstY):
                        board[firstX][firstY] = i
                    else:
                        is_live[i] = False
            else:
                board[pos[i][0]][pos[i][1]] = 0 # 초기화
                pos[i] = (nx, ny)
                board[nx][ny] = i

    for i in range(1, p+1):
        if is_live[i]:
            points[i] += 1

for i in range(1, p+1):
    print(points[i], end=" ")