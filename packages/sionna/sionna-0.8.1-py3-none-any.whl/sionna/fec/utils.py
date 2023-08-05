#
# SPDX-FileCopyrightText: Copyright (c) 2021-2022 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Utility functions and layers for the FEC package."""

import tensorflow as tf
from tensorflow.keras.layers import Layer
import numpy as np
import matplotlib.pyplot as plt
from importlib_resources import files, as_file
from sionna.fec.ldpc import codes
from sionna.utils.misc import log2

class GaussianPriorSource(Layer):
    r"""GaussianPriorSource(specified_by_mi=False, dtype=tf.float32, **kwargs)

    Generates `fake` LLRs as if the all-zero codeword was transmitted
    over an Bi-AWGN channel with noise variance ``no`` or mutual information
    (if ``specified_by_mi`` is True). If selected, the mutual information
    denotes the mutual information associated with a binary random variable
    observed at the output of a corresponding AWGN channel (cf. Gaussian
    approximation).

    .. image:: ../figures/GaussianPriorSource.png



    The generated LLRs are drawn from a Gaussian distribution with

    .. math::
        \sigma_{\text{llr}}^2 = \frac{4}{\sigma_\text{ch}^2}

    and

    .. math::
        \mu_{\text{llr}} = \frac{\sigma_\text{llr}^2}{2}

    where :math:`\sigma_\text{ch}^2` is the channel noise variance as defined by
    ``no``.

    If ``specified_by_mi`` is True, this class uses the of the so-called
    `J-function` (relates mutual information to Gaussian distributed LLRs) as
    proposed in [Brannstrom]_.

    Parameters
    ----------
        specified_by_mi : bool
            Defaults to False. If True, the second input parameter ``no`` is
            interpreted as mutual information instead of noise variance.

        dtype : tf.DType
            Defaults to `tf.float32`. Defines the datatype for internal
            calculations and the output. Must be one of the following
            `(tf.float16, tf.bfloat16, tf.float32, tf.float64)`.

    Input
    -----
        (output_shape, no):
            Tuple:

        output_shape : tf.int
            Integer tensor or Python array defining the shape of the desired
            output tensor.

        no : tf.float32
            Scalar defining the noise variance or mutual information (if
            ``specified_by_mi`` is True) of the corresponding (fake) AWGN
            channel.

    Output
    ------
        : ``dtype``, defaults to `tf.float32`
            1+D Tensor with shape as defined by ``output_shape``.

    Raises
    ------
        InvalidArgumentError
            If mutual information is not in (0,1).

        AssertionError
            If ``inputs`` is not a list with 2 elements.

    """

    def __init__(self, specified_by_mi=False, dtype=tf.float32, **kwargs):

        if dtype not in (tf.float16, tf.float32, tf.float64, tf.bfloat16,
                        tf.complex64, tf.complex128):
            raise ValueError("Only float dtypes are supported.")

        # use real_dtype to support tf.complex
        super().__init__(dtype=dtype.real_dtype, **kwargs)

        assert isinstance(specified_by_mi, bool),"specified_by_mi must be bool."
        self._specified_by_mi = specified_by_mi

    def call(self, inputs):
        """Generate Gaussian distributed fake LLRs as if the all-zero codeword
        was transmitted over an Bi-AWGN channel.

        Args:
            inputs (list): ``[output_shape, no]``, where
            ``output_shape`` (tf.int32): 1D list or tensor describing the
                desired shape of the output.
            ``no`` (tf.float32): Scalar defining the noise variance or mutual
                information (if ``specified_by_mi`` is True) of the
                corresponding (fake) AWGN channel.

        Returns:
            1+D Tensor (``dtype``): Shape as defined by ``output_shape``.
        """

        assert isinstance(inputs, list), "inputs must be a list."
        assert len(inputs)==2, "inputs must be a list with 2 elements."
        output_shape, noise_var = inputs

        if self._specified_by_mi:
            # interpret noise_var as mutual information
            mi_a = tf.cast(noise_var, tf.float32)
            tf.debugging.assert_greater_equal(mi_a, 0.,
                                        "Mutual information must be positive.")
            tf.debugging.assert_less_equal(mi_a, 1.,
                                "Mutual information must be less or equal 1.")
            #clip Ia to range (0,1)
            mi_a = tf.maximum(mi_a, 1e-7)
            mi_a = tf.minimum(mi_a, 1.)
            mu_llr = j_fun_inv_tf(mi_a)
            sigma_llr = tf.math.sqrt(2*mu_llr)
        else:
            noise_var = tf.cast(noise_var, tf.float32)

            # noise_var must be positive
            noise_var = tf.maximum(noise_var, 1e-7)
            sigma_llr = tf.math.sqrt(4 / noise_var)
            mu_llr = sigma_llr**2  / 2

        mu_llr = tf.cast(mu_llr, super().dtype)
        sigma_llr = tf.cast(sigma_llr, super().dtype)

        # generate LLRs with Gaussian approximation (BPSK, all-zero cw)
        # Use negative mean as we generate logits with definition p(b=1)/p(b=0)
        llr = tf.random.normal(output_shape,
                                mean=-1.*mu_llr,
                                stddev=sigma_llr,
                                dtype=super().dtype)
        return llr

