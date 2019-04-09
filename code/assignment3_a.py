import mathlib.utils
import mathlib.integrate
import mathlib.minimize as minimize
import mathlib.interpolate3D
import matplotlib.pyplot as plt
import numpy as np

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
    
    # Go through each file and find the optimum.
    for file in ['satgals_m15.txt', 'satgals_m14.txt', 'satgals_m13.txt',
                 'satgals_m12.txt', 'satgals_m11.txt']:


        # Read the file with halos and create a super halo.
        super_halo = np.loadtxt(file, skiprows=4)[:, 0] 

        # The number of satelites in the super halo.
        Nsat = len(super_halo)

        # A wrapper around the likelihood function. This is used
        # function that doesn't deppand on Nsat and super halo.
        likelihood_wrapper = lambda a, b, c: likelihood(Nsat, super_halo, a, b, c)       
        
        # Find the optimal values.
        a_opt, b_opt, c_opt = minimize.downhill_simplex(likelihood_wrapper,
                                                        [1.1, 1.3, 3.1],
                                                         max_iters=200)
      
        # Print the file and the output.
        print('File: {0} a_opt:{1:.5f} b_opt:{2:.5f} c_opt:{3:.5f}'
              .format(file, a_opt, b_opt, c_opt))

      
        # Plot the results  for the optimal found values.
        bins = np.logspace(-4, np.log10(5), 21)
        x = np.linspace(min(super_halo), 5, 100)
        
        plt.plot(x, N(Nsat,x,a_opt,b_opt,c_opt)/Nsat ,
                 c = 'red', label = 'Model')
        plt.hist(super_halo, bins= bins, density = True,
                 label = 'Data', edgecolor = 'black')

        plt.xlim(min(super_halo)/5, max(super_halo)*30)
        plt.ylim(bottom=10**(-20), top=10)
        plt.legend(framealpha=1, loc= 1)
        plt.loglog()
        plt.savefig('./plots/' + file[0:-4] + '.pdf')
        plt.figure()


        





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

