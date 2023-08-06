# Copyright © 2017, 2018, 2019 Alexander L. Hayes

"""
Base class for Boosted Relational Models
"""

from collections import Counter
import inspect
import json
import logging
import warnings

from sklearn.utils.validation import check_is_fitted
import subprocess

from .background import Background
from .system_manager import FileSystem
from .utils._parse_trees import parse_tree
from ._meta import __version__


warnings.simplefilter("default")


class BaseBoostedRelationalModel:
    """Base class for deriving boosted relational models

    This class extends :class:`sklearn.base.BaseEstimator` and
    :class:`sklearn.base.ClassifierMixin` while providing several utilities
    for instantiating a model and performing learning/inference with the
    BoostSRL jar files.

    .. note:: This is not a complete treatment of *how to derive estimators*.
        Contributions would be appreciated.

    Examples
    --------

    The actual :class:`srlearn.rdn.BoostedRDNClassifier` is derived from this class, so this
    example is similar to the implementation (but the actual implementation
    passes model parameters instead of leaving them with the defaults).
    This example derives a new class ``BoostedRDNClassifier``, which inherits the default
    values of the superclass while also setting a 'special_parameter' which
    may be unique to this model.

    All that remains is to implement the specific cases of ``fit()``,
    ``predict()``, and ``predict_proba()``.
    """

    def __init__(
        self,
        *,
        background=None,
        target="None",
        n_estimators=10,
        node_size=2,
        max_tree_depth=3,
        neg_pos_ratio=2,
        solver = None,
    ):
        """Initialize a BaseEstimator"""
        self.background = background
        self.target = target
        self.n_estimators = n_estimators
        self.neg_pos_ratio = neg_pos_ratio

        if solver is None:
            warnings.warn(
                "solver='BoostSRL' will default to solver='SRLBoost' in 0.6.0"
                ", pass one or the other as an argument to suppress this warning.", FutureWarning)
            self.solver = "BoostSRL"
        else:
            if solver not in ("BoostSRL", "SRLBoost"):
                raise ValueError("`solver` must be 'SRLBoost' or 'BoostSRL'")
            self.solver = solver

        if isinstance(background, Background):
            self.node_size = node_size
            self.max_tree_depth = max_tree_depth

    @property
    def node_size(self):
        return self.background.node_size

    @node_size.setter
    def node_size(self, value):
        self.background.node_size = value

    @property
    def max_tree_depth(self):
        return self.background.max_tree_depth

    @max_tree_depth.setter
    def max_tree_depth(self, value):
        self.background.max_tree_depth = value

    @classmethod
    def _get_param_names(cls):
        # Based on `scikit-learn.base.BaseEstimator._get_param_names`
        # Copyright Gael Varoquaux, BSD 3 clause
        signature = inspect.signature(cls)
        parameters = [
            p
            for p in signature.parameters.values()
            if p.name != "self" and p.kind != p.VAR_KEYWORD
        ]
        for p in parameters:
            if p.kind == p.VAR_POSITIONAL:
                raise RuntimeError(
                    "Oh no."
                )

        return sorted([p.name for p in parameters])

    def _check_params(self):
        """Check validity of parameters. Raise ValueError if errors are detected.

        If all parameters are valid, instantiate ``self.file_system`` by
        instantiating it with a :class:`srlearn.system_manager.FileSystem`
        """

        checks = (
            (
                self.target,
                (str,),
                (lambda x: x != "None",),
                "'target' must be a string and cannot be 'None'",
            ),
            (
                self.background,
                (Background,),
                (),
                "'background' must be a Background instance",
            ),
            (
                self.n_estimators,
                (int,),
                (
                    lambda x: not isinstance(x, bool),
                    lambda x: x >= 1,
                ),
                "'n_estimators' must be an 'int' >= 1",
            ),
            (
                self.neg_pos_ratio,
                (int, float),
                (lambda x: not isinstance(x, bool), lambda x: x >= 1.0),
                "'neg_pos_ratio' must be 'int' or 'float'",
            ),
        )

        for param, types, constraints, message in checks:
            if not any([isinstance(param, t) for t in types]):
                raise ValueError(message)
            for c in constraints:
                if not c(param):
                    raise ValueError(message)

        # If all params are valid, allocate a FileSystem:
        self.file_system = FileSystem()

    def to_json(self, file_name) -> None:
        """Serialize a learned model to json.

        Parameters
        ----------
        file_name : str (or pathlike)
            Path to a saved json file.

        Notes / Warnings
        ----------------

        Intended for locally saving/loading.

        .. warning::

            There could be major changes between releases, causing old model
            files to break."""
        check_is_fitted(self, "estimators_")

        with open(
            self.file_system.files.BRDNS_DIR.joinpath(
                "{0}.model".format(self.target)
            ),
            "r",
        ) as _fh:
            _model = _fh.read().splitlines()

        model_params = {
            "background": dict(self.background.__dict__.items()),
            "target": self.target,
            "n_estimators": self.n_estimators,
            "node_size": self.node_size,
            "max_tree_depth": self.max_tree_depth,
            "neg_pos_ratio": self.neg_pos_ratio,
        }

        with open(file_name, "w") as _fh:
            _fh.write(
                json.dumps(
                    [
                        __version__,
                        _model,
                        self.estimators_,
                        model_params,
                        self._dotfiles,
                    ]
                )
            )

    def from_json(self, file_name):
        """Load a learned model from json.

        Parameters
        ----------
        file_name : str (or pathlike)
            Path to a saved json file.

        Notes / Warnings
        ----------------

        Intended for locally saving/loading.

        .. warning::

            There could be major changes between releases, causing old model
            files to break. There are also *no checks* to ensure you are
            loading the correct object type.
        """

        with open(file_name, "r") as _fh:
            params = json.loads(_fh.read())

        if params[0] != __version__:
            logging.warning(
                "Version of loaded model ({0}) does not match srlearn version ({1}).".format(
                    params[0], __version__
                )
            )

        _model = params[1]
        _estimators = params[2]
        _model_parameters = params[3]

        try:
            self._dotfiles = params[4]
        except IndexError:
            self._dotfiles = None
            logging.warning(
                "Did not find dotfiles during load, srlearn.plotting may not work."
            )

        _bkg = Background()
        _bkg.__dict__ = _model_parameters["background"]

        # 1. Loop over all class attributes of `BaseBoostedRelationalModel`
        #    except `background`, `node_size`, and `max_tree_depth`, which are
        #    handled by `Background` objects.
        # 2. Update an `_attributes` dictionary mapping attributes from JSON
        # 3. *If a key was not present in the JSON*: set it to the default value.
        # 4. Initialize self by unpacking the dictionary into arguments.
        _attributes = {
            "background": _bkg,
            "node_size": _model_parameters["node_size"],
            "max_tree_depth": _model_parameters["max_tree_depth"],
        }
        for key in set(BaseBoostedRelationalModel()._get_param_names()) - {"background", "node_size", "max_tree_depth"}:
            _attributes[key] = _model_parameters.get(
                key,
                BaseBoostedRelationalModel().__dict__[key],
            )
        self.__init__(**_attributes)

        self.estimators_ = _estimators

        # Currently allocates the File System.
        self._check_params()

        self.file_system.files.TREES_DIR.mkdir(parents=True)

        with open(
            self.file_system.files.BRDNS_DIR.joinpath(
                "{0}.model".format(self.target)
            ),
            "w",
        ) as _fh:
            _fh.write("\n".join(_model))

        for i, _tree in enumerate(_estimators):
            with open(
                self.file_system.files.TREES_DIR.joinpath(
                    "{0}Tree{1}.tree".format(self.target, i)
                ),
                "w",
            ) as _fh:
                _fh.write(_tree)

        return self

    @property
    def feature_importances_(self):
        """
        Return the features contained in a tree.

        Parameters
        ----------

        tree_number: int
            Index of the tree to read.
        """
        check_is_fitted(self, "estimators_")

        features = []

        for tree_number in range(self.n_estimators):
            _rules_string = self.estimators_[tree_number]
            features += parse_tree(
                _rules_string, (not self.background.use_std_logic_variables)
            )
        return Counter(features)

    def _get_dotfiles(self):
        dotfiles = []
        for i in range(self.n_estimators):
            with open(
                self.file_system.files.DOT_DIR.joinpath(
                    "WILLTreeFor_" + self.target + str(i) + ".dot"
                )
            ) as _fh:
                dotfiles.append(_fh.read())
        self._dotfiles = dotfiles

    def _check_initialized(self):
        """Check for the estimator(s), raise an error if not found."""
        check_is_fitted(self, "estimators_")

    @staticmethod
    def _call_shell_command(shell_command):
        """Start a new process to execute a shell command.

        This is intended for use in calling jar files. It opens a new process and
        waits for it to return 0.

        Parameters
        ----------
        shell_command : str
            A string representing a shell command.

        Returns
        -------
        None
        """

        _pid = subprocess.Popen(shell_command, shell=True)
        _status = _pid.wait()
        if _status != 0:
            raise RuntimeError(
                "Error when running shell command: {0}".format(shell_command)
            )

    def fit(self, database):
        raise NotImplementedError

    def predict(self, database):
        raise NotImplementedError

    def predict_proba(self, database):
        raise NotImplementedError

    def __repr__(self):
        params = self._get_param_names()
        params.remove("max_tree_depth")
        params.remove("node_size")
        params = ", ".join([str(param) + "=" + repr(self.__dict__[param]) for param in params])
        return (
            self.__class__.__name__
            + f"({params})"
        )
