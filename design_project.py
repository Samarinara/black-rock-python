# design_project.py
# ENDG 233 F24
# By Sam Katevatis
# 30281498
# A terminal-based data analysis and visualization program in Python.
# You must follow the specifications provided in the project description.

import user_csv
import data_manipulation as dm

import matplotlib.pyplot as plt
import numpy as np
import math

def pick_exchange():
    """
    Prompt the user to pick a stock exchange from the available options

    Args: None

    Returns:
        int: The index of the chosen exchange
    """
    # Display the menu
    print("Please choose a stock exchange by inputting a number from the list below:")
    print("\t1: American Stock Exchange (NASDAQ)")
    print("\t2: Toronto Stock Exchange (TSX)")
    print("\t3: European Stock Exchange (XETR)")
    print("\t0: Exit")

    valid_choices = ["0", "1", "2", "3"] # Define valid options

    # Get the input
    choice = input(">> ") 
    choice.strip()

    # return the choice if its a valid input, but loop around if not valid
    if choice in valid_choices:
        return int(choice)
    else:
        print("\n\nPLEASE ENTER A VALID OPTION")
        return pick_exchange()

def load_data(exchange):
    """
    Load the data for a specific exchange. This function exists to clean up repeated code

    Args:
        exchange (string): The name of the exchange (eg. NASDAQ)

    Returns:
        list: A 2D list not including the headers
    """
    # Call read_csv
    raw_data = user_csv.read_csv("data_files/" + exchange + ".csv", False)
    return raw_data # return the list

def main_menu(exchange):
    """
    Displays the main menu and returns the selection

    Args:
        exchange (string): Used to customize the menu based on selected exchange

    Returns:
        string: The user's choice
    """

    # Display the menu
    print("\nWelcome to the main menu!")
    print("- DISCLAIMER: All prices are converted to USD from CAD and EUR respectively based on the exchnage rate on 1-12-25")
    print("- It also may be helpful to know that the data was gathered from Yahoo Finance in Q4 2025")
    print(f"You have selected the {exchange} exchange")
    print("Please pick an option below:")

    print("\t1: Graph the financial analysis of a specific stock")
    print("\t2: Compare volitility against another exchange")
    print(f"\t3: Find the most profitable stock next quarter in the {exchange} exchange")
    print("\t0: Choose new exchange")

    # Collect and return the input
    choice = input(">> ")
    return choice.strip()