def llr2mi(llr, s=None, reduce_dims=True):
    # pylint: disable=line-too-long
    r"""Implements an approximation of the mutual information based on LLRs.

    The function approximates the mutual information for given ``llr`` as
    derived in [Hagenauer]_ assuming an `all-zero codeword` transmission

    .. math::

        I \approx 1 - \sum \operatorname{log_2} \left( 1 + \operatorname{e}^{-\text{llr}} \right).

    This approximation assumes that the following `symmetry condition` is fulfilled

    .. math::

        p(\text{llr}|x=0) = p(\text{llr}|x=1) \cdot \operatorname{exp}(\text{llr}).

    For `non-all-zero` codeword transmissions, this methods requires knowledge
    about the signs of the original bit sequence ``s`` and flips the signs
    correspondingly (as if the all-zero codeword was transmitted).

    Please note that we define LLRs as :math:`\frac{p(x=1)}{p(x=0)}`, i.e.,
    the sign of the LLRs differ to the solution in [Hagenauer]_.

    Input
    -----
        llr : tf.float32
            Tensor of arbitrary shape containing LLR-values.

        s : None or tf.float32
            Tensor of same shape as llr containing the signs of the
            transmitted sequence (assuming BPSK), i.e., +/-1 values.

        reduce_dims : bool
            Defaults to True. If True, all dimensions are
            reduced and the return is a scalar. Otherwise, `reduce_mean` is
            only taken over the last dimension.

    Output
    ------
        mi : tf.float32
            A scalar tensor (if ``reduce_dims`` is True) or a tensor of same
            shape as ``llr`` apart from the last dimensions that is removed.
            It contains the approximated value of the mutual information.

    Raises
    ------
        TypeError
            If dtype of ``llr`` is not a real-valued float.

    """

    if s is None:
        s = tf.ones_like(llr)

    if llr.dtype not in (tf.float16, tf.bfloat16, tf.float32, tf.float64):
        raise TypeError("Dtype of llr must be a real-valued float.")

    # ensure that both tensors are compatible
    s = tf.cast(s, llr.dtype)

    # scramble sign as if all-zero cw was transmitted
    llr_zero = tf.multiply(s, llr)
    llr_zero = tf.clip_by_value(llr_zero, -20., 20.) # clip for stability
    x = log2(1. + tf.exp(1.* llr_zero))
    if reduce_dims:
        x = 1. - tf.reduce_mean(x)
    else:
        x = 1. - tf.reduce_mean(x, axis=-1)
    return x


