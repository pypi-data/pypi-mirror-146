import pandas as pd
import logging

from moosir_feature.model_validations.basic_parameter_searcher import ParameterSearcher
from moosir_feature.model_validations.benchmarking import NaiveModel, run_benchmarking
from moosir_feature.model_validations.model_validator import CustomTsCv
from moosir_feature.transformers.managers.feature_manager import FeatureCreatorManager
from moosir_feature.model_validations.model_cv_runner import predict_on_cv

from moosir_feature.transformers.managers.settings import IndicatorTargetSettings, IndicatorFeatureSettings, \
    IndicatorLagSettings

from sklearn.dummy import DummyRegressor

log = logging.getLogger(__name__)


def create_features_targets(instances: pd.DataFrame,
                            target_ind_params,
                            feature_ind_params,
                            lag_ind_params,
                            ):
    target_settings = IndicatorTargetSettings(**target_ind_params)
    feature_ind_settings = [IndicatorFeatureSettings(**feature_ind_params)]
    lag_ind_settings = [IndicatorLagSettings(**lag_ind_params)]

    fc_mgr = FeatureCreatorManager(target_settings=target_settings,
                                   feature_settings_list=feature_ind_settings,
                                   lag_settings_list=lag_ind_settings)
    features, targets, _ = fc_mgr.create_features_and_targets(instances=instances)

    return dict(features=features, targets=targets)


def run_cross_validation(features: pd.DataFrame,
                         targets: pd.DataFrame,
                         cv_search_params: dict,
                         search_params: dict,
                         metrics: list
                         ):
    log.info("searching parameters and running cross validation")

    searcher = ParameterSearcher()
    estimator = DummyRegressor(strategy="mean")

    search_result = searcher.run_parameter_search_multiple_cvs(X=features,
                                                               y=targets,
                                                               estimator=estimator,
                                                               cv_params=cv_search_params,
                                                               param_grid=search_params,
                                                               metrics=metrics,
                                                               )

    return dict(search_result=search_result)


def benchmark_best_model(features: pd.DataFrame,
                         targets: pd.DataFrame,
                         best_params: dict,
                         benchmark_cv_params: dict,
                         metrics: list
                         ):
    best_model = DummyRegressor(**best_params)

    models = [best_model, NaiveModel(targets=targets.copy(), look_back_len=1)]

    cv = CustomTsCv(train_n=benchmark_cv_params["train_length"],
                    test_n=benchmark_cv_params["test_length"],
                    sample_n=len(features),
                    train_shuffle_block_size=benchmark_cv_params["train_shuffle_block_size"])

    benchmark_result = run_benchmarking(models=models, targets=targets, features=features, cv=cv, metrics=metrics)

    return dict(benchmark_result=benchmark_result)


def train_predict_best_params(instances: pd.DataFrame,
                              target_ind_params,
                              feature_ind_params,
                              lag_ind_params,
                              best_params,
                              benchmark_cv_params):
    target_settings = IndicatorTargetSettings(**target_ind_params)
    feature_ind_settings = [IndicatorFeatureSettings(**feature_ind_params)]
    lag_ind_settings = [IndicatorLagSettings(**lag_ind_params)]

    fc_mgr = FeatureCreatorManager(target_settings=target_settings,
                                   feature_settings_list=feature_ind_settings,
                                   lag_settings_list=lag_ind_settings)

    features, targets, _ = fc_mgr.create_features_and_targets(instances=instances)

    best_model = DummyRegressor(**best_params)
    cv = CustomTsCv(train_n=benchmark_cv_params["train_length"],
                    test_n=benchmark_cv_params["test_length"],
                    sample_n=len(features),
                    train_shuffle_block_size=None)

    prediction_result = predict_on_cv(model=best_model, features=features, targets=targets, cv=cv)

    # print(prediction_result)

    return dict(prediction_result=prediction_result)

def create_alpha(instances: pd.DataFrame, prediction_result: pd.DataFrame):

    # todo: needs to be a package
    alphas = prediction_result.copy()
    alphas.columns = ["Signal"]

    alphas = alphas[alphas.index.isin(prediction_result.index)]
    alphas = pd.concat([alphas, instances], axis=1)

    # todo: just dropped na
    alphas = alphas.dropna()

    print(alphas)

    return dict(alphas=alphas)



def train_best_model(instances: pd.DataFrame,
                     target_ind_params,
                     feature_ind_params,
                     lag_ind_params,
                     best_params,
                     last_train_len: int):
    target_settings = IndicatorTargetSettings(**target_ind_params)
    feature_ind_settings = [IndicatorFeatureSettings(**feature_ind_params)]
    lag_ind_settings = [IndicatorLagSettings(**lag_ind_params)]

    fc_mgr = FeatureCreatorManager(target_settings=target_settings,
                                   feature_settings_list=feature_ind_settings,
                                   lag_settings_list=lag_ind_settings)

    features, targets, _ = fc_mgr.create_features_and_targets(instances=instances)

    best_model = DummyRegressor(**best_params)

    best_model.fit(features, targets)
    print("=" * 50)
    print("here in train again")
    print("=" * 50)

    return dict(best_model=best_model)


def inference_model(instances: pd.DataFrame, best_model: DummyRegressor, last_train_len):
    print(last_train_len)
    result = best_model.predict(instances)

    print("=" * 50)
    print("here in inference!!!")
    print("=" * 50)

    return result
