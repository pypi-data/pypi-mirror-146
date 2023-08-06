# Copyright © 2020 Alexander L. Hayes

"""
Tests for srlearn.rdn.feature_importances_
"""

import pytest
from srlearn.rdn import BoostedRDNClassifier
from srlearn.background import Background
from srlearn.datasets import load_toy_cancer


def test_feature_importances_before_fit():
    """Test that one cannot get feature importances before fit."""
    rdn = BoostedRDNClassifier()
    with pytest.raises(ValueError):
        rdn.feature_importances_


def test_feature_importances_toy_cancer():
    """Test getting the feature importances from the Toy-Cancer set."""
    train, _ = load_toy_cancer()
    bkg = Background(modes=train.modes)
    rdn = BoostedRDNClassifier(
        target="cancer",
        background=bkg,
        n_estimators=10,
    )
    rdn.fit(train)
    _features = rdn.feature_importances_
    assert _features.most_common(1)[0] == ("smokes", 10)