def single_stock_financial_analysis(data):
    """
    Displays 2 subplots analyzing a stocks financial numbers and profiatability

    Args:
        data (list): All of the data for the selected exchange

    Returns: None
    """

    # Display menu
    print("\nPlease input a stock ticker to analyze (Type 'help' to see all available stocks)")
    print("Please note, if the stock is not registered on the selected exchange you will not be able to select it")
    
    ticker = input(">> ").upper() # Collect input 

    # Display all possible tickers if the user asks for help 
    if ticker == "HELP":
        # Build the list
        tickers = []
        for row in data:
            tickers.append(row[0])
        cols = len(tickers)

        # Format and print the list
        help_menu = [tickers[i:i+cols] for i in range(0, len(tickers), cols)]
        for line in help_menu:
            row = ""
            for item in line:
                row += item + "\t"
            print(row)
        
        # Loop back around with the list displayed
        single_stock_financial_analysis(data)
        return

    # Extract just the row with the selected ticker
    company = []
    for row in data:
        if row[0] == ticker:
            company = row
            break

    # Loop around with an error message if the ticker can't be found
    if company == []:
        print("\nThe ticker entered was not found in the selected exchange. Please double check spelling and where the stock is registered")
        single_stock_financial_analysis(data)
        return

    # Make my life easier with seperate variables for columns 
    market_cap = company[2]
    high = company[3]
    low = company[4]

    # Columns 5-9 inclusive are rev 
    revenue = np.array(company[5:10])
    # Columns 10 - 14 inclusive are income
    income = np.array(company[10:15])

    expenses = revenue - income # Calculate Expenses
    profit_margin = (income / revenue) * 100 # Calculate profit margin

    # Create a handy dictionary for later
    rev_vs_income = {
        "Revenue": revenue,
        "Expenses": expenses,
        "Profit": income,
    }

    # Confirm user input
    print(f"You have selected {company[1]}\n")

    year = 2025 # Define year
    # Define labels for the x axis
    x_labels = [f"Q4 {year - 1}", f"Q1 {year}", f"Q2 {year}", f"Q3 {year}", f"Q4 {year}"]

    # Tell the user what is going on
    print("Drawing graph...")
    print("TIP: The graph looks a lot clearer when scaled up")

    width = 0.3 # define width for the columns 
    x = np.arange(len(revenue)) # create x axis values

    # Create a figure with two subplots and a shared x axis
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    fig.suptitle(f"{company[1]} Financial Analysis", fontsize=16)

    # Subplot 1 (Bars)
    index = 0
    for item, ls in rev_vs_income.items():
        offset = width * index
        rects = ax1.bar(x + offset - width, tuple(ls), width, label=item)
        ax1.bar_label(rects, padding=2, fmt='%.0f')
        index += 1

    # Dress up the plot with a title, labels and a legend
    ax1.set_ylabel("Value (USD)")
    ax1.set_title("Quarterly Financials")
    ax1.legend(loc='lower left', ncols=3)
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # Subplot 2 (Line)
    ax2.plot(x, profit_margin, label="Profit Margin (%)", color="red", marker='o')

    # Dress up the plot with a title, labels and a legend
    ax2.set_ylabel("Profit Margin (%)")    
    ax2.set_title("Quarterly Profit Margin")
    ax2.set_xticks(x, x_labels)
    ax2.legend(loc='upper right')
    ax2.grid(axis='y', linestyle='--', alpha=0.7)    

    # Stop labels from overlapping
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])

    # Save the plot to a file
    print("Saving plot to in final_plots")
    plt.savefig(f"final_plots/financial_analysis_{ticker}.png")

    # Show Plot
    plt.show()
    press_to_continue()

def compare_exchange_volitility(current_exchange, current_data, mapping):
    """
    Compares the volitility of 2 stocks ranked the same on different exchanges

    Args:
        current_exchange (string): Name of the previoulsy selected exchange
        current_data (list): The 2D list of every stock in the selected exchange
        mapping (dict): A dictionary for mapping the selected exchange to a name
    
    Returns: None
    """
    # Prompt user for another exchange
    print(f"Enter the exchange to compare to {current_exchange}")
    other_exchange = mapping[pick_exchange()]

    # Exit the program if asked
    if other_exchange == "EXIT":
        return
    # Loop around with an error message if the selection matches the current exchange
    elif other_exchange == current_exchange:
        print(f"\n- Please enter a different exchange than your original pick ({current_exchange})")
        compare_exchange_volitility(current_exchange, current_data, mapping)
        return

    # load the second exchange
    other_data = load_data(other_exchange)

    # Get the rank from the user and loop if invalid
    picked_rank = False
    rank = 0
    while picked_rank == False:
        rank = input("\nPlease enter the desired rank to compare (1-60)\n>> ")

        if dm.is_int(rank) == True:
            # Make sure the input is in the range
            if int(rank) <= 60 and int(rank) > 0:
                rank = int(rank)
                picked_rank = True
            else:
                print("Please input a valid integer between 0 and 60 \n(no letters or decimals)")
        else: 
            print("Please input a valid integer between 0 and 60 \n(no letters or decimals)")

    # make a list of the stocks and their data
    exchange_list = [current_exchange, other_exchange]
    data_list = [current_data, other_data]

    # Get the standard deviations and store them with their respective stock's data
    std_dev = []
    for i, data in enumerate(data_list):
        for row in data:
            if int(row[15]) == rank:
                ticker = row[0]
                name = row[1]
                high = row[3]
                low = row[4]
                std_dev.append([ticker, name, dm.get_standard_deviation([high, low])])


    # Determine the most and least volitile stocks
    std_dev[0].append(current_exchange)
    std_dev[1].append(other_exchange)
    winner = []
    if std_dev[0][2] > std_dev[1][2]:
        winner = std_dev[0]
        loser = std_dev[1]
    else:
        winner = std_dev[1]
        loser = std_dev[0]

    # print the chart headers
    print(f"\nExchange\tStock Ticker\tVolitility")
    
    # print the chart
    for stock in std_dev:
        print(f"{stock[3]}\t\t{stock[0]}\t\t±{stock[2]:.2f}%")

    # Print the summary of data
    print(f"\nThe most volitile stock ranked {rank} is {winner[1]} ({winner[0]}) with a standard deviation of ±{winner[2]:.2f}%")
    if winner[2] >= 30.0:
        print(f"It may not be a good idea to invest in {winner[1]} because it can fluctuate more than 30%")
        if loser[2] >= 30.0:
            print(f"Even though it is technically safer, {loser[1]} is also quite volatile")
        else:
            print(f"However, {loser[1]} looks to be much safer")
    else:
        print(f"Overall {winner[1]} is not very volatile\nEither stock is probably safe")

    press_to_continue()

    # Ask user to save as csv
    print("\nWould you like to save this result as a csv?")
    selected = False

    # Handle y/n logic and loop around if its not a y or n
    while selected == False:
        selection = input("(Enter y or n)\n>> ").upper()
        if selection == "Y":
            # write the csv
            selected = True
            volitility_csv(std_dev)
            print("Done!")
            press_to_continue()
        elif selection == "N":
            selected = True
        else:
            print("Please enter either y or n")
    