def j_fun(mu):
       # pylint: disable=line-too-long
    r"""Calculates the `J-function` in NumPy.

    The so-called `J-function` relates mutual information to the mean of
    Gaussian distributed LLRs (cf. Gaussian approximation). We use the
    approximation as proposed in [Brannstrom]_ which can be written as

    .. math::

        J(\mu) \approx \left( 1- 2^{H_\text{1}(2\mu)^{H_\text{2}}}\right)^{H_\text{2}}

    with :math:`\mu` denoting the mean value of the LLR distribution and
    :math:`H_\text{1}=0.3073`, :math:`H_\text{2}=0.8935` and
    :math:`H_\text{3}=1.1064`.

    Input
    -----
        mu : float
            float or `ndarray` of float.

    Output
    ------
        : float
            `ndarray` of same shape as the input.
    """
    assert np.all(mu<1000), "mu too large."
    # we support exact 0 for EXIT (clipping is used in any way)
    assert np.all(mu>-0.0001), "mu must be positive."

    h1 = 0.3073
    h2 = 0.8935
    h3 = 1.1064
    mu = np.maximum(mu, 1e-10) # input must be positive for numerical stability
    mi = (1-2**(-h1*(2*mu)**h2))**h3
    return mi


def j_fun_inv(mi):
     # pylint: disable=line-too-long
    r"""Calculates the inverse `J-function` in NumPy.

    The so-called `J-function` relates mutual information to the mean of
    Gaussian distributed LLRs (cf. Gaussian approximation). We use the
    approximation as proposed in [Brannstrom]_ which can be written as

    .. math::

        J(\mu) \approx \left( 1- 2^{H_\text{1}(2\mu)^{H_\text{2}}}\right)^{H_\text{2}}

    with :math:`\mu` denoting the mean value of the LLR distribution and
    :math:`H_\text{1}=0.3073`, :math:`H_\text{2}=0.8935` and
    :math:`H_\text{3}=1.1064`.

    Input
    -----
        mi : float
            float or `ndarray` of float.

    Output
    -------
        : float
            `ndarray` of same shape as the input.

    Raises
    ------
        AssertionError
            If ``mi`` < 0.001 or ``mi`` > 0.999.
    """

    assert np.all(mi<0.999), "mi must be smaller 1."
    assert np.all(mi>0.001), "mi must be greater 0."

    h1 = 0.3073
    h2 = 0.8935
    h3 = 1.1064
    mi = np.maximum(mi,1e-10)
    # add small value to avoid log(0)
    mu = 0.5*((-1/h1)*np.log2((1-mi**(1/h3)) + 1e-12))**(1/(h2))
    return np.minimum(mu, 20) # clipp the output to mu_max =20


def j_fun_tf(mu, verify_inputs=True):
     # pylint: disable=line-too-long
    r"""Calculates the `J-function` in Tensorflow.

    The so-called `J-function` relates mutual information to the mean of
    Gaussian distributed LLRs (cf. Gaussian approximation). We use the
    approximation as proposed in [Brannstrom]_ which can be written as

    .. math::

        J(\mu) \approx \left( 1- 2^{H_\text{1}(2\mu)^{H_\text{2}}}\right)^{H_\text{2}}

    with :math:`\mu` denoting the mean value of the LLR distribution and
    :math:`H_\text{1}=0.3073`, :math:`H_\text{2}=0.8935` and
    :math:`H_\text{3}=1.1064`.

    Input
    -----
        mu : tf.float32
            Tensor of arbitrary shape.

        verify_inputs : bool
            A boolean defaults to True. If True, ``mu`` is clipped internally
            to be numerical stable.

    Output
    ------
        : tf.float32
            Tensor of same shape and dtype as ``mu``.

    Raises
    ------
        InvalidArgumentError
            If ``mu`` is negative.
    """
    assert isinstance(verify_inputs, bool), "verify_inputs must be bool."
    if verify_inputs:
        # input must be positive for numerical stability
        mu = tf.maximum(mu, 1e-10)
    else:
        tf.debugging.assert_greater_equal(mu, 0., "mu must be positive.")

    h1 = 0.3073
    h2 = 0.8935
    h3 = 1.1064
    mi = (1-2**(-h1*(2*mu)**h2))**h3
    return mi

