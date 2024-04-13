from collections import deque

n = int(input())
board = [list(map(int, input().split())) for _ in range(n)]
board_with_group = [[0 for _ in range(n)] for _ in range(n)]
d = [(0,1),(0,-1),(1,0),(-1,0)]
group =[[0,0] for _ in range(n*n+1)] # idx: group / val: 실제num, 칸 갯수로 구성
group_n = 0

def dfs(x,y,visited,group_n):
    global board_with_group
    for dr,dc in d:
        nx, ny = x+dr, y+dc
        if nx<0 or nx>=n or ny<0 or ny>=n or visited[nx][ny]:
            continue
        if board[nx][ny] == board[x][y]:
            board_with_group[nx][ny] = group_n
            group[group_n][1] += 1
            visited[nx][ny] = True
            dfs(nx,ny,visited,group_n)


def make_group():
    global group_n
    group_n = 0
    visited = [[False for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if not visited[i][j]:
                group_n+=1
                visited[i][j] = True
                board_with_group[i][j] = group_n
                group[group_n][0] = board[i][j]
                group[group_n][1] = 1# idx: group / val: 실제num, 칸 갯수
                dfs(i,j,visited, group_n)

def calculate_point():

    #print(group)
    make_group() #그룹화
    point = 0
    
    visited = [[False for _ in range(n)] for _ in range(n)]
    for r in range(n):
        for c in range(n):
            for dr, dc in d:
                nr, nc = r + dr, c + dc
                if nr < 0 or nr >= n or nc < 0 or nc >=n or visited[nr][nc]:
                    continue
                if board_with_group[r][c] != board_with_group[nr][nc]:
                    g1, g2 = board_with_group[r][c], board_with_group[nr][nc]
                    num1, cnt1 = group[g1] 
                    num2, cnt2 = group[g2]
                    
                    point += ((cnt1 + cnt2) * num1 * num2)                
                
    return point//2

def cross(board):
    midR = midC = n//2
    v, h = [], []
    for i in range(n):
        v.append(board[i][midC])
        h.append(board[midR][i])
    
    h = h[::-1]
    for i in range(n):
        board[i][midC] = h.pop(0)
        board[midR][i] = v.pop(0)

def squares(board):
    midR = midC = n//2
    g1,g2,g3,g4 = [],[],[],[]
    #좌상단
    for i in range(midR):
        temp = []
        for j in range(midC):
            temp.append(board[i][j])
        g1.append(temp)
    #우상단
    for i in range(midR):
        temp = []
        for j in range(midC+1,n):
            temp.append(board[i][j])
        g2.append(temp)

    #좌하단
    for i in range(midR+1,n):
        temp = []
        for j in range(midC):
            temp.append(board[i][j])
        g3.append(temp)
    #우하단
    for i in range(midR+1,n):
        temp = []
        for j in range(midC+1,n):
            temp.append(board[i][j])
        g4.append(temp)
    
    g1 = list(zip(*g1[::-1]))
    g2 = list(zip(*g2[::-1]))
    g3 = list(zip(*g3[::-1]))
    g4 = list(zip(*g4[::-1]))

    for i in range(midR):
        for j in range(midC):
            board[i][j] = g1[i][j]
    for i in range(midR):
        for j in range(midC+1, n):
            board[i][j] = g2[i][j-midC-1]
    for i in range(midR+1,n):
        for j in range(midC):
            board[i][j] = g3[i-midR-1][j]
    for i in range(midR+1,n):
        for j in range(midC+1,n):
            board[i][j] = g4[i-midR-1][j-midC-1]
    

ans = 0
print("초기")
ans += calculate_point()

for _ in range(3):
    cross(board)
    squares(board)
    #print("회전후")
    ans += calculate_point()
    #print("============")

print(ans)