def volitility_csv(data):
    """
    Write a csv with the volitility assessment 

    Args:
        data (list): the 2D list to write 
    
    Returns: None
    """

    # Attatch headers to the list for the csv
    headers = ["Ticker", "Name", "Volitility", "Exchange"]
    output = []
    output.append(headers)

    tick = "" # create an empty string for filename tickers

    # add the data to the output
    for line in data:
        output.append(line)
        tick += line[0] + "_" # format tickers for the filename
    tickers = tick[:-1] # trim the trailing underscore

    # Write the csv with the tickers in the filename
    user_csv.write_csv(f"volitility_assessment_{tickers}.csv", output, True)

def most_profitable_next_quarter(data):
    """
    Determine which stock will be the most profitable next quarter

    Args:
        data (list): The 2D list of the selected exchange's data
    
    Returns: None
    """
    tickers_to_names = {} # create an indexing dictionary

    # Create a list of incomes for all stocks
    incomes = []
    for row in data:
        # make life easy with named variables
        ticker = row[0]
        name = row[1]

        # build the indexing dict
        tickers_to_names[ticker] = name

        # build the incomes list
        income = np.array(row[10:15])
        incomes.append([ticker, income])
    
    # Iterate through and get highest profit
    most_profitable = [0, 0, 0]
    for stock in incomes:
        aprox = dm.linear_aproximation(stock[1])
        if np.any(aprox > most_profitable[2]):
            most_profitable = [stock[0], stock[1], aprox]

    # Print most profitable 
    ticker = tickers_to_names[most_profitable[0]]
    print(f"\nThe most profitable sock next quarter will probably be {ticker} ({most_profitable[0]})")
    print(f"It will most likely earn ${most_profitable[2]} next quarter")

    press_to_continue()

def press_to_continue():
    """
    Creates a pause in text flow to separate menus. The user can press enter to continue the process
    
    Args: None

    Returns: None
    """
    dummy = input("\n<Press ENTER to continue>")

# nice translation layer for inputs
EXCHANGES = {
    1: "NASDAQ",
    2: "TSX",
    3: "XETR",
    0: "EXIT",
}


program_running = True
while program_running:
    # Enter the first menu
    print("\nWelcome to black_rock_python, a stock analysis software fit for a snake\n")
    
    # Picks the exchange and translate it to a name
    exchange = EXCHANGES[pick_exchange()]

    # Exit if exit is selected
    if exchange == "EXIT":
        break

    # Load the exchange data
    data = load_data(exchange)

    # Loop through the main menu and functions until the user exits
    exchange_chosen = True
    while exchange_chosen:
        choice = main_menu(exchange)
        if choice == "1":
            single_stock_financial_analysis(data)
        if choice == "2":
            compare_exchange_volitility(exchange, data, EXCHANGES)
        if choice == "3":
            most_profitable_next_quarter(data)
        if choice == "0":
            break
