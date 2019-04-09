import numpy as np



def newton_raphson(func, func_deriv, x_left, x_right, xacc):
    """
        Calculate the roots using the Newton-Raphson method

    In:
        param: func -- The function to calculate the roots for.
        param: func_deriv -- The derivative of the function to 
                             calculate the roots for.
        param: x_left -- The left bracket value that encloses the root.
        param: x_right -- The right bracket value that encloses the root
        param: xacc -- The accuracy to find the root with.
    
    Out:
        return: An approximation of the x coordinate of the root.
    """


    # The initial accuracy and the maximum number 
    # of iterations.
    acc = 0xFFFFFFFFF
    iters = 1e4
    
    # Make sure the left bracket value is the smallest.
    if x_left > x_right:
        raise "Left bracked value is larger than right bracked value"
    
    # Start from the center of the bracket
    result = 0.5*(x_left+x_right)
    
    # While the requested accuracy isn't reached and
    # while the maximum amount of iterations isn't reached,
    # perform Newton_Raphson
    while (acc > xacc) and (iters > 0):

        # Keep the previous result temporary in memory
        # to update the accuracy.
        old = result

        #x_i+1 = x_i - func(x_i)/func_derv(x_i)
        result -= func(result)/func_deriv(result) 
        
        # Check if we are still in the bracket
        if result < x_left or result > x_right:
            raise "Out of bracket"      
        
        # Update the accuracy
        acc = abs(abs(result) - abs(old))
        
    return result


