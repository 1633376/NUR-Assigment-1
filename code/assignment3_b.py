import numpy as np
import matplotlib.pyplot as plt
import mathlib.interpolate3D

# The a,b,c found in the previous assigment for
# m11, m12, m13, m14, m15.
abc_values = np.array([[1.28368, 1.14960, 3.33632],
              [1.54045, 0.94998, 3.74252],
              [1.40908, 0.85051, 3.20000],
              [1.61791, 0.74704, 3.48682],
              [1.60000, 0.94610, 2.90000]])

# Massa's of the halo's in suns masses.
masses = [10e11, 10e12, 10e13, 10e14, 10e15]


#The 3D interpolator for the normalization constant
interpolator = None

def main():
    global interpolator

    # Load the 'table' created in the previous assigment and use it
    # to create the 3d interpolator.
    table = np.load('table_2h.npy')
    # The a, b, c ranges of the 'table'. 
    ranges = [np.arange(1.1, 2.6, 0.1),
              np.arange(0.5, 2.1, 0.1), 
              np.arange(1.5, 4.1, 0.1)] 

    # Create the interpolator.
    interpolator = mathlib.interpolate3D.Interpolate3D(table, ranges)
    
    # Go through all mass bins and caclulate the flatness around the optimum
    for idx, file in enumerate(['satgals_m11.txt', 'satgals_m12.txt', 'satgals_m13.txt',
                                'satgals_m14.txt', 'satgals_m15.txt']):


        # Read the file with halos and create a super halo.
        super_halo = np.loadtxt(file, skiprows=4)[:, 0] 

        # The number of satelites in the super halo.
        Nsat = len(super_halo)

        # A wrapper around the likelihood function. This is used
        # function that doesn't deppand on Nsat and super halo.
        likelihood_wrapper = lambda a, b, c: likelihood(Nsat, super_halo, a, b, c)       
        
        # Calculate the flatness;

        # Stepsize
        h = 0.1
        # Optimal parameters found in the previous assignment.
        a_opt, b_opt, c_opt = abc_values[idx]
        # Evaluation of the negative loglikelihood around the optimum
        L_opt = likelihood_wrapper(a_opt, b_opt, c_opt)
        # Flatness
        F = 0

        # a dimension
        F += (likelihood_wrapper(a_opt + h, b_opt, c_opt) + L_opt)**2
        F += (likelihood_wrapper(a_opt - h, b_opt, c_opt) + L_opt)**2
      
        # b dimension
        F += (likelihood_wrapper(a_opt, b_opt + h, c_opt) + L_opt)**2
        F += (likelihood_wrapper(a_opt, b_opt -h, c_opt) + L_opt)**2

        # c dimension
        F += (likelihood_wrapper(a_opt, b_opt, c_opt + h) + L_opt)**2
        F += (likelihood_wrapper(a_opt, b_opt, c_opt - h) + L_opt)**2



        # normalization
        F *= 1/(24*L_opt**2)

        # print the flatness.
      
        # Print the file and the output.
        print('File: {0} Flatness: {1:.10f}'.format(file, F))  


    # plot the points
    labels = ['a', 'b', 'c']
    colors = ['red', 'green', 'orange']
    for i in range(0, 3):
        plt.scatter(masses, abc_values[:, i], label = labels[i], c = colors[i])
    plt.loglog()
    plt.legend()
    plt.savefig('./plots/3b.pdf')


def N(Nsat, x, a, b, c):
    """
        Calculate the number of satelites on an infinite thin shell
        with radius x.

    In:
        param: Nsat -- The total number of satelites in the halo.
        param: x -- The radius of the shell.
        param: a -- The first model parameter.
        param: b -- The second model parameter.
        param: c -- The third model parameter.
    
    Out:
        return:  The number of satelites on an infinite thin shell
                 with radius x.
    """

    global interpolator
    
    return interpolator.interpolateLin(a,b,c)*b**2*(x/b)**(a-1)* np.exp(-(x/b)**c)*Nsat*4*np.pi

def likelihood(Nsat, x_values, a, b, c):
    """
        Calculate the negative loglikelihood for
        the model given the total amount of satelites,
        their x positions and the model parameters.
    
    In: 
        param: Nsat -- The total number of satelites.
        param: x_values -- The position of all the satelites.
        param: a -- The first model parameter.
        param: b -- The secon model parameter.
        param: c -- The third model parameter.

    Out:
        return: The value of the negative loglikelihood evaluated for 
                the given input.
    """


    # Only optimise within the bounded region 1 <= a <= 2.5. Values
    # outside the bounds are put at the edge.
    if a < 1:
        a = 1
    elif a > 2.5:
        a = 2.5
    
    # Only optimise within the bounded region 0.5 <= b <= 2.0 Values
    # outside the bounds are put at the edge.
    if b < 0.5:
        b = 0.5
    elif b > 2.0:
        b = 2

    # Only optimise within the bounded region 1.5 <= c <= 4. Values
    # outside the bounds are put at the edge.
    if c > 4:
        c = 4
    elif c < 1.5:
        c = 1.5

    #return the negative loglikelihood.
    return - np.sum(np.log(N(Nsat, x_values, a, b, c))) + Nsat



if __name__ == "__main__":
    # call the entry function of this script
    main()


