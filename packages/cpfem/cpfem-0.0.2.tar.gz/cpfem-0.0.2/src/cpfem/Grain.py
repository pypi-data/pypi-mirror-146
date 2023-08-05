# -*- coding: utf-8 -*-
from EulerAngle import EulerAngle


class Grain:
    """The Grain object defines a grain.

    Attributes
    ----------
    name: str
        1st Euler angle
    eulerAngle: EulerAngle
        A :py:class:`~EulerAngle` object.

    Notes
    -----

    """
    name: str = ''
    eulerAngle: EulerAngle = EulerAngle()

    def __init__(self, name: str = '', eulerAngle: EulerAngle = EulerAngle()):
        """The method creates a Grain object.

        Parameters
        ----------
        name: str
            1st Euler angle
        eulerAngle: EulerAngle
            A :py:class:`~EulerAngle` object.

        Notes
        -----

        Returns
        -------
            A Grain object.

        Raises
        ------

        """
        self.name = name
        self.eulerAngle = eulerAngle

    def __str__(self):
        return "{'name': %s, 'eulerAngle': %s}" % (self.name, self.eulerAngle)