def j_fun_inv_tf(mi, verify_inputs=True):
    # pylint: disable=line-too-long
    r"""Calculates the inverse `J-function` in Tensorflow.

    The so-called `J-function` relates mutual information to the mean of
    Gaussian distributed LLRs (cf. Gaussian approximation). We use the
    approximation as proposed in [Brannstrom]_ which can be written as

    .. math::

        J(\mu) \approx \left( 1- 2^{H_\text{1}(2\mu)^{H_\text{2}}}\right)^{H_\text{2}}

    with :math:`\mu` denoting the mean value of the LLR distribution and
    :math:`H_\text{1}=0.3073`, :math:`H_\text{2}=0.8935` and
    :math:`H_\text{3}=1.1064`.

    Input
    -----
        mi : tf.float32
            Tensor of arbitrary shape.

        verify_inputs : bool
            A boolean defaults to True. If True, ``mi`` is clipped internally
            to be numerical stable.

    Output
    ------
        : tf.float32
            Tensor of same shape and dtype as the ``mi``.

    Raises
    ------
        InvalidArgumentError
            If ``mi`` is not in `(0,1)`.
    """

    assert isinstance(verify_inputs, bool), "verify_inputs must be bool."
    if verify_inputs:
        # input must be positive for numerical stability
        mi = tf.maximum(mi, 1e-10) # ensure that I>0
        mi = tf.minimum(mi, 1.) # ensure that I=<1
    else:
        tf.debugging.assert_greater_equal(mi, 0., "mi must be positive.")
        tf.debugging.assert_less_equal(mi, 1., "mi must be less or equal 1.")

    h1 = 0.3073
    h2 = 0.8935
    h3 = 1.1064
    mu = 0.5*((-1/h1) * log2((1-mi**(1/h3))))**(1/(h2))
    return tf.minimum(mu, 20) # clipp the output to mu_max =20

def plot_trajectory(plot, mi_v, mi_c, ebno=None):
    """Utility function to plot the trajectory of an EXIT-chart.

    Input
    -----
        plot : matplotlib.figure
            A handle to a matplotlib figure.

        mi_v : float
            An ndarray of floats containing the variable node mutual
            information.

        mi_c : float
            An ndarray of floats containing the check node mutual
            information.

        ebno : float
            A float denoting the EbNo in dB for the legend entry.
    """

    assert (len(mi_v)==len(mi_c)), "mi_v and mi_c must have same length."

    # number of decoding iterations to plot
    iters = np.shape(mi_v)[0] - 1

    x = np.zeros([2*iters])
    y = np.zeros([2*iters])

    #  iterate between VN and CN MI value
    y[1] = mi_v[0]
    for i in range(1, iters):
        x[2*i] = mi_c[i-1]
        y[2*i] = mi_v[i-1]
        x[2*i+1] = mi_c[i-1]
        y[2*i+1] = mi_v[i]

    if ebno is not None:
        label_str = f"Actual trajectory @ {ebno} dB"
    else:
        label_str = "Actual trajectory"

    #plot trajectory
    plot.plot(x,
             y,
             "-",
             linewidth=3,
             color="g",
             label=label_str)
    plot.legend(fontsize=18) # and show the legend

def plot_exit_chart(mi_a=None, mi_ev=None, mi_ec=None, title="EXIT-Chart"):
    """Utility function to plot EXIT-Charts [tenBrinkEXIT]_.

    If all inputs are `None` an empty EXIT chart is generated. Otherwise,
    the mutual information curves are plotted.

    Input
    -----
        mi_a : float
            An ndarray of floats containing the a priori mutual
            information.

        mi_v : float
            An ndarray of floats containing the variable node mutual
            information.

        mi_c : float
            An ndarray of floats containing the check node mutual
            information.

        title : str
            A string defining the title of the EXIT chart.
    Output
    ------
        plt: matplotlib.figure
            A matplotlib figure handle

    Raises
    ------
        AssertionError
            If ``title`` is not `str`.
    """

    assert isinstance(title, str), "title must be str."

    if not (mi_ev is None and mi_ec is None):
        if mi_a is None:
            raise ValueError("mi_a cannot be None if mi_e is provided.")

    if mi_ev is not None:
        assert (len(mi_a)==len(mi_ev)), "mi_a and mi_ev must have same length."
    if mi_ec is not None:
        assert (len(mi_a)==len(mi_ec)), "mi_a and mi_ec must have same length."

    plt.figure(figsize=(10,10))
    plt.title(title, fontsize=25)
    plt.xlabel("$I_{a}^v$, $I_{e}^c$", fontsize=25)
    plt.ylabel("$I_{e}^v$, $I_{a}^c$", fontsize=25)
    plt.grid(visible=True, which='major')


    # for MI, the x,y limits are always (0,1)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)

    # and plot EXIT curves
    if mi_ec is not None:
        plt.plot(mi_ec, mi_a, "r", linewidth=3, label="Check node")
        plt.legend()
    if mi_ev is not None:
        plt.plot(mi_a, mi_ev, "b", linewidth=3, label="Variable node")
        plt.legend()
    return plt

