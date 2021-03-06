import logging
from collections import OrderedDict

from tabulate import tabulate

from ... import util
from ...model_info import ModelInfo

logger = logging.getLogger(__name__)


class Counts(ModelInfo):

    def __init__(self, labels, score_labels, prediction_key):
        super().__init__()
        self['n'] = len(score_labels)

        self['labels'] = OrderedDict((l, 0) for l in labels)
        self['predictions'] = OrderedDict(
            (actual, OrderedDict((predicted, 0) for predicted in labels))
            for actual in labels)

        for score, label in score_labels:
            predicted = score[prediction_key]
            self['labels'][label] += 1
            self['predictions'][label][predicted] += 1

    def format_str(self, path_tree, **kwargs):
        if len(path_tree) > 0:
            logger.warn("Ignoring path_tree={0!r} while formatting counts."
                        .format(path_tree))
        formatted = "counts (n={0}):\n".format(self['n'])
        table_data = [
            [repr(label), self['labels'][label], '-->'] +
            [count for pred, count in pred_counts.items()]
            for label, pred_counts in self['predictions'].items()]
        table_str = tabulate(
            table_data, headers=['label', 'n', ''] +
                                ["~{0}".format(l) for l in self['labels']])
        formatted += util.tab_it_in(table_str)
        return formatted

    def format_json(self, path_tree, **kwargs):
        return util.dict_lookup(self._data, path_tree)
