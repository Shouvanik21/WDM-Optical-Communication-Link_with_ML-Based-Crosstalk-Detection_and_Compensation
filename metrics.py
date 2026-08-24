import numpy as np
import math


def calculate_ber(transmitted_bits, received_bits):

    errors = np.sum(transmitted_bits != received_bits)

    total_bits = len(transmitted_bits)

    ber = errors / total_bits

    return ber


def calculate_snr(signal_power, noise_power):

    if noise_power <= 0:

        return float("inf")

    snr = signal_power / noise_power

    snr_db = 10 * np.log10(snr)

    return snr_db


def calculate_q_factor(mean_one, mean_zero, std_one, std_zero):

    denominator = std_one + std_zero

    if denominator == 0:

        return float("inf")

    q = (mean_one - mean_zero) / denominator

    return q


def calculate_ber_from_q(q):

    if q == float("inf"):

        return 0.0

    ber = 0.5 * math.erfc(q / math.sqrt(2))

    return ber
