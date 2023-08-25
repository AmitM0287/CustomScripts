"""
    Q1. I want to generate 1 bilions random records for employees using python. There what should I use multi processing or multi threading ?

    Ans: 
        Generating 1 billion random records for employees is a CPU-bound task since it involves a significant amount of computation to generate random data. In this case, using multiprocessing would be more appropriate than multithreading.

        Python's multiprocessing module can help you take advantage of multiple CPU cores, allowing you to achieve true parallelism for CPU-bound tasks. Each process will run independently and utilize a separate CPU core, which can significantly speed up the generation of such a large amount of data.

        Note that while multiprocessing is suitable for CPU-bound tasks, it can introduce some overhead due to the creation of processes and inter-process communication. For tasks like this, consider using external libraries like joblib or exploring distributed computing frameworks like Apache Spark for even more efficient parallelization and scalability.
"""

import time
import multiprocessing
from tqdm import tqdm


def update_progress(bar_number, progress_queue):
    for i in range(101):
        progress = i / 100
        progress_queue.put((bar_number, progress))
        time.sleep(0.05)  # Simulate some work being done

if __name__ == "__main__":
    processes = []
    progress_queue = multiprocessing.Queue()

    for i in range(1, 5):
        process = multiprocessing.Process(target=update_progress, args=(i, progress_queue))
        processes.append(process)
        process.start()

    try:
        pbar_dict = {i: tqdm(total=100, desc=f"Bar {i}", position=i-1, leave=False) for i in range(1, 5)}

        while any(process.is_alive() for process in processes):
            while not progress_queue.empty():
                bar_number, progress = progress_queue.get()
                pbar_dict[bar_number].update(int(progress * 100) - pbar_dict[bar_number].n)
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

    for process in processes:
        process.terminate()
        process.join()

    for pbar in pbar_dict.values():
        pbar.close()

    print()  # Print a newline to separate the progress bars from subsequent output
