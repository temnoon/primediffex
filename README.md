# primediffex
# README

## Prime Difference Explorer

Prime Explorer is a Python project that explores the properties of prime numbers. It generates prime numbers, calculates their second differences and second ratios, identifies specific sets of primes (such as twin primes, cousin primes, and others), and writes these results to various output files.

# Second Differences and Second Ratios of Prime Numbers

In number theory, the sequence of prime numbers is of fundamental importance. While we understand a lot about how primes are distributed (for instance, the Prime Number Theorem gives us an approximation for how many primes are less than a given size), there are still many open questions related to the properties of primes. My interest is more in these sequences, which just exist out there in the field of prime relations, in a precise and discoverable way. I see this software as a way of exploring and mapping an enormous universe of simple inevitable and timeless values which are bound as attributes to specific primes. 

## Second Differences

The Second Difference of a sequence is a measure of how the differences between terms in the sequence change. For the sequence of prime numbers, the First Difference between two primes \(p_{n+1}\) and \(p_n\) is simply the gap between them: \(p_{n+1} - p_n\). 

For example, if we have the sequence of prime numbers 2, 3, 5, 7, 11, the First Differences are 1 (3-2), 2 (5-3), 2 (7-5), and 4 (11-7).

The Second Difference is then the difference of these First Differences. In our example, the Second Differences are 1 (2-1), 0 (2-2), and 2 (4-2). 

Second Differences can give us insights into how the gaps between primes change. For instance, we know that except for the gap between 2 and 3, all other gaps are even numbers, because primes (other than 2) are always odd. 

## Second Ratios

The Second Ratio of a sequence is a measure of how the ratios between terms in the sequence change. For the sequence of prime numbers, the First Ratio between two primes \(p_{n+1}\) and \(p_n\) is the ratio between them: \(p_{n+1} / p_n\). 

For example, if we have the sequence of prime numbers 2, 3, 5, 7, 11, the First Ratios are 1.5 (3/2), 1.67 (5/3), 1.4 (7/5), and 1.57 (11/7).

The Second Ratio is then the ratio of these First Ratios. In our example, the Second Ratios are 1.11 (1.67/1.5), 0.84 (1.4/1.67), and 1.12 (1.57/1.4).

Second Ratios can give us insights into how the relative sizes of primes change. Studying these can provide us with deeper understanding of prime distribution and density.

Keep in mind that while these properties can provide insights into the nature of prime numbers, many aspects about the distribution of primes remain deeply mysterious and are the subject of ongoing research in number theory.


## How to Run the Prime Difference Explorer

1. Ensure that you have Python 3.6 or later installed.

2. Install the required Python packages by running `pip install -r requirements.txt` in your terminal. The addition of the animation and visualization function with v0.22 requires several packages, beyond the sympy required by the prime generation. 

4. Modify the `config.json` file to specify your desired parameters for the prime number generation and analysis. The parameters you can specify are described in the "Configuration Parameters" section below.

5. I run the software with "primes, sd, sr, sd_sr_combinations, named_prime_sets = run_from_config('config.json')" in a Jupyter notebook, connected to the home directory of the app. 

6. The script will generate the prime numbers and perform the analyses as specified in your `config.json` file. The results will be written to output files in the same directory as the script.

## Configuration Parameters

In the `config.json` file, you can specify the following parameters:

- `num_bits`: The bit length of the generated primes. 

- `num_primes`: The number of primes to generate.

- `start_number`: The starting number for the prime number generation. If "random", a random start number will be chosen.

- `output_primes`: Whether to output a CSV file with the last 10 digits of each prime number, its second difference, and its second ratio.

- `output_second_differences`: Whether to output a CSV file with the counts and percentages of the second differences.

- `output_second_ratios`: Whether to output a CSV file with the counts and percentages of the second ratios.

- `output_sd_sr_combinations`: Whether to output a CSV file with the counts of the second difference-second ratio combinations.

- `output_named_prime_sets`: Whether to output a CSV file with the named prime sets (pairs of primes with specific gaps).

- `output_named_prime_sets_totals`: Whether to output a CSV file with the total counts of the named prime sets.

- `miller_rabin_iterations`: The number of iterations to use in the Miller-Rabin primality test.
  
- `num-digits`: best practice is to set this to 'auto' to allow the software to determine the number of digits needed to be displayed, so extras can be truncated for long primes.
  
- `prime_sets`: a list of the gap between primes which should be captured by prime sets. Capturing all in large dataset can get very large. The largest set the software is prepared to deal with is [2,4,6,8,10,12]. Any smaller subset should work. 


## Output Files

The output files that can be generated by Prime Explorer are as follows:

-  Output Directory named `[number of bits]bits[number of primes][timestamp]`
   inside the output directory are the following files. 

- `metadata.json`: has information about the dataset, notably the full prime number, and the most significant digits of the prime that can be concatenated onto the left of the truncated primes which are used in the other output files. This keeps massive primes from taking up unnecessary space in the files. 

