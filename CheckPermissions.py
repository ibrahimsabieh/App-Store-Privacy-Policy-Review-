import pandas as pd
import pyperclip

# Set display options to show all columns
pd.set_option('display.max_columns', None)

def update_table(input_list):
    # Define the columns
    columns = ['CalendarRead', 'CalendarWrite', 'ContactsRead', 'ContactsWrite', 'Bluetooth', 'Calendar', 'Camera',
               'Contacts', 'Location', 'Microphone', 'Motion']
    # Initialize the table with False values
    table = pd.DataFrame(columns=columns, index=[0])
    table[:] = "FALSE"

    # Check and update the table based on the input list
    for item in input_list:
        if 'Calendar' in item or 'Calendars' in item:
            table['CalendarRead'] = table['CalendarWrite'] = table['Calendar'] = "TRUE"
        if 'Camera' in item:
            table['Camera'] = "TRUE"
        if 'Contact' in item or 'Contacts' in item:
            table['ContactsRead'] = table['ContactsWrite'] = table['Contacts'] = "TRUE"
        if 'Location' in item:
            table['Location'] = "TRUE"
        if 'Microphone' in item:
            table['Microphone'] = "TRUE"
        if 'Motion' in item:
            table['Motion'] = "TRUE"
        if 'Bluetooth' in item:
            table['Bluetooth'] = "TRUE"

    return table


if __name__ == "__main__":

    while True:
        user_input = input("")

        # Convert the input string to a list
        input_list = user_input.strip("[] ").split(', ')
        input_list = [item.strip("'\"") for item in input_list]

        result_table = update_table(input_list)

        listout = (list(result_table.loc[0]))

        print(' '.join([str(elem) for elem in listout]))
        pyperclip.copy(' '.join([str(elem) for elem in listout]))


