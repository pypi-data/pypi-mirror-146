class Calculator:

    """
       Calculator is set to perform these functions:
       - Addition
       - Multiplication
       - Subtraction
       - Division
       - nth root calculation
       - Memory reset
       - Print out memory
    """

    def __init__(self) -> None:
        self.memory = 0.0

    # This function adds number to memory
    def add(self, digit: float) -> float:
        try:
            self.memory += digit
        except TypeError:
            print("Please enter a valid number:")
        return self.memory

    # This function subtracts number from memory
    def subtract(self, digit: float) -> float:
        try:
            self.memory -= digit
        except TypeError:
            print("Please enter a valid number:")
        return self.memory

    # This function multiplies memory by number
    def multiply(self, digit: float) -> float:
        try:
            self.memory *= digit
        except ZeroDivisionError:
            return 1.0
        except TypeError:
            print("Please enter a valid number:")
        return self.memory

    # This function divides memory by number
    def divide(self, digit: float) -> float:
        try:
            self.memory /= digit
        except ZeroDivisionError:
            return 0.0
        except TypeError:
            print("Please enter a valid number:")
        return self.memory

    # This function calculates n root of memory
    def n_root(self, digit: float) -> float:
        try:
            self.memory **= (1.0/float(digit))
        except TypeError:
            print("Please enter a valid number:")
        return self.memory

    # This function resets memory to 0.0
    def memory_reset(self) -> float:
        self.memory = 0.0

    @property
    def return_memory(self):
        return self.memory

    @return_memory.setter
    def return_memory(self) -> None:
        print("Memory cannot be changed!")