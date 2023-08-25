"""
    Maximum Threads = Available RAM / Thread Memory
    Maximum Threads = 8000 MB / 8 MB = 1000 threads (approximately)

    A single CPU core can have up-to 2 threads per core. For example, if a CPU is dual core (i.e., 2 cores) it will have 4 threads. And if a CPU is Octal core (i.e., 8 core) it will have 16 threads and vice-versa.


    Q1. I want to write 1 bilions records into postgres using python. There what should I use multi processing or multi threading ?

    Ans: 
        When dealing with a task like writing a large number of records (1 billion records) into a database like PostgreSQL, the choice between multiprocessing and multithreading depends on the nature of the task and the resources available.

        I/O-Bound Task (Recommended for this case): If the process is mainly I/O-bound, which means it involves a lot of waiting for I/O operations (like database writes), then multithreading can be a good choice. Python's threading module can help you manage concurrent I/O operations efficiently. Since the GIL doesn't affect I/O-bound tasks much, threads can effectively run in parallel for I/O tasks.

        CPU-Bound Task: If the task involves a significant amount of CPU computation, then multiprocessing might be a better option. This allows you to take advantage of multiple CPU cores and achieve true parallelism. However, keep in mind that due to the GIL, Python's multiprocessing module can still be limited in terms of CPU-bound tasks, and you might want to consider using other parallelization libraries that work around this limitation.

        In your case, since you're writing records to PostgreSQL, which is primarily an I/O operation, using multithreading with the threading module is a reasonable choice. Each thread can manage a separate database connection and write records concurrently. Be sure to manage the number of threads to avoid overwhelming the database with too many simultaneous connections.
"""

import time
import threading
from blessed import Terminal


def print_progress_bar(term, y, progress):
    bar_length = 20
    block = int(round(bar_length * progress))
    progress_str = f"{progress*100:.2f}%"
    bar = "[" + "=" * block + " " * (bar_length - block) + "]"
    print(term.move_yx(y, 0) + f"Bar {y}: {bar} {progress_str}")

def update_progress(term, y):
    for i in range(101):
        progress = i / 100
        print_progress_bar(term, y, progress)
        time.sleep(0.05)  # Simulate some work being done

def main():
    term = Terminal()
    with term.fullscreen(), term.hidden_cursor():
        threads = []
        for y in range(1, 5):
            thread = threading.Thread(target=update_progress, args=(term, y))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

if __name__ == "__main__":
    main()
