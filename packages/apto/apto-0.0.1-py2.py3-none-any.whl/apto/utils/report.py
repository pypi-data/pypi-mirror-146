# Author: Sergey Kolesnikov (scitator@gmail.com)
# Licence: Apache 2.0
from collections import defaultdict
import warnings

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    roc_auc_score,
)


def get_classification_report(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_score: np.ndarray = None,
    beta: float = None,
) -> pd.DataFrame:
    """Generates pandas-based per-class and aggregated classification metrics.

    Args:
        y_true: ground truth labels of shape [n_samples, ]
        y_pred: model predicted labels of shape [n_samples, ]
        y_score: model predicted scores of shape [n_samples, n_classes].
            Defaults to None. Multiclass ROC AUC measured in ``one-vs-rest`` way.
        beta: Beta parameter for custom Fbeta score computation. Defaults to None.

    Returns:
        pd.DataFrame: pandas dataframe with main classification metrics.

    Examples:

    .. code-block:: python

        from sklearn import datasets, linear_model, metrics
        from sklearn.model_selection import train_test_split
        from apto.utils import get_classification_report

        digits = datasets.load_digits()

        # flatten the images
        n_samples = len(digits.images)
        data = digits.images.reshape((n_samples, -1))

        # Create a classifier
        clf = linear_model.LogisticRegression(multi_class="ovr")

        # Split data into 50% train and 50% test subsets
        X_train, X_test, y_train, y_test = train_test_split(
            data, digits.target, test_size=0.5, shuffle=False)

        # Learn the digits on the train subset
        clf.fit(X_train, y_train)

        # Predict the value of the digit on the test subset
        y_score = clf.predict_proba(X_test)
        y_pred = clf.predict(X_test)

        get_classification_report(
            y_true=y_test,
            y_pred=y_pred,
            y_score=y_score,
            beta=0.5
        )
    """
    metrics = defaultdict(lambda: {})
    metrics_names = [
        "precision",
        "recall",
        "f1-score",
        "auc",
        "support",
        "support (%)",
    ]
    averages = ["macro", "micro", "weighted"]

    labels = sorted(set(y_true).union(y_pred))
    num_classes = len(labels)
    is_binary = num_classes == 2
    if y_score is not None:
        assert (len(y_score.shape) == 1 and is_binary) or (
            len(y_score.shape) == 2 and y_score.shape[1] == num_classes
        ), "Incorrect ``y_score`` shape found."
        assert np.min(y_score) >= 0.0 and np.max(y_score) <= 1.0
    if y_score is not None and is_binary and len(y_score.shape) != 2:
        warnings.warn(
            "Flatten binary ``y_score`` found."
            "Expanding to ``1 - scores`` for 0-class and ``scores`` for 1-class."
        )
        y_score = np.vstack((1.0 - y_score, y_score)).T

    accuracy = accuracy_score(y_true=y_true, y_pred=y_pred)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true=y_true, y_pred=y_pred, average=None, labels=labels
    )
    r_support = support / support.sum()

    auc = np.zeros(num_classes)
    if y_score is not None:
        for i, label in enumerate(labels):
            auc[i] = roc_auc_score((y_true == label).astype(int), y_score[:, i])

    report = pd.DataFrame(
        [precision, recall, f1, auc, support, r_support],
        columns=labels,
        index=metrics_names,
    ).T

    for average in averages:
        avg_precision, avg_recall, avg_f1, _ = precision_recall_fscore_support(
            y_true=y_true, y_pred=y_pred, average=average, labels=labels
        )

        avg_metrics = avg_precision, avg_recall, avg_f1
        for k, v in zip(metrics_names[:4], avg_metrics):
            metrics[k][average] = v

    if beta is not None:
        _, _, fbeta, _ = precision_recall_fscore_support(
            y_true=y_true, y_pred=y_pred, average=None, beta=beta, labels=labels
        )
        avg_fbeta = np.zeros(len(averages))
        for i, average in enumerate(averages):
            _, _, avg_beta, _ = precision_recall_fscore_support(
                y_true=y_true, y_pred=y_pred, average=average, beta=beta, labels=labels
            )
            avg_fbeta[i] = avg_beta
        report.insert(3, "fb-score", fbeta, True)

    metrics["support"]["macro"] = support.sum()
    metrics["precision"]["accuracy"] = accuracy
    if y_score is not None:
        if is_binary:
            auc_macro = roc_auc_score(y_true, y_score[:, 1], average="macro")
            auc_weighted = roc_auc_score(y_true, y_score[:, 1], average="weighted")
        else:
            auc_macro = roc_auc_score(
                y_true, y_score, multi_class="ovr", average="macro"
            )
            auc_weighted = roc_auc_score(
                y_true, y_score, multi_class="ovr", average="weighted"
            )
        metrics["auc"]["macro"] = auc_macro
        metrics["auc"]["weighted"] = auc_weighted

    metrics = pd.DataFrame(metrics, index=averages + ["accuracy"])
    result = pd.concat((report, metrics)).fillna("")

    if beta:
        result["fb-score"]["macro"] = avg_fbeta[0]
        result["fb-score"]["micro"] = avg_fbeta[1]
        result["fb-score"]["weighted"] = avg_fbeta[2]
    return result


__all__ = [get_classification_report]
