N,M,K = map(int, input().split())

maze = [[0 for _ in range(N+1)]] + [[0] + list(map(int, input().split())) for _ in range(N)]
player_list = [(-1,-1)]
for _ in range(M):
    player_list.append(tuple(map(int, input().split())))
exit = tuple(map(int, input().split()))   
maze[exit[0]][exit[1]] = -1    

move = 0

cnt = 0

def move_players():
    global move, cnt, exit
    for i in range(1,M+1):
        #이미 탈출 성공했으면 건너뜀
        if player_list[i] == exit:
            continue
            
        (tx, ty) = player_list[i]
        (ex, ey) = exit
        #nx, ny = tx, ty
        #상하부터 체크
        if ex != tx:
            nx, ny = tx, ty
            if ex > nx:
                nx += 1
            else:
                nx -= 1
        
            if (nx,ny) == exit:
                player_list[i] = (nx, ny)
                move += abs(nx-tx)
                cnt += 1
                continue
            elif (nx,ny) != exit and maze[nx][ny] == 0: #이동 가능하면
                player_list[i] = (nx, ny)
                move += abs(nx-tx)
                continue
            
        #좌우 체크
        if ey != ty:
            nx, ny = tx, ty
            if ey > ny:
                ny += 1
            else:
                ny -= 1
        
            if (nx, ny) == exit:
                player_list[i] = (nx, ny)
                move += abs(ny-ty)
                cnt += 1
                continue
            elif (nx,ny) != exit and maze[nx][ny] == 0: #이동 가능하면
                player_list[i] = (nx, ny)
                move += abs(ny-ty)
                continue
    
def find_square():
    
    global exit, sx, sy, sz, maze
    ex, ey = exit
    
    for size in range(2, N+1):
        for x in range(1,N-size+2):
            for y in range(1,N-size+2):    
                if not (x <= ex < x + size and y <= ey < y + size):
                    continue
                
                have_player = False
                for i in range(1, M+1):
                    (tx, ty) = player_list[i]
                    
                        
                    if x <= tx < x + size and y <= ty < y + size:
                        if (tx,ty) != exit:
                            have_player = True
                
                if have_player:
                    sx, sy, sz = x, y, size
                    #print("정사각형",sx, sy, sz)
                    return


def rotate():
    
    global exit, maze
    #벽 내구도 깎음
    for x in range(sx, sx+sz):
        for y in range(sy, sy+sz):
            if maze[x][y] > 0:
                maze[x][y] -= 1 
    #print("내구도-1",maze)
    #회전
    rotate = [[0] * sz for _ in range(sz)]
    for x in range(sx, sx+sz):
        for y in range(sy, sy+sz):
            rotate[x-sx][y-sy] = maze[x][y]
    
    rotate = [list(row) for row in zip(*rotate[::-1])]
    
    for x in range(sx, sx+sz):
        for y in range(sy, sy+sz):
            maze[x][y] = rotate[x-sx][y-sy]
    
    #print("회전",maze)
    
    #player 좌표 업데이트
    for i in range(1,M+1):
        (tx, ty) = player_list[i]
        #이미 나간 애들은 건너뜀 -> 건너뛰면 안됨!!!!!!!!! exit 바뀌니까 같이 바뀌어야함
#         if (tx,ty) == exit:
#             continue
            
        if sx <= tx < sx + sz and sy <= ty < sy + sz:
            ox = tx - sx
            oy = ty - sy
            player_list[i] = (oy+sx, sz-1-ox+sy)
    
    #exit 업데이트 
    for x in range(1,N+1):
        for y in range(1,N+1):
            if maze[x][y] == -1:
                exit = (x, y)
                break
    
    
    
for k in range(K):
    #print(k+1,"번째 초기 maze",maze)
    sx, sy, sz = 0, 0, 0
    if cnt == M:
        break
    
    move_players()
    #print("이동",player_list)
    find_square()
    rotate()    
    #print("회전",player_list)

print(move)
print(exit[0],exit[1],end=" ")