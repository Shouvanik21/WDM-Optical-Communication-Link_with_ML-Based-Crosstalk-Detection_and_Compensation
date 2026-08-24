import matplotlib.pyplot as plt


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
    plt.ylabel("Signal Amplitude")

    plt.title("WDM Channel Signal Transformation")

    plt.legend()

    plt.grid()

    plt.show()


def plot_ber(crosstalk_values, ber_values):

    plt.figure(figsize=(8, 5))

    plt.plot(crosstalk_values, ber_values, marker="o")

    plt.xlabel("Crosstalk Coupling Coefficient")

    plt.ylabel("BER")

    plt.title("Effect of Crosstalk on BER")

    plt.grid()

    plt.show()