def get_exit_analytic(pcm, ebno_db):
    """Calculate the analytic EXIT-curves for a given parity-check matrix.

    This function extracts the degree profile from ``pcm`` and calculates the
    variable (VN) and check node (CN) decoder EXIT curves. Please note that
    this is an asymptotic tool which needs a certain codeword length for
    accurate predictions.

    Transmission over an AWGN channel with BPSK modulation and SNR ``ebno_db``
    is assumed. The detailed equations can be found in [tenBrink]_ and
    [tenBrinkEXIT]_.

    Input
    -----
        pcm : ndarray
            The parity-check matrix.

        ebno_db : float
            The channel SNR in dB.

    Output
    ------
        mi_a : ndarray of floats
            NumPy array containing the `a priori` mutual information.

        mi_ev : ndarray of floats
            NumPy array containing the extrinsic mutual information of the
            variable node decoder for the corresponding ``mi_a``.

        mi_ec : ndarray of floats
            NumPy array containing the extrinsic mutual information of the check
            node decoder for the corresponding ``mi_a``.

    Note
    ----
        This function assumes random parity-check matrices without any imposed
        structure. Thus, explicit code construction algorithms may lead
        to inaccurate EXIT predictions. Further, this function is based
        on asymptotic properties of the code, i.e., only works well for large
        parity-check matrices. For details see [tenBrink]_.
    """

    # calc coderate
    n = pcm.shape[1]
    k = n - pcm.shape[0]
    coderate = k/n

    # calc mean and noise_var of Gaussian distributed LLRs for given channel SNR
    ebno = 10**(ebno_db/10)
    snr = ebno*coderate
    noise_var = 1/(2*snr)

    # For BiAWGN channels the LLRs follow a Gaussian distr. as given below [1]
    sigma_llr = np.sqrt(4 / noise_var)
    mu_llr = sigma_llr**2  / 2

    # calculate max node degree
    # "+1" as the array indices later directly denote the node degrees and we
    # have to account the array start at position 0 (i.e., we need one more
    # element)
    c_max = int(np.max(np.sum(pcm, axis=1)) + 1 )
    v_max = int(np.max(np.sum(pcm, axis=0)) + 1 )

    # calculate degree profile (node perspective)
    c = np.histogram(np.sum(pcm, axis=1),
                     bins=c_max,
                     range=(0, c_max),
                     density=False)[0]

    v = np.histogram(np.sum(pcm, axis=0),
                     bins=v_max,
                     range=(0, v_max),
                     density=False)[0]

    # calculate degrees from edge perspective
    r = np.zeros([c_max])
    for i in range(1,c_max):
        r[i] = (i-1)*c[i]
    r = r / np.sum(r)
    l = np.zeros([v_max])
    for i in range(1,v_max):
        l[i] = (i-1)*v[i]
    l = l / np.sum(l)

    mi_a = np.arange(0.002, 0.998, 0.001) # quantize Ia with 0.01 resolution

    # Exit function of check node update
    mi_ec = np.zeros_like(mi_a)
    for i in range(1, c_max):
        mi_ec += r[i] * j_fun((i-1.) * j_fun_inv(1 - mi_a))
    mi_ec = 1 - mi_ec

    # Exit function of variable node update
    mi_ev = np.zeros_like(mi_a)
    for i in range(1, v_max):
        mi_ev += l[i] * j_fun(mu_llr + (i-1.) * j_fun_inv(mi_a))

    return mi_a, mi_ev, mi_ec

