# Author: Sergey Kolesnikov (scitator@gmail.com)
# Licence: Apache 2.0
from typing import List

import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


def plot_confusion_matrix(
    cm: np.ndarray = None,
    y_true: np.ndarray = None,
    y_pred: np.ndarray = None,
    labels: List = None,
    normalize: bool = False,
    show: bool = False,
    cmap: str = "Blues",
    **kwargs,
):
    if cm is None:
        cm = confusion_matrix(y_true=y_true, y_pred=y_pred, labels=labels)
    if normalize:
        # equals to metrics.confusion_matrix(normalize="true")
        cm = cm.astype(np.float32) / cm.sum(axis=1)[:, np.newaxis]
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(cmap=cmap, **kwargs)
    if show:
        import matplotlib.pyplot as plt

        plt.show()
    return disp


__all__ = [plot_confusion_matrix]
