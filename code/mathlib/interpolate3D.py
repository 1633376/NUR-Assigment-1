import numpy as np
import mathlib.interpolate as intrp

class Interpolate3D(object):
    """
        A class representing a 3D interpolator. 
    """

    def __init__(self, tensor, ranges):
        """
            Create a new instance of the 3D interpolator.

        param: tensor -- A tensor containing the known y = f(a,b,c) values
        param: ranges -- A matrix containing the a, b and c values of the tensor.
        """

        self._tensor = tensor

        # Unpack the a, b, c values.
        self._row_ranges = ranges[0] 
        self._column_ranges = ranges[1]
        self._depth_ranges = ranges[2]


    def interpolateLin(self, a, b, c):
        """
            Estimate the point y = f(a, b, c) using linear interpolation.

        In:
            param: a    The a coordinate to interpolate for.
            param: b    The b coordinate to interpolate for.
            param: c    The c coordinate to interpolate for.
        Out:
            return: An approximation for the value y = f(a, b, c)
        """

        """
            For linear interpolating we first find the cube that encloses 
            the point c_1 = f(a, b, c). (see cube below).
            This is done by finding the indices of the known (a, b, c) values 
            that correspond to the left top corner of the cube (point 500). 
            Knowing these indices the indices of the other corners 
            can easily be found. 

            To find the value c_1 we now first interpolate over the 'b' dimension
            to obtain the points x_1, x_4, x_2, x_3. These points are then used 
            to interpolate over the c dimension to obtain y_1 and y_2. 
            Finally we use y_1 and y_2 to obtain the asked point c_1.
        
            Note: You don't necessary have to interpolate the b dimension first.
                  You can start with any dimension you want.
               
               800----x_4-------700
               / |     /       / |
              /  |   y_1      /  |
             /   |   /|      /   |
            500-----x_1-----600  |
            |    |    |      |   |
            |    |    C_1    |   |
            |   300---|x_3---|--400
            |  /      |/     |  /
            | /       y_2    | /
            |/       /       |/  
           000------x_2------100 
        """

        # Indices of the left top coorner of the cube. 
        a_idx = self._find_closest_smaller(a, self._row_ranges)
        b_idx = self._find_closest_smaller(b, self._column_ranges)
        c_idx = self._find_closest_smaller(c, self._depth_ranges)

        # Interpolate b dimension between 
        # [500, 600] for x_1, 
        # [000, 100] for x_2,
        # [800, 700] for x_4 
        # and [300, 400] for x_3.
        x_1 = intrp.interpolate_linear(self._column_ranges[b_idx:b_idx+2],
                            self._tensor[a_idx][b_idx:b_idx+2][:,c_idx],
                            b)
        x_2 = intrp.interpolate_linear(self._column_ranges[b_idx:b_idx+2], 
                            self._tensor[a_idx+1][b_idx:b_idx+2][:,c_idx],
                            b)
        x_3 = intrp.interpolate_linear(self._column_ranges[b_idx:b_idx+2],
                            self._tensor[a_idx+1][b_idx:b_idx+2][:,c_idx+1],
                            b)
        x_4 = intrp.interpolate_linear(self._column_ranges[b_idx:b_idx+2],
                            self._tensor[a_idx][b_idx:b_idx+2][:,c_idx+1],
                            b)


        # Next interpolate the 'c' dimension 
        # between [x_1,x_4] for y_1 and [x_2,x_3] y_2. 
        y_1 = intrp.interpolate_linear(self._depth_ranges[c_idx:c_idx+2],
                                       np.array([x_1,x_4]), c)
        y_2 = intrp.interpolate_linear(self._depth_ranges[c_idx:c_idx+2],
                                       np.array([x_2,x_3]), c)
 
        # Finally interpolate the 'a' dimension
        # between [y_1, y_2] to obtain the final result.
        ret = intrp.interpolate_linear(self._row_ranges[a_idx:a_idx+2],
                                       np.array([y_1, y_2]), a)

        return ret


    def _find_closest_smaller(self, value, array):
        """
            Find the closest index of the known value's in the array 'array'
            that is at the left of 'value'. 

        In:
            param: value -- The value to find the closest index for.
            param: array -- The array in which to find the closest index 
                            (must be sorted)
                            
        Out:
        	return: The closest index of the known value's in the array
            that is at the left of 'value'. 
        """

        # The index of the closest value.
        closest_idx = 0     
        # The difference between value and the current closest value.
        closest_diff = 0xFFFFFFFFF  

        # Go through each element in the array.
        for idx, array_value in enumerate(array): 

            # If the difference between value and array_value is smaller, 
            # then the new closest value is found.
            # Update the difference and the index in this case.
            if abs(array_value - value) < closest_diff:
                closest_diff = abs(array_value - value)
                closest_idx = idx 


        # If the closest idx is zero then there is no index smaller.
        if closest_idx == 0:
            return closest_idx

        # We want the index left. Thus, if the found value is slightly larger
        # then return the index of the found value - 1.
        # The factor 1e-7 is to correct for rounding errors.
        if array[closest_idx] + 1e-7 >= value: 
            return closest_idx - 1
        else:
            return closest_idx     
        
  