import time
from concurrent.futures import ThreadPoolExecutor
from typing import Tuple

def formula_1(x: int) -> int:
    return x**2 - x**2 + x*4 - x*5 + x + x

def formula_2(x: int) -> int:
    return x + x

def compute_step(formula, iterations: int) -> Tuple[int, float]:
    start_time = time.time()
    result = sum(formula(x) for x in range(iterations))
    duration = time.time() - start_time
    return result, duration

def parallel_computations(iterations: int) -> Tuple[float, float, float]:
    with ThreadPoolExecutor(max_workers=2) as executor:
        future1 = executor.submit(compute_step, formula_1, iterations)
        future2 = executor.submit(compute_step, formula_2, iterations)
        
        result1, duration1 = future1.result()
        result2, duration2 = future2.result()

    start_time_step3 = time.time()
    result3 = result1 + result2
    duration3 = time.time() - start_time_step3

    return duration1, duration2, duration3

iterations_list = [10000, 100000, 23232312] # добавил 3 вариант по приколу чтобы проверить

for iterations in iterations_list:
    duration1, duration2, duration3 = parallel_computations(iterations)
    print(f"\nИтерации: {iterations}")
    print(f"Длительность шага 1: {duration1:.6f} секунд")
    print(f"Длительность шага 2: {duration2:.6f} секунд")
    print(f"Длительность шага 3: {duration3:.6f} секунд")
