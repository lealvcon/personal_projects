
"""
maze solver using BFS algorithm, finds the shortest path to the exit
moving in four possible directions avoiding the stones (#)
"""
import numpy as np

board=[['s','.','#','#','.','.','e'],
       ['.','.','.','.','.','#','.'],
       ['.','#','.','.','.','.','.'],
       ['.','.','#','#','.','.','.'],
       ['#','.','#','.','.','#','.']]

board=np.array(board)
rows, columns= board.shape
s=np.where(board=='s')
e=np.where(board=='e')
start=(int(s[0]),int(s[1]))
end=(int(e[0]),int(e[1]))

def get_neighbors(r,c):
    up=(r-1,c)
    down=(r+1,c)
    left=(r,c-1)
    right=(r,c+1)
    if c-1 < 0:
        left=None
    elif c+1 == columns:
        right=None
    if r-1 <0:
        up=None
    elif r+1 == rows:
        down=None
    return [up,down,left,right]



def solve(start,end,board):
    queue=[start]
    path=[]
    visited=[]
    prev=[None]
    
    while queue:
        current_tile=queue[0]
        r,c=current_tile
        if current_tile not in visited:
            visited.append(current_tile)
        neighbors=get_neighbors(r,c)
        neighbors=[n for n in neighbors if (n and n not in visited and board[n[0]][n[1]]!='#')]
        if not neighbors:
            queue.pop(0)
            continue
        for n in neighbors:
            queue.append(n)
            visited.append(n)
            prev.append(current_tile)
    now=end
    try:
        while now != start:
            path.append(now)
            i=visited.index(now)
            now=prev[i]
        path.append(start)
        return path[::-1]
    except ValueError:
        print('NO PATH AVAILABLE')
print(board)
print()
print('path: {}'.format(solve(start,end,board)))
    
    
    
    
        