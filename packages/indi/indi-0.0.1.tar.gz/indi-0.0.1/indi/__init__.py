__version__ = "0.0.1"


# define fitting methods
# note the sample splits are aligned using random_state=0
import scipy
import xgboost
import sklearn
import shap
import numpy as np

def fit_raw_regression(X, y, max_depth=1, learning_rate=0.02, sample_weight=None, verbose=None):
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, sample_weight, random_state=0)
    model = xgboost.XGBRegressor(n_estimators=50000, max_depth=max_depth, learning_rate=learning_rate, subsample=0.5)
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], early_stopping_rounds=20, verbose=verbose)
    return model

def fit_raw_classification(X, y, max_depth=1, learning_rate=0.02, sample_weight=None, verbose=None):
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, sample_weight, random_state=0)
    model = xgboost.XGBClassifier(n_estimators=50000, max_depth=max_depth, learning_rate=learning_rate, subsample=0.5)
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], early_stopping_rounds=20, verbose=verbose)
    return model

def fit_residual(X, y, base_margin, max_depth=1, learning_rate=0.02, sample_weight=None, verbose=None):
    parts = sklearn.model_selection.train_test_split(X, y, base_margin, random_state=0)
    X_train, X_test, y_train, y_test, base_margin_train, base_margin_test = parts
    model = xgboost.XGBClassifier(
        n_estimators=50000,
        max_depth=max_depth,
        learning_rate=learning_rate,
        subsample=0.5,
        use_label_encoder=False
    )
    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        early_stopping_rounds=100,
        verbose=verbose,
        base_margin=base_margin_train,
        base_margin_eval_set=[base_margin_test],
        eval_metric="logloss"
    )
    return model

def direct_effects(features, X, y, children_margins=None, learning_rate=0.05, verbose=None):
    """ Here we learn the direct effect of a set of features on the output.
    
    To learn the direct effects of the features on the output we control for all the
    other features in X. We also allow children margins to be passed in that represent
    lower level direct effects that we don't need to relearn. So we try to learn the
    direct effects that are not already encoded in children_margins.
    
    Parameters:
    ===========
    features : list[str]
        The set of features we will learn a di
    """
    
    if children_margins is None:
        children_margins = np.zeros(len(y))
    
    # note that it is important that we set this base score so that we don't have to
    # relearn the base rate each time we train a model. This relearning won't hurt
    # predictive performance but it can cause us to put credit on features that does
    # not belong there (since it really just about the base value)
    base_score = scipy.special.logit(y.mean())

    # if we are learning the effects of all features then we 
    if len(features) == X.shape[1]:
        control_margins = np.ones(len(y)) * base_score
    else:
        model = fit_residual(X.drop(features, axis=1), y, np.ones(len(y)) * base_score, learning_rate=learning_rate, verbose=verbose)
        control_margins = model.predict(X.drop(features, axis=1), output_margin=True) + np.ones(len(y)) * base_score

    model_residual = fit_residual(X[features], y, control_margins + children_margins, max_depth=1, learning_rate=learning_rate, verbose=verbose)
    return model_residual