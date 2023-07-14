import random
from math import gcd
from sympy import isprime, simplify
from fractions import Fraction
from collections import deque, Counter
from itertools import islice
import time
import json
import csv
import os
from datetime import datetime
import pickle
import shutil
from itertools import product
from collections import defaultdict


# The Miller-Rabin primality test is a probabilistic primality test: an algorithm which 
# determines whether a given number is likely to be prime, similar to the Fermat primality test 
# and the Solovay-Strassen primality test. Its original version, as described by Miller 
# (who proved that the test is correct for all prime numbers) and extended by Rabin (who 
# dealt with the composite, or non-prime, numbers), is deterministic, but the determinism 
# relies on the unproven generalized Riemann hypothesis. Michael O. Rabin modified it to 
# obtain an unconditional probabilistic algorithm.
def miller_rabin(n, k):  # number of tests
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23]:
        if n % p == 0:
            return n == p
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True
    
# Find the next prime number greater than the input number. Uses the Miller-Rabin primality test.
def find_next_prime(start_number, miller_rabin_iterations):
    if start_number % 2 == 0:
        start_number += 1
    else:
        start_number += 2
    number = start_number
    while True:
        is_prime = miller_rabin(number, miller_rabin_iterations)
        if is_prime:
            return number
        number += 2

