import numpy as np


def calculate_snr(signal_power, noise_power):

    if noise_power <= 0:

        return 100

    snr = signal_power / noise_power

    snr_db = 10 * np.log10(snr)

    return snr_db


def calculate_q_factor(mean_one, mean_zero, std_one, std_zero):

    denominator = std_one + std_zero

    if denominator == 0:

        return 100

    q = (mean_one - mean_zero) / denominator

    return q


def calculate_ber_from_q(q):

    ber = 0.5 * np.math.erfc(q / np.sqrt(2))

    return ber
