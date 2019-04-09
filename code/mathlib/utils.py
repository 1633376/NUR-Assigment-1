import mathlib.sorting
import numpy as np

def factorial(number):
    """
        Calculate the factorial for a number

    In:
        param: number -- The number to calculate the factorial for.
    Out:
        return: The factorial of the input number.
    """

    # If number < 20 convert it to an int64 to not lose any precision.
    # else use a np.float64. ( = lose in precision)
    # Note: Only datatypes with 64 or less bits are allowed.
    if number < 20: 
        number = np.int64(number)
    else:          
        number = np.float64(number)

    if number < 0:
        raise RuntimeError('Invalid input for factorial: {n}. \
                            Input must be larger or equal than zero.')
    elif np.int64(number) == 0: #!0 = 1
        return 1
    else:
        return number*factorial(number-1)


def poisson(average, events):
    """
        Evaluate the Poisson distribution.

    In:
        param: average -- The average number of events.
        param: events -- The number of observed events.

    Out:
        return: The evaluation of the Poisson distribution
                for the given parameters.
    """

    return (average**events * np.exp(-average))/factorial(events)


def median(array):
    """
        Determine the median of an array
    
    In:
        param: array -- The array to determine the median of.
    Out:
        return: The median of the array. 
    """

    # Create a sorted version of the array.
    sort = mathlib.sorting.merge_sort(array)
    size = len(sort)
    mid = size >> 1 

    if size % 2 == 0: # even
        # An even array doesn't have an exact mid value. We 
        # therefore give the average of the values in the mid back.
        return (sort[mid] + sort[mid- 1])/2
    else: # odd 
        return sort[mid] # Give the value in the mid 

def percentile(array, value):
    """
        Determine the 'value' percentile of the array 
        using linear interpolation.
    In:
        param: array -- The array to find the 'value' percentile for
        param: value -- A value between 0 and 1 representing the
                        wanted percentile.
    Out:
        return: The 'value' percentile of the array.
    
    """

    # Sort the array and determine the amount of elements.
    sort = mathlib.sorting.merge_sort(array) 
    elements = len(array) - 1

    # The index in the array that corresponds with the percentile.
    # This is a decimal (i.e 1.2345)
    idx_unrounded = (value*elements/100) 
    
    # The rounded index (i.e 1)
    idx_rounded = int(idx_unrounded)  

    # The decimals of the unrounded index. 
    # This indicates the place between index 'indx_rounded' 
    # and 'idx_rounded+1' at which the interpolated value 
    # should be determined to obtain the percentile.
    idx_decimals = idx_unrounded - idx_rounded  
    
    # Interpolation fails for 100th percentile, as 
    # idx_rounded+1 doesn't exists.
    if value == 100: 
        return sort[elements]

    # Determine the interpolated value. 
    return idx_decimals*(sort[idx_rounded+1] - sort[idx_rounded]) + sort[idx_rounded] 

