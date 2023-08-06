#! /usr/bin/python
# -*- coding: utf-8 -*-

import tensorlayerx as tlx
from tensorlayerx import logging
from tensorlayerx.nn.core import Module
from ..initializers import *

__all__ = ['Input', '_InputLayer']


class _InputLayer(Module):
    """
    The :class:`Input` class is the starting layer of a neural network.

    Parameters
    ----------
    shape : tuple (int)
        Including batch size.
    dtype: dtype or None
        The type of input values. By default, tf.float32.
    name : None or str
        A unique layer name.

    """

    def __init__(self, shape, dtype=None, name=None, init=None):
        super(_InputLayer, self).__init__(name)

        logging.info("Input  %s: %s" % (self.name, str(shape)))
        self.shape = shape
        self.dtype = dtype
        self.shape_without_none = [_ if _ is not None else 1 for _ in shape]
        if init is None:
            self.outputs = ones()(self.shape_without_none, dtype=self.dtype)
        else:
            self.outputs = init(self.shape_without_none, dtype=self.dtype)
        self._built = True

    def __repr__(self):
        s = 'Input(shape=%s' % str(self.shape)
        if self.name is not None:
            s += (', name=\'%s\'' % self.name)
        s += ')'
        return s

    def __call__(self, *args, **kwargs):
        return self.outputs

    def build(self, inputs_shape):
        pass

    def forward(self):
        return self.outputs


def Input(shape, init=ones(), dtype=tlx.float32, name=None):
    """
    The :class:`Input` class is the starting layer of a neural network.

    Parameters
    ----------
    shape : tuple (int)
        Including batch size.
    init : initializer or str or None
        The initializer for initializing the input matrix
    dtype: dtype
        The type of input values. By default, tf.float32.
    name : None or str
        A unique layer name.

    Examples
    ---------
    With TensorLayer

    >>> ni = tlx.nn.Input([10, 50, 50, 32], name='input')
    >>> output shape : [10, 50, 50, 32]

    """

    if tlx.BACKEND == 'paddle':
        return tlx.ops.ones(shape, dtype)
    input_layer = _InputLayer(shape, dtype=dtype, name=name, init=init)
    outputs = input_layer()
    return outputs
