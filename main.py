from simulation import WDMSimulator

print("\n======================================")
print("      INTELLIGENT WDM SYSTEM")
print("======================================")


simulator = WDMSimulator(
    number_of_channels=4,
    number_of_bits=100,
    samples_per_bit=20,
    fiber_length=50,
    attenuation=0.2,
    dispersion=17,
    coupling=0.001,
    noise_level=0.000005,
)


result = simulator.run()


print("\n========== SIMULATION RESULTS ==========")


for key, value in result.items():

    print(key, ":", value)
