import matplotlib.pyplot as plt

# ==========================================
# SIGNAL TRANSFORMATION
# ==========================================


def plot_signals(
    original_signal, fiber_signal, crosstalk_signal, noisy_signal, number_of_samples=200
):

    samples = range(number_of_samples)

    plt.figure(figsize=(12, 8))

    plt.plot(samples, original_signal[:number_of_samples], label="Original Signal")

    plt.plot(samples, fiber_signal[:number_of_samples], label="After Fiber")

    plt.plot(samples, crosstalk_signal[:number_of_samples], label="After Crosstalk")

    plt.plot(samples, noisy_signal[:number_of_samples], label="After Noise")

    plt.xlabel("Sample")

    plt.ylabel("Optical Power (W)")

    plt.title("WDM Channel Signal Transformation")

    plt.legend()

    plt.grid()

    plt.tight_layout()

    plt.show()


# ==========================================
# CROSSTALK VS BER
# ==========================================


def plot_ber(crosstalk_values, ber_values):

    plt.figure(figsize=(8, 5))

    plt.plot(crosstalk_values, ber_values, marker="o")

    plt.xlabel("Crosstalk Coupling Coefficient")

    plt.ylabel("Bit Error Rate (BER)")

    plt.title("Effect of Crosstalk on BER")

    plt.grid()

    plt.tight_layout()

    plt.show()


# ==========================================
# BER BEFORE VS AFTER COMPENSATION
# ==========================================


def plot_compensation(ber_before, ber_after):

    labels = ["Before Compensation", "After Compensation"]

    values = [ber_before, ber_after]

    plt.figure(figsize=(8, 5))

    plt.bar(labels, values)

    plt.ylabel("Bit Error Rate (BER)")

    plt.title("BER Before and After Crosstalk Compensation")

    plt.grid(axis="y")

    plt.tight_layout()

    plt.show()
