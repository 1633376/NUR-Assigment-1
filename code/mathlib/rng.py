import numpy as np

class RNG():
    """
        A class representing a random number generator (RNG)
    """

    def __init__(self, seed):
        """
            Create a new instance of the random number generator.
        
        In:
            param: seed -- The seed of the random number generator.
                           This must be an positive integer.
        """

        self._seed = seed
        self._uint32_max = 0xFFFFFFFF  
        
        # The values for the Linear congruential generator.
        self._lgc_a = 0xBEEF         
        self._lgc_c = 0xBADC0DE
        self._lgc_m = 0xFFFFFFFF

        # The values for the Xor shift.
        self._xor_a1 = 3
        self._xor_a2 = 29
        self._xor_a3 = 7

        # The values for the multiply with carry.
        self._mwc_a = 0xFFFFFFF


    def get_seed(self):
        """ 
            Get the current seed. 

        Out:
            return: The current seed of the generator.
        """
        return self._seed

    def gen_next_int(self):
        """ 
            Generate a pseudo random unsigned integer.

        Out:
            return: A pseudo random unsigned integer,
        """
        return self._gen_next()      

    def gen_next_float(self):
        """ 
            Generate a random float between 0 and 1.
        
        Out:
            return: A pseudo random float between 0 and 1.
        """
        return self._gen_next() * (1.0 / self._uint32_max)

    def gen_next_floats(self, amount):
        """ 
            Generate multiple random floats
            between 0 and 1.
        In:
            param: amount -- The amount of floats to generate.
        Out:
            return: An array with 'amount' random floats 
                    between 0 and 1.
        """

        samples = np.zeros(amount)

        for i in range(amount):
            samples[i] = self.gen_next_float()

        return samples

    def gen_next_float_range(self, low, high):
        """
            Generate a float in a specific range.
        
        In:
            param: low -- The lowest possible value to generate.
            param: high -- The highest possible value to generate.
        Out:
            return: A float in the range low, high.
        """

        ret = self.gen_next_float()
        return  ret* (high-low) + low

    def gen_next_floats_range(self, low, high, amount):
        """
            Generate multiple floats in a specific range.

         In:
            param: low -- The lowest possible value to generate.
            param: high -- The highest possible value to generate.
            param: amount -- The amount of floats to generate.
        Out:
            return: An array of floats in the range low, high
        """

        floats = self.gen_next_floats(amount)
        return floats * (high - low) + low 
        
   
    def _LCG(self, number):
        """ 
            Execute the linear congurential algorithm (LGC) on the 
            provided number.

        In:
            param: number -- The number to execute the LCA on. 
        Out:
            return: The number produced by the LCA.
         """
        return (self._lgc_a*number + self._lgc_c ) % self._lgc_m
    
    def _XOR_shift(self, number):
        """ 
            Execute the XOR-shift algorithm on the 
            input number.
        In:
            param: number -- The number to XOR-shift.
        Out:
            return: The number produced by XOR-shift.
         """

        # Shift to the right and then bitwise xor.
        number ^= (number >> self._xor_a1) 
        # Shift to the left and then bitwise xor.
        number ^= (number << self._xor_a2) 
        # Shift to the right and then bitwise xor.
        number ^= (number >> self._xor_a3) 

        return number

    def _mwc(self, number):
        """
           Perform multiply with carry (MWC) on
           the given input.
        In:
            param: number -- The number to perform MWC on. 
        Out:
            return The new number.
        """
        return self._mwc_a * (number & (self._uint32_max -1)) + (number >> 32)

    def _gen_next(self):
        """
            Generate the next pseudo random value 
            and update the seed.
        """
        
        old_seed = self._seed 

        self._seed = self._XOR_shift(old_seed)
        self._seed ^= self._LCG(old_seed)
        self._seed -= self._mwc(old_seed) 

        # Only keep the last 32 bits to prevent number becoming to large.
        self._seed &= self._uint32_max      
        
        return abs(self._seed) 

    def rejection_sampling(self, sample_dist, encl_func, \
                           encl_unif_transf, samples):
        """
            Perform rejection sampling.
        
        In:
            param: sample_dist -- The distribution to sample from.
            param: encl_func -- The function that encloses the distribution. 
                                This is the distribution that is chosen to 
                                enclose the sample distribution multiplied 
                                by a scalar x so that 
                                sample_dist(x) < enclosing_func(x) for x in
                                the intervall of which the distribution holds.

            param: encl_unf_transf -- The transformation that transforms a 
                                      uniform distributed variable
                                      between 0 and 1 to a variable
                                      distributed according to the chosen 
                                      enclosing distribution. 
            param: samples -- The amount of samples to sample from 'sample_dist'.

        Out:
            return: An array of 'samples' samples sampled 
                    from 'sample_dist'.
        """
        
        # An array that stores the generated samples.
        ret = np.zeros(samples)

        # While there are still samples to sample
        while samples > 0: 

            # Generate a uniform variable between 0 and 1.
            uniform = self.gen_next_float() 

            # Transform it to a variable distributed 
            # by the enclosing distribution.
            transformed_x = encl_unif_transf(uniform) 

            # Generate a random uniform variable between 
            # 0 and the height of the enclosing function 
            # evaluated at transformed_x.
            # Note: enclosing functions = enclosing distribution * scalar
            transformed_y = self.gen_next_float_range(0, \
                                                      encl_func(transformed_x))

            # If the generated y value is within the distribution 
            # to sample from, then a sample is found.
            if transformed_y <= sample_dist(transformed_x):
                ret[samples-1] = transformed_x
                samples -= 1  #1 sample less to find.

        return ret


    def gen_uniform_spherical_surface_coords(self, samples):
        """
            Generate pairs of angles phi and theta uniform 
            distributed around the surface of a sphere.
            Phi is the declination and theta is the ascension.
        
        In:
            param: samples -- The amount of angle pairs to generate.
        Out:
            return: An array containing 'samples' pairs 
                    of angles theta and phi that are 
                    uniform distributed around the
                    surface of a sphere
        """

        # Transformations from a uniform variable between 0 and 1
        # to uniformly distributed angles around the unit sphere.
        theta_transf = lambda x : np.arccos(1-2*x)
        phi_transf = lambda x : 2*np.pi*x

        # Generate 'samples' uniform floats.
        samples_gen = self.gen_next_floats(samples)

        # Generate the uniform distributed angles.
        return theta_transf(samples_gen), phi_transf(samples_gen)