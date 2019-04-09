import numpy as np
import matplotlib.pyplot as plt

def downhill_simplex(function, start, max_iters = 100, toll = 1e-10):
    """
        Try to find the minimum of the provided function
        with the help of the downhill simplex method
    In:
        param:function -- The function to minimize.
        param:start --  The best guess for the minimum.
        param:max_iters -- The maximum number of iterations to perform.
        param:toll -- The minimum tolerance for convergence.
    Out:
        return: An approximation for the minimum.
    """
    
    
    # The dimension in which we are.
    dim = len(start)
    
    # A matrix representing the vertices.
    vertices = np.zeros((dim+1, dim)) 
    vertices[0] = start #first one is start point
        
    # A matrix with function evaluations of the vertices.
    evaluations = np.zeros(dim+1)
    evaluations[0] = function(*vertices[0])

    # An array representing a direction
    # vector in our n-dimensional space.
    direction_vector = np.zeros(dim)
    
    # Create the simplex by selecting
    # vertices around the starting point.
    for i in range(1, dim+1):     
        direction_vector[i-1] = 1
        vertices[i] = start + 0.1*direction_vector
        evaluations[i] = function(*vertices[i])
        direction_vector[i-1] = 0
     
    while max_iters >= 0:
             
        max_iters -= 1
        
        # Order the vertices such that f(x_0) <= f(x_1) <= f(x_2) ... <= f(x_n).
        # Just use selection sorts, even in 50 dimensions it is just of O(2500)
        for i in range(0, vertices.shape[0]):

            # Loop over the remaining vertices
            for j in range(i+1, vertices.shape[0]):
               
                # If the function evaluation is smaller
                # at the remaining vertex, then swap the vertices
                if evaluations[j] < evaluations[i]:
                    tmp_1 = vertices[i].copy()
                    tmp_2 = evaluations[i]
                    vertices[i] = vertices[j]
                    evaluations[i] = evaluations[j]
                    vertices[j] = tmp_1              
                    evaluations[j] = tmp_2     

        # Check if error is within the tolerance.
        if (abs(evaluations[dim] - evaluations[0]))/(abs(evaluations[dim] + evaluations[0])/2) < toll:
            return vertices[0]

        # Determine the centroid.
        centroid = (1/(dim))*np.sum(vertices[0:dim], axis = 0)

        # Try a new reflected point. 
        try_point = 2*centroid - vertices[dim]
        try_eval = function(*try_point)
        
        # if f(x_0) <= f(x_try) < f(x_n)
        # then the new point is better but not the best, accept it.
        if evaluations[0] <= try_eval < evaluations[dim]:
            vertices[dim] = try_point.copy() 
            evaluations[dim] = try_eval     
            continue
            
        
        # Expansion
        
        # New point is the very best, propose 
        # a second point by expanding further in that
        # direction.
        if try_eval < evaluations[0]:
            expand = 2*try_point - centroid
            expand_eval = function(*expand)

            # Expansion is even better
            if expand_eval < try_eval:
                vertices[dim] = expand.copy()
                evaluations[dim] = expand_eval
            else:
                vertices[dim] = try_point.copy()
                evaluations[dim] = try_eval
            
            continue

        # Contraction
        
        # We now know that f(x_try) > f(x_{n-1}) and
        # therefore propose new point by contraction.
        
        try_point = (centroid + vertices[dim])/2
        try_eval = function(*try_point)

        # Is it better than the worst point?
        if try_eval < evaluations[dim]: # true
            vertices[dim] = try_point.copy()
            evaluations[dim] = try_eval
            continue
            
        # Shrink
        
        # All previous points where bad, zoom in on the best point
        # by shrinking.
        for i in range(1, dim+1):
            vertices[i] = (vertices[i]+ vertices[0])/2
            evaluations[i] = function(*(vertices[i]))
        
        
    return vertices[0]