import numpy as np
import pandas as pd
import pytest
from sklearn.exceptions import NotFittedError
from feature_engine.discretisation import DecisionTreeDiscretiser, EqualWidthDiscretiser


def test_DecisionTreeDiscretiser(dataframe_normal_dist, dataframe_vartypes, dataframe_na):
    # test case 1: classification
    transformer = DecisionTreeDiscretiser(cv=3, scoring='roc_auc', variables=None,
                                          param_grid={'max_depth': [1, 2, 3, 4]},
                                          regression=False, random_state=0)
    np.random.seed(0)
    y = pd.Series(np.random.binomial(1, 0.7, 100))
    X = transformer.fit_transform(dataframe_normal_dist, y)
    X_t = [1., 0.71, 0.93, 0.]

    # init params
    assert transformer.cv == 3
    assert transformer.variables == ['var']
    assert transformer.scoring == 'roc_auc'
    assert transformer.regression is False
    # fit params
    assert transformer.input_shape_ == (100, 1)
    # transform params
    assert len([x for x in np.round(X['var'].unique(), 2) if x not in X_t]) == 0
    assert transformer.scores_dict_ == {'var': 0.717391304347826}

    # test case 2: regression
    transformer = DecisionTreeDiscretiser(cv=3, scoring='neg_mean_squared_error', variables=None,
                                          param_grid={'max_depth': [1, 2, 3, 4]}, regression=True,
                                          random_state=0)
    np.random.seed(0)
    y = pd.Series(pd.Series(np.random.normal(0, 0.1, 100)))
    X = transformer.fit_transform(dataframe_normal_dist, y)
    X_t = [0.19, 0.04, 0.11, 0.23, -0.09, -0.02, 0.01, 0.15, 0.07,
           -0.26, 0.09, -0.07, -0.16, -0.2, -0.04, -0.12]

    # init params
    assert transformer.cv == 3
    assert transformer.variables == ['var']
    assert transformer.scoring == 'neg_mean_squared_error'
    assert transformer.regression is True
    # fit params
    assert transformer.input_shape_ == (100, 1)
    assert transformer.scores_dict_ == {'var': -4.4373314584616444e-05}
    # transform params
    assert len([x for x in np.round(X['var'].unique(), 2) if x not in X_t]) == 0

    with pytest.raises(ValueError):
        DecisionTreeDiscretiser(cv='other')

    with pytest.raises(ValueError):
        DecisionTreeDiscretiser(regression='other')

    # test case 3: raises error if target is not passed
    with pytest.raises(TypeError):
        encoder = DecisionTreeDiscretiser()
        encoder.fit(dataframe_normal_dist)

    with pytest.raises(NotFittedError):
        transformer = EqualWidthDiscretiser()
        transformer.transform(dataframe_vartypes)