# Find a sequence of prime numbers, starting from a specified number.
def find_prime_sequence(start_number, num_primes, miller_rabin_iterations, verbose):
    primes = []
    current_number = start_number
    if num_primes > 1000:
        feedback_factor = 1000
    else:
        feedback_factor = num_primes / 2
    while len(primes) < num_primes:
        current_number = find_next_prime(current_number, miller_rabin_iterations)
        primes.append(current_number)
        if verbose and len(primes) % (num_primes // feedback_factor) == 0:  # Report progress every 0.1%
            print(f"\r{100.0 * len(primes) / num_primes} % done    ", end="")
    print(f"\r{100.0} % done             ", end="")
    print()  # Print a newline at the end to move the cursor to the next line
    return primes

# Calculate the second difference for a sequence of numbers.
def calculate_second_differences(primes):
    gaps = [b - a for a, b in zip(primes[:-1], primes[1:])]
    second_differences = [b - a for a, b in zip(gaps[:-1], gaps[1:])]
    return second_differences


# Calculate the second ratio for a sequence of numbers.
def calculate_second_ratios(primes):
    gaps = [b - a for a, b in zip(primes[:-1], primes[1:])]
    second_differences = [b - a for a, b in zip(gaps[:-1], gaps[1:])]
    second_sums = [a + b for a, b in zip(gaps[:-1], gaps[1:])]
    second_ratios = [Fraction(sd, ss).limit_denominator() if ss != 0 else None for sd, ss in zip(second_differences, second_sums)]
    return second_ratios

# Generate a random number with a specific number of bits.
def generate_random_number(num_bits):
    return random.randint(2**(num_bits-1), 2**num_bits - 1)

# Create a directory to store dataset output files.
def create_output_directory(num_bits, num_primes):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    directory_name = f"{num_bits}bit{num_primes}_{timestamp}"
    directory = os.path.join(os.getcwd(), directory_name)
    os.makedirs(directory, exist_ok=True)
    return directory

# Write the sequence of primes with their second differences and second ratios to a CSV file.
def write_output_to_csv(primes, sd, sr, base_filename):
    filename = f"{base_filename}_primes.csv"
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Prime", "Second Difference", "Second Ratio (Fraction)", "Second Ratio (Decimal)"])
        for i in range(len(sd)):  # Include all second differences and second ratios
            writer.writerow([
                str(primes[i+1])[-10:],  # Write the prime number associated with each second difference and second ratio
                sd[i] if i < len(sd) else None, 
                str(sr[i]) if i < len(sr) else None, 
                float(sr[i]) if (i < len(sr) and sr[i] is not None) else None
            ])
            
    filename = f"{base_filename}_sd.csv"
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Second Difference", "Count", "Percentage"])
        sd_counter = Counter(sd)
        total_count = len(sd)
        for sd, count in sd_counter.most_common():
            writer.writerow([sd, count, 100 * count / total_count])

    filename = f"{base_filename}_sr.csv"
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Second Ratio (Fraction)", "Count", "Percentage"])
        sr_counter = Counter(sr)
        total_count = len(sr)
        for sr, count in sr_counter.most_common():
            writer.writerow([str(sr), count, 100 * count / total_count])

    filename = f"{base_filename}_state.pkl"
    with open(filename, 'wb') as file:
        pickle.dump((primes, sd, sr), file)

def calculate_sd_sr_combinations(sd, sr):
    sd_sr_combinations = list(zip(sd, sr))
    return Counter(sd_sr_combinations)

# Write the combinations of second differences and second ratios to a CSV file.
def write_sd_sr_combinations_to_csv(sd_sr_combinations, base_filename):
    total_count = sum(sd_sr_combinations.values())
    filename = f"{base_filename}_sd_sr_combinations.csv"
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Second Difference", "Second Ratio (Fraction)", "Count", "Percentage"])
        for (sd, sr), count in sd_sr_combinations.most_common():
            writer.writerow([sd, str(sr), count, 100 * count / total_count])

            
# Write a README file for the dataset that that includes full prime number
def write_dataset_readme(output_directory, start_prime, num_primes, left_digits):
    readme_text = f"""
    # primedifex.py Prime Difference Explorer Dataset

    This dataset was generated by primedifex.py, the Prime Difference Explorer. It contains a sequence of {num_primes} primes, starting from the prime after {start_prime}.

    The CSV files in this directory contain information about the primes, their second differences, second ratios, and combinations of second differences and second ratios. Note that the primes in the CSV files are truncated to their last 10 digits to save space.

    To reconstitute a full prime from a truncated prime, append the last 10 digits of the prime to these "left digits" '{left_digits}'.

    Note: This method assumes that the difference between consecutive primes in this dataset is less than 10^10, which is generally true for large primes.
    """
    with open(os.path.join(output_directory, "README.md"), 'w') as readme_file:
        readme_file.write(readme_text)

        
# Find sets of primes with specific differences (named prime sets, like "twin primes").
def find_named_prime_sets(primes):
    named_prime_sets = {
        "Twin primes": [],
        "Cousin primes": [],
        "Sexy primes": [],
        "Octo primes": [],
        "Deca primes": [],
        "Dodeca primes": [],
    }
    named_prime_gaps = {
        "Twin primes": 2,
        "Cousin primes": 4,
        "Sexy primes": 6,
        "Octo primes": 8,
        "Deca primes": 10,
        "Dodeca primes": 12,
    }
    for i in range(len(primes) - 1):
        diff = primes[i + 1] - primes[i]
        for name, gap in named_prime_gaps.items():
            if diff == gap:
                named_prime_sets[name].append((str(primes[i])[-10:], str(primes[i + 1])[-10:]))
    return named_prime_sets

# Write the totals of named prime sets to a CSV file.
def write_named_prime_sets_totals_to_csv(named_prime_sets, base_filename):
    filename = f"{base_filename}_named_prime_sets_totals.csv"
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Total"])
        for name in named_prime_sets.keys():
            writer.writerow([name, len(named_prime_sets[name])])

            
# Write the named prime sets to a CSV file.            
def write_named_prime_sets_to_csv(named_prime_sets, base_filename):
    filename = f"{base_filename}_named_prime_sets.csv"
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Prime Set"])
        for name in named_prime_sets.keys():
            for prime_set in named_prime_sets[name]:
                writer.writerow([name, prime_set])

# Generate the text for the README file.                
def generate_readme_text(first_prime, num_bits, num_primes):
    readme_text = f"""
    # Prime Difference Explorer Dataset

    This dataset was generated by the Prime Difference Explorer. It contains a sequence of {num_primes} primes, starting from the prime after {first_prime}.

    The CSV files in this directory contain information about the primes, their second differences, second ratios, and combinations of second differences and second ratios. Note that the primes in the CSV files are truncated to their last 10 digits to save space.

    To reconstitute a full prime from a truncated prime, append the last 10 digits of the prime to the left digits '{str(first_prime)[:-10]}'.

    Note: This method assumes that the difference between consecutive primes in this dataset is less than 10^10, which is generally true for large primes.
    """
    return readme_text


# Write the primes, second differences, and second ratios to a CSV file.
def write_primes_to_csv(primes, second_differences, second_ratios, base_filename):
    with open(base_filename + "_primes.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Prime", "Second Difference", "Second Ratio"])
        for i in range(len(second_differences)):
            writer.writerow([str(primes[i + 1])[-10:], second_differences[i], second_ratios[i]])




