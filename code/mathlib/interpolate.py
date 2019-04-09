import numpy as np

def _find_bisection_idx(x_vals, points, x): 
    """
        Find the index of the point that is the closest to x from the left
        in the provided array of known x points.
        
    In: 
        param: x_vals -- The known x value's.
        param: points -- The minimum number of required points
                         that are needed to interpolate. For example 2 
                         when using linear interpolation.
        param: x -- The point to find the closest point for.
    Out:
        return: The index of the closest known point that is left of x, 
                corrected by the minimum number of required points needed
                for interpolation.
    
    """


    # Index of known point of the right.
    edge_right_idx = len(x_vals) - 1 
    # Index of known point of the left. 
    edge_left_idx = 0                
    # Index of the known point in the center of the left and right point.
    edge_mid_idx = 0                  
        
    # While the known left and right point are not separated
    # by known points, perform bisection. 
    while edge_right_idx - edge_left_idx > 1:  

        # Use the left and right index to find the index 
        # of the point in the center.
        edge_mid_idx = (edge_right_idx + edge_left_idx) >> 1 

        # Is the point x left of the point in the middle?
        if x_vals[edge_mid_idx] > x: #True -> set right index to middle
            edge_right_idx = edge_mid_idx
        else: #False, set left index to middle index
            edge_left_idx = edge_mid_idx
            

    # The point is now found, the interpolation might need
    # need a minimum of point 'points' for interpolation. If there are not 
    # enough points on the right of the left_index then decrease the index 
    # until there are enough.

    # Not enough points because the left point is to far to the right.
    if edge_left_idx + points > len(x_vals): 

        # Move to the left until there are enough points.
        while edge_left_idx + points > len(x_vals): 
            edge_left_idx -= 1
            
        # Not enough points in the dataset.
        if edge_left_idx < 0: 
            raise "Dataset is to small to interpolate x. Not enough points"
            
        return edge_left_idx
    else: # Enough points are available
        return edge_left_idx  



def interpolate_linear(x_vals, y_vals, x):
    """
            Perform linear interpolation
    
    In:
        param: x_vals -- The known x values.
        param: y_vals -- The known y values.
        param: x -- The point to linear interpolate using the known values.
    
    Out:
        return: The interpolated y value for x.
    """

    # Find the index of the closest known value to the left of x.
    idx = _find_bisection_idx(x_vals, 2, x) 

    # Horizontal line, no need to interpolate.
    if y_vals[idx] == y_vals[idx+1]: 
        return y_vals[idx]

     # Linear interpolate.
    else:

        # Find the slope between the points x_{idx} and x_{idx} + 1
        a = (y_vals[idx+1] - y_vals[idx])/(x_vals[idx+1] - x_vals[idx])
        
        # Find the intersect.
        b =  y_vals[idx] - a*x_vals[idx]

        # Linear interpolate the point x.
        return a*x + b


def interpolate_neville(x_vals, y_vals, x):
    """
        Perform polynomial interpolation using Neveille's algorithm
    
       In:
        param: x_vals -- The known x values.
        param: y_vals -- The known y values.
        param: x -- The point to linear interpolate using the known values
    
    Out:
        return: The interpolated y value for x.
    """

    
    # Number of x values.
    values = len(x_vals)
      
    # The array that contains the initial polynomial values.
    initials = np.zeros(values) 


    # Combine the evaluations of order 'order' to approximate
    # the higher order polynomial. Store the results in the 
    # array with the initial values.
    for order in range(0, values): 

        # Each order had one less element. Combine them to approximate
        # the higher order polynomial.
        for element_idx in range(values - order): 
            # The very first time set the initial values.
            if order == 0:
                initials[element_idx] = y_vals[element_idx]
            else:
                top = (x_vals[order+ element_idx] - x)* initials[element_idx] 
                top += (x - x_vals[element_idx])*initials[element_idx+1]
                bottom = x_vals[element_idx+order] - x_vals[element_idx] 
              
                initials[element_idx] = top/bottom

    return initials[0]


