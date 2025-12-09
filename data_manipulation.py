# data_manipulation.py
# ENDG 233 F24
# By Sam Katevatis
# 30281498
# A terminal-based data analysis and visualization program in Python.
# You must follow the specifications provided in the project description.

import numpy as np
import math

def get_standard_deviation(numbers):
    """
    Calculates the standard deviation of a set of numbers

    Args:
        numbers (List): A full dataset to analyze the volitility of

    Returns:
        float: The standard deviation of the dataset in %± 
    """
    values = np.array(numbers) # Creates an ndarray of the dataset
    variance = sum((x - np.mean(values)) ** 2 for x in values) / (len(values) - 1) # Calculates variance
    return math.sqrt(variance) # Returns standard deviation

def linear_aproximation(data):
    """
    Performs a linear aproximation of the next value in a sequence of values

    Args:
        data (List): A list of values used to aproximate the next one in the set

    Returns:
        float: The approximate value of the next item in the sequence
    """
    quarters = np.arange(len(data)) + 1 # Create a list of number of quarters
    next_quarter = len(data) + 1 # Get the index of the next quarter
    data_avg = np.mean(data) # Get the average
    quarter_avg = np.mean(quarters) # Get the average number of quarters
    
    # Perform the linear regression
    regression = np.sum((quarters -  quarter_avg)*(data - data_avg) / np.sum((quarters - quarter_avg)**2))
    linear_regression = data_avg + (regression * (next_quarter - quarter_avg))

    return linear_regression # return the value

def is_float(text):
    """
    Determines if a string can be cast to a float

    Args:
        text (string): The string to be analyzed

    Returns:
        bool: If true, the string can be cast to a float. If false, it cannot be cast
    """
    # Define what characters can be turned into a float
    allowed_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "-"]
    
    # Determine if any chars are not allowed
    for char in text:
        if char not in allowed_chars:
            return False
    return True

def is_int(text):
    """
    Determines if a string can be cast to an int

    Args:
        text (string): The string to be analyzed

    Returns:
        bool: If true, the string can be cast to an int. If false, it cannot be cast
    """
    # Define what characters can be turned into an int
    allowed_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-"]
    
    # Determine if any chars are not allowed
    for char in text:
        if char not in allowed_chars:
            return False
    return True


