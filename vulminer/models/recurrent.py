# -*- coding: utf-8 -*-
"""
recurrent.py - Models of Recurrent Neural Network

:Author: Verf
:Email: verf@protonmail.com
:License: MIT
"""
import torch
import torch.nn as nn

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class GRU(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes,
                 **kwargs):
        super(GRU, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_classes = num_classes
        self.gru = nn.GRU(self.input_size, self.hidden_size, self.num_layers,
                          **kwargs)
        self.dense = nn.Linear(
            self.hidden_size,
            self.num_classes,
        )

    def forward(self, train_dataset):
        output, _ = self.gru(train_dataset)
        output = self.dense(output[:, -1, :])
        return output


class BGRU(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes,
                 **kwargs):
        super(BGRU, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_classes = num_classes
        self.bgru = nn.GRU(
            self.input_size,
            self.hidden_size,
            self.num_layers,
            bidirectional=True,
            **kwargs)
        self.dense = nn.Linear(
            self.hidden_size * 2,
            self.num_classes,
        )

    def forward(self, train_dataset):
        output, _ = self.bgru(train_dataset)
        output = self.dense(output[:, -1, :])
        return output


class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes,
                 **kwargs):
        super(LSTM, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_classes = num_classes
        self.lstm = nn.LSTM(
            self.input_size,
            self.hidden_size,
            self.num_layers,
            **kwargs,
        )
        self.dense = nn.Linear(
            self.hidden_size,
            self.num_classes,
        )

    def forward(self, train_dataset):
        hidden = torch.zeros(self.num_layers, train_dataset.size(0),
                             self.hidden_size).to(device)
        c0 = torch.zeros(self.num_layers, train_dataset.size(0),
                         self.hidden_size).to(device)
        output, _ = self.lstm(train_dataset, (hidden, c0))
        output = self.dense(output[:, -1, :])
        return output


class BLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes,
                 **kwargs):
        super(BLSTM, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_classes = num_classes
        self.blstm = nn.LSTM(
            self.input_size,
            self.hidden_size,
            self.num_layers,
            bidirectional=True,
            **kwargs)
        self.dense = nn.Linear(
            self.hidden_size * 2,
            self.num_classes,
        )

    def forward(self, train_dataset):
        hidden = torch.zeros(self.num_layers * 2, train_dataset.size(0),
                             self.hidden_size).to(device)
        c0 = torch.zeros(self.num_layers * 2, train_dataset.size(0),
                         self.hidden_size).to(device)
        output, _ = self.blstm(train_dataset, (hidden, c0))
        output = self.dense(output[:, -1, :])
        return output