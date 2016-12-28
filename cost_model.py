from math import log10
def private_cost_per_greened_acre(greenedAcrePerSMP):
    log10CostPerGA = 4.98 - 0.24*log10(greenedAcrePerSMP)
    costPerGA = 10**log10CostPerGA
    return costPerGA
def public_cost_per_greened_acre(greenedAcrePerSMP):
    log10CostPerGA = 5.25 - 0.24*log10(greenedAcrePerSMP)
    costPerGA = 10**log10CostPerGA
    return costPerGA