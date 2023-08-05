#
# SPDX-FileCopyrightText: Copyright (c) 2021-2022 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Various classes for spatially correlated flat-fading channels."""

from abc import ABC, abstractmethod
import tensorflow as tf
from tensorflow.experimental.numpy import swapaxes
from sionna.utils import expand_to_rank, matrix_sqrt

class SpatialCorrelation(ABC):
    # pylint: disable=line-too-long
    r"""Abstract class that defines an interface for spatial correlation functions.

    The :class:`~sionna.channel.FlatFadingChannel` model can be configured with a
    spatial correlation model.

    Input
    -----
    h : tf.complex
        Tensor of arbitray shape containing spatially uncorrelated
        channel coeffficients

    Output
    ------
    h_corr : tf.complex
        Tensor of the same shape and dtype as ``h`` containing the spatially
        correlated channel coefficients.
    """
    @abstractmethod
    def __call__(self, h, *args, **kwargs):
        return NotImplemented

class KroneckerModel(SpatialCorrelation):
    # pylint: disable=line-too-long
    r"""Kronecker model for spatial correlation.

    Given a batch of matrices :math:`\mathbf{H}\in\mathbb{C}^{M\times K}`,
    :math:`\mathbf{R}_\text{tx}\in\mathbb{C}^{K\times K}`, and
    :math:`\mathbf{R}_\text{rx}\in\mathbb{C}^{M\times M}`, this function
    will generate the following output:

    .. math::

        \mathbf{H}_\text{corr} = \mathbf{R}^{\frac12}_\text{rx} \mathbf{H} \mathbf{R}^{\frac12}_\text{tx}

    Note that :math:`\mathbf{R}_\text{tx}\in\mathbb{C}^{K\times K}` and :math:`\mathbf{R}_\text{rx}\in\mathbb{C}^{M\times M}`
    must be positive semi-definite, such as the ones generated by
    :meth:`~sionna.channel.exp_corr_mat`.

    Parameters
    ----------
    r_tx : [..., K, K], tf.complex
        Tensor containing the transmit correlation matrices. If
        the rank of ``r_tx`` is smaller than that of the input ``h``,
        it will be broadcast.

    r_rx : [..., M, M], tf.complex
        Tensor containing the receive correlation matrices. If
        the rank of ``r_rx`` is smaller than that of the input ``h``,
        it will be broadcast.

    Input
    -----
    h : [..., M, K], tf.complex
        Tensor containing spatially uncorrelated
        channel coeffficients.

    Output
    ------
    h_corr : [..., M, K], tf.complex
        Tensor containing the spatially
        correlated channel coefficients.
    """
    def __init__(self, r_tx=None, r_rx=None):
        super().__init__()
        self.r_tx = r_tx
        self.r_rx = r_rx

    @property
    def r_tx(self):
        r"""Tensor containing the transmit correlation matrices.

        Note
        ----
        If you want to set this property in Graph mode with XLA, i.e., within
        a function that is decorated with ``@tf.function(jit_compile=True)``,
        you must set ``sionna.Config.xla_compat=true``.
        See :py:attr:`~sionna.Config.xla_compat`.
        """
        return self._r_tx

    @r_tx.setter
    def r_tx(self, value):
        self._r_tx = value
        if self._r_tx is not None:
            self._r_tx_sqrt = matrix_sqrt(value)
        else:
            self._r_tx_sqrt = None

    @property
    def r_rx(self):
        r"""Tensor containing the receive correlation matrices.

        Note
        ----
        If you want to set this property in Graph mode with XLA, i.e., within
        a function that is decorated with ``@tf.function(jit_compile=True)``,
        you must set ``sionna.Config.xla_compat=true``.
        See :py:attr:`~sionna.Config.xla_compat`.
        """
        return self._r_rx

    @r_rx.setter
    def r_rx(self, value):
        self._r_rx = value
        if self._r_rx is not None:
            self._r_rx_sqrt = matrix_sqrt(value)
        else:
            self._r_rx_sqrt = None

    def __call__(self, h):
        if self._r_tx_sqrt is not None:
            r_tx_sqrt = expand_to_rank(self._r_tx_sqrt, tf.rank(h), 0)
            h = tf.matmul(h, r_tx_sqrt, adjoint_b=True)

        if self._r_rx_sqrt is not None:
            r_rx_sqrt = expand_to_rank(self._r_rx_sqrt, tf.rank(h), 0)
            h = tf.matmul(r_rx_sqrt, h)

        return h

class PerColumnModel(SpatialCorrelation):
        # pylint: disable=line-too-long
    r"""Per-column model for spatial correlation.

    Given a batch of matrices :math:`\mathbf{H}\in\mathbb{C}^{M\times K}`
    and correlation matrices :math:`\mathbf{R}_k\in\mathbb{C}^{M\times M}, k=1,\dots,K`,
    this function will generate the output :math:`\mathbf{H}_\text{corr}\in\mathbb{C}^{M\times K}`,
    with columns

    .. math::

        \mathbf{h}^\text{corr}_k = \mathbf{R}^{\frac12}_k \mathbf{h}_k,\quad k=1, \dots, K

    where :math:`\mathbf{h}_k` is the kth column of :math:`\mathbf{H}`.
    Note that all :math:`\mathbf{R}_k\in\mathbb{C}^{M\times M}` must
    be positive semi-definite, such as the ones generated
    by :meth:`~sionna.channel.one_ring_corr_mat`.

    This model is typically used to simulate a MIMO channel between multiple
    single-antenna users and a base station with multiple antennas.
    The resulting SIMO channel for each user has a different spatial correlation.

    Parameters
    ----------
    r_rx : [..., M, M], tf.complex
        Tensor containing the receive correlation matrices. If
        the rank of ``r_rx`` is smaller than that of the input ``h``,
        it will be broadcast. For a typically use of this model, ``r_rx``
        has shape [..., K, M, M], i.e., a different correlation matrix for each
        column of ``h``.

    Input
    -----
    h : [..., M, K], tf.complex
        Tensor containing spatially uncorrelated
        channel coeffficients.

    Output
    ------
    h_corr : [..., M, K], tf.complex
        Tensor containing the spatially
        correlated channel coefficients.
    """
    def __init__(self, r_rx):
        super().__init__()
        self.r_rx = r_rx

    @property
    def r_rx(self):
        """Tensor containing the receive correlation matrices.

        Note
        ----
        If you want to set this property in Graph mode with XLA, i.e., within
        a function that is decorated with ``@tf.function(jit_compile=True)``,
        you must set ``sionna.Config.xla_compat=true``.
        See :py:attr:`~sionna.Config.xla_compat`.
        """

        return self._r_rx

    @r_rx.setter
    def r_rx(self, value):
        self._r_rx = value
        if self._r_rx is not None:
            self._r_rx_sqrt = matrix_sqrt(value)

    def __call__(self, h):
        if self._r_rx is not None:
            h = swapaxes(h, -2, -1)
            h = tf.expand_dims(h, -1)
            r_rx_sqrt = expand_to_rank(self._r_rx_sqrt, tf.rank(h), 0)
            h = tf.matmul(r_rx_sqrt, h)
            h = tf.squeeze(h, -1)
            h = swapaxes(h, -2, -1)

        return h
