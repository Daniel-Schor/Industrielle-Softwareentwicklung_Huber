class custom_context_manager:

    def __init__(self):
        self._counter = 0

    def __enter__(self):
        print("Entering the context")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting the context")
        self._counter = 0

    def _increment(self):
        self._counter += 1

    def get_counter(self):
        return self._counter

if __name__ == "__main__":
    with custom_context_manager() as ccm:
        print("Inside the context")
        
        ccm._increment()

        print(ccm.get_counter())

    print(ccm.get_counter())