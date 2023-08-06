class Factor():
    # TODO
    # column name in kwargs
    """
    Factor is a class defining technical feature's factor.

    Examples
    --------
    >>> Factor(name="001", method="sma", column_name="close", window_size=2)
    """

    def __init__(self, name, **kwargs):
        self.name = name
        for i in kwargs:
            setattr(self, i, kwargs[i])

    def __str__(self) -> str:
        return self.name