def load_parity_check_examples(pcm_id, verbose=False):
    # pylint: disable=line-too-long
    """Utility function to load example codes stored in sub-folder LDPC/codes.

    The following codes are available

    - 0 : `(7,4)`-Hamming code of length `k=4` information bits and codeword    length `n=7`.

    - 1 : `(63,45)`-BCH code of length `k=45` information bits and codeword    length `n=63`.

    - 2 : (127,106)-BCH code of length `k=106` information bits and codeword    length `n=127`.

    - 3 : Random LDPC code with regular variable node degree 3 and check node degree 6 of length `k=50` information bits and codeword length         `n=100`.

    - 4 : 802.11n LDPC code of length of length `k=324` information bits and    codeword length `n=648`.

    Input
    -----
        pcm_id : int
            An integer defining which matrix id to load.

        verbose : bool
            A boolean defaults to False. If True, the code parameters are
            printed.

    Output
    ------
        pcm: ndarray of `zeros` and `ones`
            An ndarray containing the parity check matrix.

        k : int
            An integer defining the number of information bits.

        n : int
            An integer defining the number of codeword bits.

        coderate : float
            A float defining the coderate (assuming full rank of
            parity-check matrix).
    """

    source = files(codes).joinpath("example_codes.npy")
    with as_file(source) as code:
        pcms = np.load(code, allow_pickle=True)

    pcm = np.array(pcms[pcm_id]) # load parity-check matrix
    n = int(pcm.shape[1]) # number of codeword bits (codeword length)
    k = int(n - pcm.shape[0]) # number of information bits k per codeword
    coderate = k / n

    if verbose:
        print(f"\nn: {n}, k: {k}, coderate: {coderate:.3f}")
    return pcm, k, n, coderate

def bin2int(arr):
    """Convert binary array to integer.

    For example ``arr`` = `[1, 0, 1]` is converted to `5`.

    Input
    -----
        arr: int or float
            An iterable that yields 0's and 1's.

    Output
    -----
        : int
            Integer representation of ``arr``.

    """
    if len(arr) == 0: return None
    return int(''.join([str(x) for x in arr]), 2)

def bin2int_tf(arr):
    """
    Converts binary tensor to int tensor. Binary representation in ``arr``
    is across the last dimension from most significant to least significant.

    For example ``arr`` = `[0, 1, 1]` is converted to `3`.

    Input
    -----
        arr: int or float
            Tensor of  0's and 1's.

    Output
    -----
        : int
            Tensor containing the integer representation of ``arr``.
    """
    len_ = tf.shape(arr)[-1]
    shifts = tf.range(len_-1,-1,-1)

    # (2**len_-1)*arr[0] +... 2*arr[len_-2] + 1*arr[len_-1]
    op = tf.reduce_sum(tf.bitwise.left_shift(arr, shifts), axis=-1)

    return op

def int2bin(num, len_):
    """
    Convert ``num`` of int type to list of length ``len_`` with 0's and 1's.
    ``num`` and ``len_`` have to non-negative.

    For e.g., ``num`` = `5`; `int2bin(num`, ``len_`` =4) = `[0, 1, 0, 1]`.

    For e.g., ``num`` = `12`; `int2bin(num`, ``len_`` =3) = `[1, 0, 0]`.

    Input
    -----
        num: int
            An integer to be converted into binary representation.

        len_: int
            An integer defining the length of the desired output.

    Output
    -----
        : list of int
            Binary representation of ``num`` of length ``len_``.
    """
    assert num >= 0,  "Input integer should be non-negative"
    assert len_ >= 0,  "width should be non-negative"

    bin_ = format(num, f'0{len_}b')
    binary_vals = [int(x) for x in bin_[-len_:]] if len_ else []
    return binary_vals

def int2bin_tf(ints, len_):
    """
    Converts (int) tensor to (int) tensor with 0's and 1's. `len_` should be
    to non-negative. Additional dimension of size `len_` is inserted at end.

    Input
    -----
        ints: int
            Tensor of arbitrary shape `[...,k]` containing integer to be
            converted into binary representation.

        len_: int
            An integer defining the length of the desired output.

    Output
    -----
        : int
            Tensor of same shape as ``ints`` except dimension of length
            ``len_`` is added at the end `[...,k, len_]`. Contains the binary
            representation of ``ints`` of length ``len_``.
    """
    assert len_ >= 0

    shifts = tf.range(len_-1, -1, delta=-1)
    bits = tf.math.floormod(
        tf.bitwise.right_shift(tf.expand_dims(ints, -1), shifts), 2)
    return bits

