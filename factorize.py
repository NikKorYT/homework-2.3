import time
import multiprocessing

def fectorize_number(number):
    """
    This function takes a single number and returns a list of its factors.
    """
    results = []
    for divisor in range(1, number + 1):
        if number % divisor == 0:
            results.append(divisor)
    return results

def factorize(*numbers) -> list:
    """
    This function takes a list of numbers and returns a list of lists containing the factors of each number.
    Uses multiprocessing to factorize numbers in parallel.
    """
    with multiprocessing.Pool() as pool:
        return pool.map(fectorize_number, numbers)


if __name__ == "__main__":

    start_time = time.time()

    a, b, c, d = factorize(128, 255, 99999, 10651060)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    print("Factors of 128 are correct.")
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    print("Factors of 255 are correct.")
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    print("Factors of 99999 are correct.")
    assert d == [
        1,
        2,
        4,
        5,
        7,
        10,
        14,
        20,
        28,
        35,
        70,
        140,
        76079,
        152158,
        304316,
        380395,
        532553,
        760790,
        1065106,
        1521580,
        2130212,
        2662765,
        5325530,
        10651060,
    ]
    print("Factors of 10651060 are correct.")
    print("All tests passed successfully.")

    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
