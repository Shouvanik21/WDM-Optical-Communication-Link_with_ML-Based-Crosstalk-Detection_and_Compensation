import numpy as np
import math

# ==========================================
# BIT ERROR RATE
# ==========================================


def calculate_ber(transmitted_bits, received_bits):

    transmitted_bits = np.asarray(transmitted_bits)

    received_bits = np.asarray(received_bits)

    # Make sure both arrays have
    # the same number of bits

    if len(transmitted_bits) != len(received_bits):

        raise ValueError("Transmitted and received " "bits must have the same length.")

    errors = np.sum(transmitted_bits != received_bits)

    total_bits = len(transmitted_bits)

    if total_bits == 0:

        return 0.0

    ber = errors / total_bits

    return float(ber)


# ==========================================
# SIGNAL-TO-NOISE RATIO
# ==========================================


def calculate_snr(signal_power, noise_power):

    if noise_power <= 0:

        return float("inf")

    if signal_power <= 0:

        return float("-inf")

    snr = signal_power / noise_power

    snr_db = 10 * np.log10(snr)

    return float(snr_db)


# ==========================================
# SIGNAL POWER
# ==========================================


def calculate_signal_power(signal):

    signal = np.asarray(signal)

    power = np.mean(signal**2)

    return float(power)


# ==========================================
# NOISE POWER
# ==========================================


def calculate_noise_power(noise):

    noise = np.asarray(noise)

    power = np.mean(noise**2)

    return float(power)


# ==========================================
# CROSSTALK RATIO
# ==========================================


def calculate_crosstalk_ratio(signal_power, crosstalk_power):

    epsilon = 1e-12

    if signal_power <= 0:

        return 0.0

    ratio = crosstalk_power / (signal_power + epsilon)

    return float(ratio)


# ==========================================
# CROSSTALK IN dB
# ==========================================


def calculate_crosstalk_db(signal_power, crosstalk_power):

    ratio = calculate_crosstalk_ratio(signal_power, crosstalk_power)

    epsilon = 1e-12

    crosstalk_db = 10 * np.log10(ratio + epsilon)

    return float(crosstalk_db)


# ==========================================
# Q FACTOR
# ==========================================


def calculate_q_factor(mean_one, mean_zero, std_one, std_zero):

    denominator = std_one + std_zero

    if denominator <= 0:

        return float("inf")

    q = (mean_one - mean_zero) / denominator

    return float(q)


# ==========================================
# BER FROM Q FACTOR
# ==========================================


def calculate_ber_from_q(q):

    if q == float("inf"):

        return 0.0

    if q <= 0:

        return 0.5

    ber = 0.5 * math.erfc(q / math.sqrt(2))

    return float(ber)


# ==========================================
# BER IMPROVEMENT
# ==========================================


def calculate_ber_improvement(ber_before, ber_after):

    if ber_before <= 0:

        return 0.0

    improvement = ((ber_before - ber_after) / ber_before) * 100

    return float(improvement)