def alist2mat(alist, verbose=True):
    # pylint: disable=line-too-long
    r"""Convert `alist` [MacKay]_ code definition to `full` parity-check matrix.

    Many code examples can be found in [UniKL]_.

    About `alist` (see [MacKay]_ for details):

        - `1.` Row defines parity-check matrix dimension `m x n`
        - `2.` Row defines int with `max_CN_degree`, `max_VN_degree`
        - `3.` Row defines VN degree of all `n` column
        - `4.` Row defines CN degree of all `m` rows
        - Next `n` rows contain non-zero entries of each column (can be zero padded at the end)
        - Next `m` rows contain non-zero entries of each row.

    Input
    -----
    alist: list
        Nested list in `alist`-format [MacKay]_.

    verbose: bool
        Defaults to True. If True, the code parameters are printed.

    Output
    ------
    (pcm, k, n, coderate):
        Tuple:

    pcm: ndarray
        NumPy array of shape `[n-k, n]` containing the parity-check matrix.

    k: int
        Number of information bits.

    n: int
        Number of codewords bits.

    coderate: float
        Coderate of the code.

    Note
    ----
        Use :class:`~sionna.fec.utils.load_alist` to import alist from a
        textfile.

        For example the following code snippet will import an alist from a file called ``filename``:

        .. code-block:: python

            pcm, k, n, coderate = alist2mat(load_alist(path = filename))
    """

    assert len(alist)>4, "Invalid alist format."

    n = alist[0][0]
    m = alist[0][1]
    v_max = alist[1][0]
    c_max = alist[1][1]
    k = n - m
    coderate = k / n

    vn_profile = alist[2]
    cn_profile = alist[3]

    # plausibility checks
    assert np.sum(vn_profile)==np.sum(cn_profile), "Invalid alist format."
    assert np.max(vn_profile)==v_max, "Invalid alist format."
    assert np.max(cn_profile)==c_max, "Invalid alist format."

    if len(alist)==len(vn_profile)+4:
        print("Note: .alist does not contain (redundant) CN perspective.")
        print("Recovering parity-check matrix from VN only.")
        print("Please verify the correctness of the results manually.")
        vn_only = True
    else:
        assert len(alist)==len(vn_profile) + len(cn_profile) + 4, \
                                                "Invalid alist format."
        vn_only = False

    pcm = np.zeros((m,n))
    num_edges = 0 # count number of edges

    for idx_v in range(n):
        for idx_i in range(vn_profile[idx_v]):
            # first 4 rows of alist contain meta information
            idx_c = alist[4+idx_v][idx_i]-1 # "-1" as this is python
            pcm[idx_c, idx_v] = 1
            num_edges += 1 # count number of edges (=each non-zero entry)

    # validate results from CN perspective
    if not vn_only:
        for idx_c in range(m):
            for idx_i in range(cn_profile[idx_c]):
                # first 4 rows of alist contain meta information
                # follwing n rows contained VN perspective
                idx_v = alist[4+n+idx_c][idx_i]-1 # "-1" as this is python
                assert pcm[idx_c, idx_v]==1 # entry must already exist

    if verbose:
        print("Number of variable nodes (columns): ", n)
        print("Number of check nodes (rows): ", m)
        print("Number of information bits per cw: ", k)
        print("Number edges: ", num_edges)
        print("Max. VN degree: ", v_max)
        print("Max. CN degree: ", c_max)
        print("VN degree: ", vn_profile)
        print("CN degree: ", cn_profile)

    return pcm, k, n, coderate

def load_alist(path):
    """Read `alist`-file [MacKay]_ and return nested list describing the
    parity-check matrix of a code.

    Many code examples can be found in [UniKL]_.

    Input
    -----
    path:str
        Path to file to be loaded.

    Output
    ------
    alist: list
        A nested list containing the imported alist data.
    """

    alist = []
    with open(path, "r") as reader: # pylint: disable=unspecified-encoding
        # read list line by line (different length)
        for line in reader:
            l = []
            # append all entries
            for word in line.split():
                l.append(int(word))
            if l: # ignore empty lines
                alist.append(l)

    return alist
