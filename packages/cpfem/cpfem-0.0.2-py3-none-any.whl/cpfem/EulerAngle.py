# -*- coding: utf-8 -*-


class EulerAngle:
    """The EulerAngle object defines Euler angle of a grain.

    Attributes
    ----------
    phi1: float
        1st Euler angle
    Phi: float
        2nd Euler angle
    phi2: float
        3rd Euler angle

    Notes
    -----

    """
    phi1: float = 0.
    Phi: float = 0.
    phi2: float = 0.

    def __init__(self, phi1: float = 0., Phi: float = 0., phi2: float = 0.):
        """The method creates a EulerAngle object.

        Parameters
        ----------
        phi1: float
            1st Euler angle
        Phi: float
            2nd Euler angle
        phi2: float
            3rd Euler angle

        Notes
        -----

        Returns
        -------
            A EulerAngle object.

        Raises
        ------

        """
        self.phi1 = float(phi1)
        self.Phi = float(Phi)
        self.phi2 = float(phi2)

    def setValues(self, phi1: float = 0., Phi: float = 0., phi2: float = 0.):
        """This method modifies the EulerAngle object.

        Parameters
        ----------
        phi1: float
            1st Euler angle
        Phi: float
            2nd Euler angle
        phi2: float
            3rd Euler angle

        """
        self.phi1 = float(phi1)
        self.Phi = float(Phi)
        self.phi2 = float(phi2)

    def __str__(self):
        return "{'phi1': %s, 'Phi': %s, 'phi2': %s}" % (self.phi1, self.Phi, self.phi2)