- `primes.csv`: Contains the last 10 digits of each prime number, its second difference, and its second ratio.

- `second_differences.csv`: Contains the counts and percentages of the second differences.

- `second_ratios.csv`: Contains the counts and percentages of the second ratios.

- `sd_sr_combinations.csv`: Contains the counts of the second difference-second ratio combinations.

- `named_prime_sets.csv`: Contains the named prime sets (pairs of primes with specific gaps, like 'twin primes').

- `named_prime_sets_totals.csv`: Contains the total counts of the named prime sets.

# Animations and Visualizations

In the Jupyter Notebook Primediffex0.23-w-Visualizations0.21.ipynb Animations and visualizations were introduced which use the primediffex output files to create visual output. 


# Animation of Prime Differences and Ratios

This codebase includes a feature to animate the progress of the second differences and second ratios of the sequence of prime numbers. This can be a helpful visual tool for understanding the properties and behavior of these sequences.

## Function Overview

The main function to run the animation is `run_config_animation(directory_path)`. This function takes as input a directory path which should contain the necessary files for running the animation.

The necessary files are:

- A CSV file with the prime numbers and their second differences and second ratios. This file should have the columns `Prime`, `Second Difference`, `Second Ratio (Decimal)`, and `Second Ratio (Fraction)`.
- A CSV file with the frequency counts of the second differences.
- A CSV file with the frequency counts of the second ratios.
- A metadata JSON file with metadata about the prime number sequence.

The filenames of these files are derived from the directory name. For example, if the directory name is '10bit1000_20230717_165833', the expected filenames would be '10bit1000_primes.csv', '10bit1000_sd.csv', '10bit1000_sr.csv', and 'metadata.json'.

The function first checks that these files exist in the given directory. It then loads the data from the files and creates the animation. The animation shows a circle whose radius represents the absolute value of the second difference, and a small particle on the x-axis representing the second ratio. The color of the circle and the particle is determined by the rank of the corresponding second difference and second ratio in their frequency counts.

The function outputs an MP4 file with the animation. The filename of the output file is also derived from the directory name, with '_animation.mp4' appended. For example, the output file for the above directory would be '10bit1000_animation.mp4'.

While the animation is being created, the function provides feedback on its progress through print statements and a progress bar. When the animation is done, the function returns the path to the output file.

## Usage

You can run the animation function as follows:

```python
ani = run_config_animation('10bit1000_20230717_165833')
```

This will create an animation based on the files in the '10bit1000_20230717_165833' directory and save it to '10bit1000_animation.mp4' in the same directory. The path to the output file is also returned by the function.

Please note that creating the animation can take some time, especially for large sequences of prime numbers.

This animation function is a great way to visualize and understand the behavior of the second differences and second ratios of prime numbers. We hope you find it helpful!
### Charting Distributions

There are two functions for creating histograms of the second difference and second ratio distributions:

```python
plot_sd_distribution('your_file_primes.csv')
plot_sr_distribution('your_file_primes.csv')
```

These functions create a histogram showing the distribution of second differences or second ratios, and save the plot as a PNG file in the same directory as the input file. The filename will be the same as the input file's name, with '_sd_distribution_plot.png' or '_sr_distribution_plot.png' appended.

### Calculating +/- Bias in a dataset.

To calculate the bias in the second differences or second ratios, use the `calculate_sd_bias(filename)` or `calculate_sr_bias(filename)` functions:

```python
calculate_sd_bias('your_file_here.csv')
calculate_sr_bias('your_file_here.csv')
```

These functions will return a bias score, which represents the bias towards positive or negative second differences or second ratios in the data. The score is a number between -1 and 1, where -1 indicates a bias towards negative values, 1 indicates a bias towards positive values, and 0 indicates no bias.

### About the Miller-Rabin Algorithm

The Miller-Rabin algorithm is a probabilistic test to check whether a number is a composite or probably prime. It was first discovered by Gary L. Miller and later improved by Michael O. Rabin.

The algorithm is based on the following claim:

**Claim:** Let \( n \) be an odd prime number and \( n-1 = 2^s \cdot d \) with \( d \) odd. Then for any number \( a \) such that \( 2 \leq a \leq n-2 \), one of the following statements is true:
1. \( a^d \equiv 1 \mod n \)
2. \( a^{2^r \cdot d} \equiv -1 \mod n \) for some \( r \) such that \( 0 \leq r \leq s-1 \)

In other words, if \( n \) is a prime number, then either \( a^d \) is 1 modulo \( n \), or \( a^{2^r \cdot d} \) is -1 modulo \( n \) for some \( r \). If neither of these conditions is met, then \( n \) is definitely composite.

The Miller-Rabin algorithm uses this claim to test whether a number is prime. It picks a random number \( a \), and checks whether the claim holds. If the claim fails to hold, then \( n \) is composite. If the claim holds, then \( n \) is probably prime. By repeating the test with multiple randomly chosen values of \( a \), we can increase our confidence that \( n \) is indeed prime. 

