# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 15:36:08 2020

@author: s.gnodde
"""
import os
import mlflow
import logging
import pickle
import pyperclip
import datetime
from sklearn.metrics import r2_score, make_scorer, get_scorer

os.environ['FIRST_RUN'] = "True"


def mlflow_run_sklearn(
    X_train, y_train,
    X_valid, y_valid,
    model,
    check_cicd_pl_vs_local=True,
    log_model_file=True,
    filename_model_prefix="model",
    warn_devops=False,
    tracking_uri=None,
    other_parameters_to_log={},
    log_artifacts_list=None,
    run_name=None,
    score_metric="r2"
):
    """Run a model whilst tracking with MLFlow.

    Logs score, the model itself and if possible also the coefficients.

    Parameters
    ----------
    X_train : numpy.array or pandas.DataFrame
        Train set features.
    y_train : numpy.array or pandas.DataFrame
        Train set target.
    X_valid : numpy.array or pandas.DataFrame
        valid set features.
    y_valid : numpy.array or pandas.DataFrame
        valid set target.
    model : sklearn model object
        The model that is run.
    check_cicd_pl_vs_local : bool, optional
        If true, check whether run on pipeline or local. The default is True.
    log_model_file : bool, optional
        Log a Pickle of the model when True.
        Default value is True.
    filename_model_prefix : str, optional
        Prefix of the model file when log_model_file=True.
        Function appends date and time to make filename unique.
        The default is 'model'.
    warn_devops : bool, optional
        If True, warns when not running on DevOps pipeline.
        The default value is False.
    tracking_uri : str or None, optional
        Tracking uri. If None, gets is from current experiment.
    other_parameters_to_log : dict, optional
        Log other parameters, according to your preferences,
        in this format: {parameter_name:value,...}
    log_artifacts_list : list or None, optional
        If not None, logs every item (file or directory)
        in the list. Default value is None
    run_name : str or None, optional
        The name of the run. If None, does not log name.
    score_metric : str, sklearn scorer function or sklearn metric function
        Any score metric function from sklearn, either as string by name,
        or metric function (default way to load), or as scorer function
        (usually happens with sklearn._scorer.make_scorer(score_metric))
        See the metric functions at:
        https://scikit-learn.org/stable/modules/model_evaluation.html
        Default value: "r2", for sklearn.r2_score

    Returns
    -------
    None.

    """
    if tracking_uri is None:
        tracking_uri = get_directory_prompt(print_uri=False)
    check_first_run(tracking_uri)

    if check_cicd_pl_vs_local:
        check_running_cicd_pipeline(warn_devops=warn_devops)

    with mlflow.start_run(run_name=run_name):
        mlflow.sklearn.autolog()
        model.fit(X_train, y_train)

        if hasattr(model, 'coef_'):
            mlflow.log_param("Coeffs", model.coef_)

        # log other parameters
        for key in other_parameters_to_log:
            mlflow.log_param(key, other_parameters_to_log[key])

        # Inspired by sklearn; this makes sure that either a string
        # describing the score, a metric function or a scorer function
        # can be passed.
        if callable(score_metric):
            module = getattr(score_metric, "__module__", None)
            if (
                hasattr(module, "startswith")
                and module.startswith("sklearn.metrics.")
                and not module.startswith("sklearn.metrics._scorer")
                and not module.startswith("sklearn.metrics.tests.")
            ):
                score_metric = make_scorer(score_metric)
        score = get_scorer(score_metric)(model, X_valid, y_valid)
        mlflow.log_metric("score", score)

        # log a pickle of the model file
        if log_model_file:
            filename_model = fr"{tracking_uri}/{filename_model_prefix}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')}.sav"  # nopep8
            pickle.dump(model, open(filename_model, 'wb'))

            # exception if cwd is used
            if tracking_uri == "":
                filename_model = filename_model[1:]

            mlflow.log_artifact(filename_model)

        # log artifacts or folders
        if log_artifacts_list is not None:
            for artifact in log_artifacts_list:
                mlflow.log_artifact(artifact)


def new_experiment(name, artifact_location=None):
    """Setup new MLFlow experiment.

    Parameters
    ----------
    name : str
        Name of the experiment.
    artifact_location : str, optional
        The location to store experiment results and other artifacts.
        Can be the same as previous experiment.
        If not provided, the server picks an 'appropriate' default,
        not on a shared location.
    """
    mlflow.create_experiment(name, artifact_location=artifact_location)
    mlflow.set_experiment(name)
    os.environ['FIRST_RUN'] = "False"


def get_directory_prompt(print_uri=True):
    """Get the directory prompt that is needed to start MLFlow UI.

    Returns
    -------
    needed_uri : str
        The uri that one needs for the prompt.

    """
    full_uri = mlflow.get_tracking_uri()
    needed_uri = full_uri[5:-7]
    pyperclip.copy(needed_uri)
    if print_uri:
        print(needed_uri)
    return needed_uri


def check_running_cicd_pipeline(warn_devops=False):
    """Check whether it is run locally or on DevOps pipeline.

    Note: only tested on Azure DevOps.
    Quite probably does not work on other CICD tools.

    Parameters
    ----------
    warn_devops : bool, optional
        If True, warns when not running on DevOps pipeline.
        The default value is False.

    Returns
    -------
    None.

    """
    build_number = os.environ.get("BUILD_BUILDNUMBER")
    if build_number is not None:
        logging.info(f"Running in a (DevOps) pipeline, build {build_number}")
        # De forward slash is nodig voor databricks hosted mlflow
        # De BUILD_SOURCEBRANCHNAME is standaard in de azure pipeline
        # beschikbaar en deze bevat je git branchnaam
        mlflow.set_experiment(f"/{os.environ.get('BUILD_SOURCEBRANCHNAME')}")
    else:
        if warn_devops:
            logging.warning("Not running in a DevOps pipeline")


def mlflow_run_tensorflow():
    """Has not yet been implemented.
    """
    error_message = "mlflow_run_tensorflow has not yet been implemented"
    raise NotImplementedError(error_message)


def mlflow_run_pytorch():
    """Has not yet been implemented.
    """
    error_message = "mlflow_run_pytorch has not yet been implemented"
    raise NotImplementedError(error_message)


def check_first_run(tracking_uri):
    """Check whether this is the first run and set tracking uri accordingly.


    Parameters
    ----------
    tracking_uri : str
        Location of the artifacts.
        Similar to `artifact_location` in other MLFlow functions.

    Returns
    -------
    None.

    """
    if os.environ['FIRST_RUN'] == "True":
        name = input("Enter name of first experiment")
        print("First run: shifting to 'local_test'")
        setup_mlflow(name, tracking_uri)


def setup_mlflow(name, tracking_uri):
    """Setup MLFlow experiment.

    Parameters
    ----------
    name : str
        Name of the experiment.
    tracking_uri : str
        Location of the artifacts.
        Similar to `artifact_location` in other MLFlow functions.
    """
    mlflow.set_tracking_uri(f"file:{tracking_uri}")
    mlflow.set_experiment(name)
    os.environ['FIRST_RUN'] = "False"


def open_mlflowui_browser(pid=5000):
    """Opens location of MLFlow UI in the default web browser.

    Parameters
    ----------
    pid : int, optional
        Process ID of MLFlow UI, by default 5000,
        which is also the default of MLFlow.
    """
    import webbrowser
    webbrowser.open_new(f"http://localhost:{pid}/")
