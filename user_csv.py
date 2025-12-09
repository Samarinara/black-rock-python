# user_csv.py
# ENDG 233 F24
# By Sam Katevatis
# 30281498
# A terminal-based data analysis and visualization program in Python.
# You must follow the specifications provided in the project description.

import data_manipulation as dm

def read_csv(filename, include_headers=True):
    """
    Read a csv and turn it into a 2D list

    Args:
        filename (string): name of the csv to read
        include_headers (bool, optional): Determines if the 2D list should contain the csv headers. Defaults to True

    Returns:
        list: A 2D list representation of the csvs
    """
    file_text = open(filename) # Open the file
    
    # Turns the whole file into a 2D list
    file_list = []
    for line in file_text:
        line_list = line.split(",") # Split the line by commas

        # Conver the item to a float if possible
        for i, item in enumerate(line_list):
            if dm.is_float(item):
                line_list[i] = float(item)

        file_list.append(line_list)

    # Removes the first entry if there shouldn't be headers
    if include_headers != True:
        file_list.pop(0)

    # Close the file and return the list
    file_text.close()
    return file_list

def write_csv(filename, data, overwrite):
    """
    Transforms a 2D list into a csv file

    Args:
        filename (string): name of the file to write
        data (list): The 2D list to convert
        overwrite (bool): A flag to indicate whether you are overwriting or appending to an existing file
    """
    # Determine the operator on f.write() based on the overwrite bool
    operator = "w"
    if overwrite == False:
        operator = "a"

    # open the file 
    with open(filename, operator) as f:
        for line in data:
            # Construct each line as a string
            line_string = ""
            for item in line:
                line_string += str(item)
                line_string += ","
            
            # Format the line
            output_string = line_string[0:(len(line_string) - 1)]
            output_string += "\n"

            # Add the line to the end of the file
            f.write(output_string)