Here is the pseudocode for the Miller-Rabin primality test:

```
Input: n > 2, an odd integer to be tested for primality;
       k, a parameter that determines the number of times the test is repeated

write n − 1 as 2^r·d with d odd by factoring powers of 2 from n − 1

LOOP repeat k times:
    pick a random integer a in the range [2, n − 2]
    x ← a^d mod n
    if x = 1 or x = n − 1 then do next LOOP
    for i = 1 to r − 1
        x ← x^2 mod n
        if x = n − 1 then do next LOOP
    return composite

return probably prime
```

You can use a fixed random seed and control the number of iterations to make the test deterministic. The random seed is used to generate the random integers \( a \), and the number of iterations determines how many times the test is repeated. By fixing these values, you can get the same result every time you run the test.

For example, in Python:

```python
import random

def miller_rabin(n, k, seed=1):
    # Use the seed for the random number generator
    random.seed(seed)

    # The rest of the algorithm as described in the pseudocode...

# Run the test with a fixed seed and a specific number of iterations
print(miller_rabin(561, 5, seed=12345))  # Prints 'composite'
```

This will give the same result every time it is run, because the random numbers generated by `random.randint(2, n - 2)` will be the same every time.

Please note that while the Miller-Rabin test is very fast and accurate for small numbers, it is a probabilistic test and there is a very small chance that it can report a composite number as "probably prime". The chance of a false positive decreases as the number of iterations increases. 

Also, note that using a fixed seed for the random number generator can impact the accuracy of the test, because it always tests the same sequence of 'a' values. It is generally better to use a different random seed each time you run the test, unless you have a specific reason for wanting the results to be deterministic.

## Loading the Pickle File

Prime Explorer saves its state to a pickle file after each run. You can load this pickle file to inspect the state of the Prime Explorer at the end of its last run.

Here's a Python snippet that loads the pickle file:

```python
import pickle

with open('state.pkl', 'rb') as f:
    state = pickle.load(f)

# `state` is now a dictionary that contains the primes, second differences, second ratios, 
# second difference-second ratio combinations, and named prime sets generated in the last run.
```

Replace `'state.pkl'` with the path to your pickle file if it's different.

# Changelog

### Version 0.2.0
- **Added**: New parameter "prime_sets" in config file to specify which prime sets to find.
- **Changed**: Updated "find_named_prime_sets" function to only compute specified prime sets.
- **Fixed**: Bug where the software would calculate prime sets twice. 
- **Fixed**: Bug in the "auto" truncation mode that resulted in overly large truncations.

# README Additions

## Prime Sets
In addition to exploring prime second differences and second ratios, the Prime Difference Explorer can also find specific sets of primes. The software recognizes the following sets, each identified by the difference between the primes in the set:

- Twin primes (difference of 2)
- Cousin primes (difference of 4)
- Sexy primes (difference of 6)
- Octo primes (difference of 8)
- Deca primes (difference of 10)
- Dodeca primes (difference of 12)

To specify which sets you want the software to find, add a "prime_sets" parameter to your configuration file. The value should be a list of the differences that identify each set. For example, to find twin primes and cousin primes, your configuration file would include:

```json
"prime_sets": [2, 4]
```

If you want the software to find all the recognized sets, you would use:

```json
"prime_sets": [2, 4, 6, 8, 10, 12]
```

If the "prime_sets" parameter is omitted from the configuration file, the software will not find any prime sets.

The software outputs a CSV file for each prime set that it finds. The file contains each pair of primes in the set, identified by their last 10 digits. To reconstitute a full prime from a truncated prime, append the last 10 digits of the prime to the left digits specified in the README file for the dataset.

## Updates in Version 0.2.0
In this version, we added the ability to specify which prime sets you want the software to find. This allows you to focus on specific sets without having to compute all of them, which can save a significant amount of time and space when dealing with large prime sequences. We also fixed a bug where the software would calculate prime sets twice, and a bug in the "auto" truncation mode that resulted in overly large truncations.

## Updates in Version 0.2.1

"random_seed" now supported as a config parameter. Allows the usual control over randomness that seeds afford.

Pickle file now Gzip'd. 

truncation parameter "num_digits": "auto" allows the software to choose the smallest effective truncation when prime is large. 

Sample new config file

```json
{
"random_seed": 9999,
"num_bits": 256,
"num_primes": 10000,
"start_number": "random",
"write_output": true,
"output_primes": true,
"output_second_differences": true,
"output_second_ratios": true,
"output_sd_sr_combinations": true,
"output_named_prime_sets": true,
"output_named_prime_sets_totals": true,
"miller_rabin_iterations": 5,
"num_digits": "auto",
"prime_sets": [2, 4]
}
```
## Updates in Version 0.2.2

Improved labeling in Animations.mp4.

SD and SR Distribution charts

Bias scaler calculation.
## Updates in Version 0.2.3

Fixed bug in the labeling in SD_Distribution chart. 

## Caveat

ChatGPT 4.0 was used in developing this code. 
