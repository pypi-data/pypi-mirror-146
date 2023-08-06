# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""
background.py
"""

import pathlib


class Background:
    """Background Knowledge for a database.

    Background knowledge expressed in the form of modes.
    """

    # pylint: disable=too-many-instance-attributes,too-many-arguments

    def __init__(
        self,
        *,
        modes=None,
        ok_if_unknown=None,
        bridgers=None,
        ranges=None,
        number_of_clauses=100,
        number_of_cycles=100,
        recursion=False,
        line_search=False,
        use_std_logic_variables=False,
        use_prolog_variables=True,
        load_all_libraries=False,
        load_all_basic_modes=False,
    ):
        """Initialize a set of background knowledge

        Parameters
        ----------
        modes : list of str (default: None)
            Modes constrain the search space for hypotheses.
        ok_if_unknown : list of str (default: None)
            Okay if not known.
        bridgers : list of str (default: None)
            List of bridger predicates.
        ranges : dict of str (default: None)
            Dict mapping object types to discrete categories
        number_of_clauses : int, optional (default: 100)
            Maximum number of clauses in the tree (i.e. maximum number of leaves)
        number_of_cycles : int, optional (default: 100)
            Maximum number of times the code will loop to learn clauses,
            increments even if no new clauses are learned.
        line_search : bool, optional (default: False)
            Use lineSearch
        recursion : bool, optional (default: False)
            Use recursion
        use_std_logic_variables : bool, optional (default: False)
            Set the stdLogicVariables parameter to True
        use_prolog_variables : bool, optional (default: True)
            Set the usePrologVariables parameter to True
        load_all_libraries : bool, optional (default: False)
            Load libraries: ``arithmeticInLogic``, ``comparisonInLogic``,
            ``differentInLogic``, ``listsInLogic``
        load_all_basic_modes : bool, optional (default: False)
            Load ``modes_arithmeticInLogic``, ``modes_comparisonInLogic``,
            ``modes_differentInLogic``, ``modes_listsInLogic``
            These may require many cycles while proving.

        Examples
        --------

        This demonstrates how to add parameters to the Background object.
        The main thing to take note of is the ``modes`` parameter, where
        background knowledge of the Toy-Cancer domain is specified.

        >>> from srlearn import Background
        >>> bk = Background(
        ...     modes=[
        ...         "cancer(+Person).",
        ...         "smokes(+Person).",
        ...         "friends(+Person,-Person).",
        ...         "friends(-Person,+Person).",
        ...     ],
        ... )
        >>> print(bk)
        setParam: numOfClauses=100.
        setParam: numOfCycles=100.
        usePrologVariables: true.
        setParam: nodeSize=2.
        setParam: maxTreeDepth=3.
        mode: cancer(+Person).
        mode: smokes(+Person).
        mode: friends(+Person,-Person).
        mode: friends(-Person,+Person).
        <BLANKLINE>

        This Background object is used by the :class:`srlearn.rdn.BoostedRDN` class to
        write the parameters to a ``background.txt`` file before running BoostSRL.

        >>> from srlearn import Background
        >>> from srlearn.datasets import load_toy_cancer
        >>> train, _ = load_toy_cancer()
        >>> bk = Background(modes=train.modes)
        >>> bk.write("training/")   # doctest: +SKIP

        Notes
        -----

        Descriptions of these parameters are lifted almost word-for-word from the
        BoostSRL-Wiki "Advanced Parameters" page [1]_.

        Some of these parameters are defined in multiple places. This is mostly
        to follow the sklearn-style requirement for all tune-able parameters to
        be part of the object while still being relatively similar to the
        style where BoostSRL has parameters defined in a modes file.

        .. [1] https://starling.utdallas.edu/software/boostsrl/wiki/advanced-parameters/
        """
        self.modes = modes
        self.ok_if_unknown = ok_if_unknown
        self.number_of_clauses = number_of_clauses
        self.number_of_cycles = number_of_cycles
        self.line_search = line_search
        self.recursion = recursion
        self.use_std_logic_variables = use_std_logic_variables
        self.use_prolog_variables = use_prolog_variables
        self.load_all_libraries = load_all_libraries
        self.load_all_basic_modes = load_all_basic_modes
        self.bridgers = bridgers
        self.ranges = ranges

        # These parameters are stored in Background, but they're set in classifiers/regressors.
        self.node_size = 2
        self.max_tree_depth = 3

        # Check params are correct at the tail of initialization.
        self._check_params()

    def _check_params(self) -> None:
        """Runtime check that background parameters are valid.

        Structure:
            (Parameters, Tuple of valid types, Constraints on values, Message for invalid cases)
        """

        checks = (
            (self.modes, (list, type(None)), (), "'modes' should be 'None' or 'list"),
            (self.ok_if_unknown, (list, type(None)), (), "'ok_if_unknown' should be 'None' or 'list'"),
            (self.bridgers, (list, type(None)), (), "'bridgers' should be 'None' or 'list'"),
            (self.ranges, (dict, type(None)), (), "'ranges' should be 'None' or 'dict'"),
            (self.line_search, (bool,), (), "'line_search' should be 'bool'"),
            (self.recursion, (bool,), (), "'recursion' should be 'bool'"),
            (self.node_size, (int,), (lambda x: x >= 1,), "'node_size' should be 'int' >= 1"),
            (self.max_tree_depth, (int,), (lambda x: x >= 1,), "'max_tree_depth' should be 'int' >= 1"),
            (self.number_of_clauses, (int,), (lambda x: x >= 1,), "'number_of_clauses' should be 'int' >= 1"),
            (self.number_of_cycles, (int,), (lambda x: x >= 1,), "'number_of_cycles' should be 'int' >= 1"),
            (self.load_all_basic_modes, (bool,), (), "'load_all_basic_modes' should be 'bool'"),
            (self.load_all_libraries, (bool,), (), "'load_all_libraries' should be 'bool'"),
            (self.use_std_logic_variables, (bool,), (lambda x: x != self.use_prolog_variables,), "'use_std_logic_variables' should be 'bool'"),
            (self.use_prolog_variables, (bool,), (lambda x: x != self.use_std_logic_variables,), "'use_prolog_variables' is deprecated"),
        )

        for param, types, constraints, message in checks:
            if not any([isinstance(param, t) for t in types]):
                raise ValueError(message)
            for c in constraints:
                if not c(param):
                    raise ValueError(message)

    def write(self, filename="train", location=pathlib.Path("train")) -> None:
        """Write the background to disk for learning.

        Parameters
        ----------
        filename : str
            Name of the file to write to: 'train_bk.txt' or 'test_bk.txt'
        location : :class:`pathlib.Path`
            This should be handled by a manager to ensure locations do not overlap.
        """

        with open(location.joinpath("{0}_bk.txt".format(filename)), "w") as _fh:
            _fh.write(str(self))

    def _to_background_string(self) -> str:
        """Convert self to a string.

        This converts the Background object to use the background/mode syntax used
        by BoostSRL. Normally this will be accessed via the public __str__ method
        or __repr__ method.

        Parameters
        ----------
        self : object
            Instance of a Background object.

        Returns
        -------
        self : str
            A string representation of the Background object.

        Notes
        -----

        This method is based on the description and examples from the
        BoostSRL-Wiki "Basic Modes Guide" [1]_.

        .. [1] https://starling.utdallas.edu/software/boostsrl/wiki/basic-modes/
        """
        _relevant = [
            [_attr, _val]
            for _attr, _val in self.__dict__.items()
            if (_val is not False) and (_val is not None)
        ]

        _background_syntax = {
            "line_search": "setParam: lineSearch={0}.\n",
            "recursion": "setParam: recursion={0}.\n",
            "node_size": "setParam: nodeSize={0}.\n",
            "max_tree_depth": "setParam: maxTreeDepth={0}.\n",
            "number_of_clauses": "setParam: numOfClauses={0}.\n",
            "number_of_cycles": "setParam: numOfCycles={0}.\n",
            "load_all_libraries": "setParam: loadAllLibraries = {0}.\n",
            "load_all_basic_modes": "setParam: loadAllBasicModes = {0}.\n",
            "use_std_logic_variables": "useStdLogicVariables: {0}.\n",
            "use_prolog_variables": "usePrologVariables: {0}.\n",
        }

        _background = ""
        for _attr, _val in _relevant:
            if _attr in ["modes", "ok_if_unknown", "bridgers", "ranges"]:
                pass
            else:
                _background += _background_syntax[_attr].format(str(_val).lower())

        if self.modes:
            for _mode in self.modes:
                _background += "mode: " + _mode + "\n"

        try:
            if getattr(self, "ok_if_unknown"):
                for _unknown in self.ok_if_unknown:
                    _background += "okIfUnknown: " + _unknown + ".\n"
        except AttributeError:
            pass

        try:
            if getattr(self, "bridgers"):
                for _bridger in self.bridgers:
                    _background += "bridger: "  + _bridger + ".\n"
        except AttributeError:
            pass

        try:
            if getattr(self, "ranges"):
                for _range in self.ranges:
                    _background += f"range: {_range}={{" + ", ".join(self.ranges[_range]) + "}.\n"
        except AttributeError:
            pass

        return _background

    def __str__(self) -> str:
        return self._to_background_string()

    def __repr__(self) -> str:
        return self._to_background_string()
