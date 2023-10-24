def is_prime(n):
    """Return True if n is a prime number, False otherwise."""
    # edge cases
    if n == 2 or n == 3: return True
    if n % 2 == 0 or n == 1: return False
    
    # check from 3 to square root of n
    for i in range(3, int(n ** 0.5) + 1, 2): 
        if n % i == 0:
            return False
    return True

def find_primes(n):
    """Return list of prime numbers up to n."""
    primes = [i for i in range(2, n) if is_prime(i)]
    return primes

# upper limit
high_num = 100

# call our function, print the primes
primes = find_primes(high_num)

print(primes)
