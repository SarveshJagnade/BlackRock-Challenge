import time
import psutil
import threading

class PerformanceService:

    @classmethod
    async def get_metrics(cls, start_time):
        duration = time.time() - start_time
        memory = psutil.Process().memory_info().rss / (1024 * 1024)
        threads = threading.active_count()

        return {
            "time": f"{duration:.3f}s",
            "memory": f"{memory:.2f} MB",
            "threads": threads
        }