# Write the second differences to a CSV file.
def write_second_differences_to_csv(second_differences, base_filename):
    filename = base_filename + "_sd.csv"
    sd_counter = Counter(second_differences)
    total_counts = len(second_differences)
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Second Difference", "Count", "Percentage"])
        for sd, count in sd_counter.most_common():
            writer.writerow([sd, count, count / total_counts * 100])

            
# Write the second ratios to a CSV file.
def write_second_ratios_to_csv(second_ratios, base_filename):
    filename = base_filename + "_sr.csv"
    sr_counter = Counter(second_ratios)
    total_counts = len(second_ratios)
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Second Ratio", "Count", "Percentage"])
        for sr, count in sr_counter.most_common():
            writer.writerow([sr, count, count / total_counts * 100])

# The main function that runs the prime sequence exploration from a configuration file.            
def run_from_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)

    miller_rabin_iterations = config.get('miller_rabin_iterations', 5)  # Use 5 as the default

    if config['start_number'] == "random":
        start_number = generate_random_number(config['num_bits'])
    else:
        start_number = config['start_number']

    print("Generating primes...")
    primes = find_prime_sequence(start_number, config['num_primes'], miller_rabin_iterations, verbose=True)
    print("Calculating second differences...")
    second_differences = calculate_second_differences(primes)
    print("Calculating second ratios...")
    second_ratios = calculate_second_ratios(primes)
    print("Calculating SD-SR combinations...")
    sd_sr_combinations = calculate_sd_sr_combinations(second_differences, second_ratios)
    sd_sr_combinations = Counter(sd_sr_combinations) 
    print("Calculating named prime sets...")
    named_prime_sets = find_named_prime_sets(primes)
    print("Done!")
    
    if config['write_output']:
        output_directory = create_output_directory(config['num_bits'], config['num_primes'])
        # Copy the configuration file to the output directory
        shutil.copy2(config_file, os.path.join(output_directory, "config.json"))
        # Write the prime truncation prefix to a README file
        with open(os.path.join(output_directory, "README.md"), 'w') as file:
            file.write(generate_readme_text(primes[0], config['num_bits'], config['num_primes']))

        base_filename = os.path.join(output_directory, f"{config['num_bits']}bit{config['num_primes']}")

        if config.get('output_primes', True):
            write_primes_to_csv(primes, second_differences, second_ratios, base_filename)
        if config.get('output_second_differences', True):
            write_second_differences_to_csv(second_differences, base_filename)
        if config.get('output_second_ratios', True):
            write_second_ratios_to_csv(second_ratios, base_filename)
        if config.get('output_sd_sr_combinations', True):
            write_sd_sr_combinations_to_csv(sd_sr_combinations, base_filename)
        if config.get('output_named_prime_sets', True):
            write_named_prime_sets_to_csv(named_prime_sets, base_filename)
        if config.get('output_named_prime_sets_totals', True):
            write_named_prime_sets_totals_to_csv(named_prime_sets, base_filename)


        
    return primes, second_differences, second_ratios, sd_sr_combinations, named_prime_sets
