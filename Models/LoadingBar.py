import threading
import time

from alive_progress import alive_bar

lock = threading.Lock()
should_stop = threading.Event()


class Status:
    is_complete = False


def done_loading():
    Status.is_complete = not Status.is_complete
    # should_stop.set()


def loading_bar(steps, message):
    # print(message)
    try:
        with alive_bar(steps, force_tty=True, title=message) as bar:
            for i in range(steps):
                if Status.is_complete:
                    # Skipping to the end of the progress bar
                    bar(skipped=True)
                    continue
                else:
                    time.sleep(0.1)
                    bar()

        done_loading()
    except Exception as e:
        done_loading()
        print(f"An error occurred during loading: {e}")


def start_loading(message, steps=100):
    thread = threading.Thread(target=loading_bar, args=(steps, message))
    thread.daemon = True
    thread.start()
    return thread
