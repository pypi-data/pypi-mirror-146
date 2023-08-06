"""
PyTorch BRITS model for both the time-series imputation task and the classification task.
"""

# Created by Wenjie Du <wenjay.du@gmail.com>
# License: MIT

import torch.nn as nn
import torch.nn.functional as F

from pypots.imputation.brits import (
    RITS as imputation_RITS,
    BRITS as imputation_BRITS
)


class RITS(imputation_RITS):
    def __init__(self, seq_len, feature_num, rnn_hidden_size, **kwargs):
        super(RITS, self).__init__(seq_len, feature_num, rnn_hidden_size, **kwargs)
        self.dropout = nn.Dropout(p=0.25)
        self.classifier = nn.Linear(self.rnn_hidden_size, 1)

    def forward(self, data, direction='forward'):
        ret_dict = super(RITS).forward(data, direction)
        logits = self.classifier(ret_dict['final_hidden_state'])
        ret_dict['classification_loss'] = F.binary_cross_entropy_with_logits(logits, data['labels'])
        ret_dict['predictions'] = F.sigmoid(logits)
        return ret_dict


class BRITS(imputation_BRITS):
    pass
