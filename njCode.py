import numpy as np

# dMatrix refers to distance matrix

def njPair(dMatrix):
    n = len(dMatrix)
    
    minM = None
    joinPair = None
    
    # sum of rows of dMatrix; range(n-1) because indexed at 0
    for i in range(n-1):
        Rn = sum(dMatrix[i])
        
        # sum of columns/following row of dMatrix
        for j in range(i+1, n):
            Rm = sum(dMatrix[j])
        
        # dnm is exactly as in formula
        dnm = dMatrix[i][j]
        Mnm = (n-2)*dnm - Rn - Rm
        
        # assigns lowest Mnm value to a node
        if (minM is None) or (Mnm < minM):
            minM = Mnm
            joinPair = [i, j]
            
    return joinPair

def njDistToPair(dMatrix, i, j):
    n = len(dMatrix)
    row = dMatrix[i]
    col = dMatrix[j]
    
    dist = dMatrix[i][j] + (sum(row) - sum(col))/(n-2)
    dist *= 0.5
    
    return dist

def njTree(dMatrix):
    joinOrder = []
    n = len(dMatrix)
    tree = list(range(n)) # only need list() if using Python 3
    
    '''
    This loop continues while the length of the distance matrix is 
    greater than two. Each time we go through the loop a new branch
    point is defined and the length of the distance matrix will
    decrease by one. When there are only two tree parts to join, 
    there are no more choices to be made.
    '''
    
    '''
    Inside this loop, we use the njPair() function defined above to
    determine which indices, stored here as x, y, represent the 
    closest pair and should be joined during this iteration.
    '''
    
    while n > 2:
        x, y = njPair(dMatrix) # assigns i, j to x, y
    '''
    The variable node below is defined as a tuple containing the two
    parts of the tree to be combined. These two parts correspond to
    the positions x and y (i, j) in the distance matrix and in the
    tree list. The new branch node is added to the joinOrder list and
    the tree list. To see the tree grow, print(tree) during the
    iteration.
    '''     
        
    node = (tree[x], tree[y]) 
    
    joinOrder.append(node)
    tree.append(node)
    
    '''
    We then delete the x and y elements from the tree list since these
    parts have now been combined and added as the new node to the end.
    We delete the y element before the x one because we want to
    delete the largest list index first. Deleting the smaller index x
    first would shuffle the remainder of the list containing the y
    position along by one.
    '''
    
    del tree[y]
    del tree[x]
    
    '''
    Next, we adjust the distance matrix in response to the the newly
    joined positions. We first calculate the distance from the joined
    x and y positions to the new branch point using the function
    njDistToPair() as detailed above.
    '''
    
    distX = njDistToPair(dMatrix, x, y)
    distY = njDistToPair(dMatrix, y, x)
    
    '''
    A new row, containing zeros, is added to the distance matrix, which
    will later be filled with distances to the new branch point. This
    new row has one more element than the existing rows because it 
    will not be extended like the others in the following loop.
    '''
    
    dMatrix.append([0] * (n+1))
    
    '''
    We then loop through all positions in the distance matrix, except
    for the newly added one, and select those that have not been
    joined yet (not x or y). The distance from each of these positions
    to the new node is then defined as the average of the distances
    to the x, y points minus the respective distances of x and y to 
    their joining node.
    '''
    
    for i in range(n):
        if i not in (x, y):
            dist = (dMatrix[x][i] - distX) + (dMatrix[y][i] - distY)
            dist *= 0.5 # multiplies the above expression by 1/2
    
    '''
    This distance is added to the end of the distance matrix row. The
    new row (n) at the bottom has the appropriate element filled in, 
    so we have filled in the new distance values for the ends of row
    and column i.
    '''
            
    dMatrix[i].append(dist)
    dMatrix[n][i] = dist
    
    '''
    Once the loop through matrix positions is done, we will have a 
    new row and column in the distance matrix for the newly joined
    branch point. We then delete the old x and y positions from the 
    matrix. We delete two rows first and, for the remaining rows, we
    loop through and delete the appropriate two columns. At the end
    of the while loop we decrease n by one since the distance matrix
    is now one row/column smaller.
    '''
    
    del dMatrix[y]
    del dMatrix[x]
    
    for row in dMatrix:
        del row[y]
        del row[x]
        
    n -= 1
    
    '''
    We then convert the tree list to a tuple to show that the two
    remaining parts are joined since tuples are immutable. We add
    the whole tree to the list of join events. The function then 
    passes back the tree and branch combination order.
    '''
    
    tree = tuple(tree)
    joinOrder.append(tree)
    
    return tree, joinOrder

tree, treeJoinOrder = njTree(dMatrix)

print(tree)