"""
Neighborhood functions.

F Comitani, SG Riva, A Tangherloni 
"""

class Neighborhoods:
    """ Container class with functions to calculate neihgborhoods. """

    def __init__(self, xp=None):
        """ Instantiate the Neighborhoods class.

        Args:
            xp (numpy or cupy): the numeric labrary to use
                to calculate distances.
        """

        self.xp = xp

    def gaussian(self, center, sigma, xx, yy):
        """Returns a Gaussian centered in c on any 2d topology.
        
        Args:
            center (int): index of the center point along the xx yy grid.
            sigma (float): standard deviation coefficient.
            xx (array): x coordinates in the grid mesh.
            yy (array): y coordinates in the grid mesh.

        Returns:
            (array): the resulting neighborhood matrix.
        """

        d = 2*sigma**2

        nx = xx[self.xp.newaxis,:,:]
        ny = yy[self.xp.newaxis,:,:]
        cx = xx.T[center][:, self.xp.newaxis, self.xp.newaxis]
        cy = yy.T[center][:, self.xp.newaxis, self.xp.newaxis]

        px = self.xp.exp(-self.xp.power(nx-cx, 2)/d)
        py = self.xp.exp(-self.xp.power(ny-cy, 2)/d)

        return (px*py).transpose((0,2,1))


    def mexican_hat(self, center, std_coeff, xx, yy):
        """Mexican hat centered in c on any topology.
        
        TODO: remove compact_support and sigma

        Args:
            center (int): index of the center point along the xx yy grid.
            sigma (float): standard deviation coefficient.
            xx (array): x coordinates in the grid mesh.
            yy (array): y coordinates in the grid mesh.

        Returns:
            (array): the resulting neighborhood matrix.
        """

        d = 2*sigma**2

        nx = xx[self.xp.newaxis,:,:]
        ny = yy[self.xp.newaxis,:,:]
        cx = xx.T[center][:, self.xp.newaxis, self.xp.newaxis]
        cy = yy.T[center][:, self.xp.newaxis, self.xp.newaxis]

        px = self.xp.power(nx-cx, 2)
        py = self.xp.power(ny-cy, 2)

        p = px + py
        
        return (self.xp.exp(-p/d)*(1-2/d*p)).transpose((0,2,1))

    def bubble(self, center, sigma, neigx, neigy):
        """Constant function centered in c with spread sigma,
        which should be an odd value.
        
        TODO: remove compact_support

        Args: 
            center (int): center point along the xx yy grid.
            sigma (float): spread coefficient.
            neigx (array): coordinates along the x axis.
            neigy (array): coordinates along the y axis.

        Returns:
            (array): the resulting neighborhood matrix.
        """
        
        nx = neigx[self.xp.newaxis,:]
        ny = neigy[self.xp.newaxis,:]
        cx = center[0][:,self.xp.newaxis]
        cy = center[1][:,self.xp.newaxis]

        ax = self.xp.logical_and(nx > cx-sigma,
                            nx < cx+sigma)
        ay = self.xp.logical_and(ny > cy-sigma,
                            ny < cy+sigma)

        return (ax[:,:,self.xp.newaxis]*ay[:,self.xp.newaxis,:])