"""
| Bryan Marcin
| ITN160-603
| Restaurant Menu Editor
| 10/25/23
"""

import copy
import pickle

# print the value of keys for oft handled exceptions.
exception_list = {'id_error': '\nSubmenu IDs and Item IDs are integer values only.',
                  'invalid_id': '\nSubmenu ID or Item ID not found.',
                  'binary_choice': '\nPlease input "y" for "yes" or "n" for "no".',
                  'menu_mishap': '\nInvalid menu selection, '
                                 'please enter the letter that corresponds to the desired action.',
                  'no_submenu': '\nNo submenu will be added to the main menu.',
                  'no_item': '\nNo item will be added to the submenu.',
                  'no_change': '\nNo changes made to menu.'}


def create_submenu(menu):
    """
    | uses the working main menu dictionary to add submenus
    | then returns a new working main menu dictionary
    :param menu:
    :return:
    """
    # New working menu is created so all changes can be reverted when returning
    test_menu = copy.deepcopy(menu)
    submenu_name = ''
    # Loop until the submenu has a valid name, or the user cancels the operation
    while not submenu_name:
        new_submenu_name = input('\nEnter new Submenu name, or press enter to return to the menu editor.'
                                 '\nNew submenu name: ')
        # Empty field flags canceled operation
        if not new_submenu_name:
            print(exception_list['no_submenu'])
            return menu
        else:
            # Create an iterable object of current submenu names to check new submenu name against
            submenu_listing = []
            for each in test_menu.values():
                submenu_listing.append(each[0])
            # Input is valid as long as it is unique
            if new_submenu_name not in submenu_listing:
                submenu_name = new_submenu_name
            else:
                print('\nSubmenu name must be unique.')
    # Loop until the submenu has a valid id, or the user cancels the operation
    submenu_id = 0
    while not submenu_id:
        # Validate input is an integer
        try:
            user_input = input(f'\nEnter an id for the "{submenu_name}" submenu.'
                               f'\nEnter "0" to cancel.\nYour choice: ')
            # Accept empty field as a flag for consistency with previous option
            if not user_input:
                print(exception_list['no_submenu'])
                return menu
            else:
                new_submenu_id = int(user_input)
                # Use "0" as a flag in order to prevent its use as an ID
                if new_submenu_id == 0:
                    print(exception_list['no_submenu'])
                    return menu
                else:
                    # Input is valid as long as it is an integer and unique
                    if new_submenu_id not in test_menu.keys():
                        submenu_id = new_submenu_id
                    else:
                        print('\nSubmenu ID already in use.')
        except ValueError:
            print(exception_list['id_error'])
    # Add the submenu id and name values to the working menu
    # An empty dictionary is placed in advance of edit_submenu()
    test_menu[submenu_id] = [submenu_name, {}]
    # Print the working menu before confirming the addition
    print('\nNew Menu:')
    for index, submenu in sorted(test_menu.items()):
        print(f'{index:2}: {submenu[0]}')
    confirm = ''
    while confirm not in ('y', 'n'):
        confirm = input('\nCreate submenu? (y or n)\nYour choice: ').lower()
        # if confirmed, the working menu becomes the value to be returned.
        if confirm == 'y':
            menu = copy.deepcopy(test_menu)
        # if it is not confirmed, the loop will complete
        # but the original menu dictionary will return, discarding changes
        elif confirm == 'n':
            print(exception_list['no_submenu'])
        else:
            print(exception_list['binary_choice'])
    return menu


def edit_submenu(submenu):
    """
    | Take the contents of a specific submenu as input
    | Create, edit or remove items from that menu
    | Return the edited submenu as output
    :param submenu:
    :return:
    """
    def add_item():
        """
        | Add an item to the selected submenu
        | similar to adding a submenu
        :return:
        """
        create_name = ''
        while not create_name:
            new_create_name = input('\nEnter new item name, or press enter to return to the submenu editor.'
                                    '\nNew item name: ')
            # Empty field flags canceled operation
            if not new_create_name:
                print(exception_list['no_item'])
                return
            else:
                # Create an iterable object of current item names to check new item name against
                submenu_items = []
                for each in sub_test_menu.values():
                    submenu_items.append(each[0])
                # Input is valid as long as it is unique
                if new_create_name not in submenu_items:
                    create_name = new_create_name
                else:
                    print('\nSubmenu name must be unique.')
        # Loop until the item has a valid price, or the user cancels the operation
        create_price = 0.0
        while not create_price:
            new_create_price = input('\nEnter the price for the item, or press enter to return to the submenu editor.'
                                     '\nNew item price: $')
            # Empty field flags canceled operation
            if not new_create_price:
                print(exception_list['no_item'])
                return
            else:
                # Validate that input is numeric
                try:
                    new_create_price = float(new_create_price)
                    # Validate that price is positive
                    if new_create_price < 0.0:
                        print('No negative prices.')
                    # Set the price
                    else:
                        create_price = new_create_price
                except ValueError:
                    print('Please enter the price in numeric dollars and cents.')
        # Loop until the item has a valid id, or the user cancels the operation
        create_id = 0
        while not create_id:
            # Validate input is an integer
            try:
                create_user_input = input(f'\nEnter an id for the "{create_name}" item.'
                                          f'\nEnter "0" to cancel.\nYour choice: ')
                # Accept empty field as a flag for consistency with previous option
                if not create_user_input:
                    print(exception_list['no_item'])
                    return
                else:
                    new_create_id = int(create_user_input)
                    # Use "0" as a flag in order to prevent its use as an ID
                    if new_create_id == 0:
                        print(exception_list['no_item'])
                        return
                    else:
                        # Input is valid as long as it is an integer and unique
                        if new_create_id not in sub_test_menu.keys():
                            create_id = new_create_id
                        else:
                            print('\nItem ID already in use.')
            except ValueError:
                print(exception_list['id_error'])
        # once confirmed, write changes to working submenu
        sub_test_menu[create_id] = [create_name, create_price]

    # create a working submenu so changes can be reverted
    sub_test_menu = copy.deepcopy(submenu)
    # confirm loop encapsulates editing function, similar to menu editing
    selection = ''
    while selection != 's':
        # if the submenu is not empty, normal editing can take place
        if sub_test_menu:
            # user inputs letters to make selection
            for index, menu_item in sorted(sub_test_menu.items()):
                print(f'{index:2}: {menu_item[0]:16} - ${menu_item[1]:5,.2f}')
            selection = input('\nc - Create a new item.\ne - Edit the properties of an item.'
                              '\nd - Delete an item.\ns - Save your changes.'
                              '\nPlease enter your choice: ').lower()
            # create new item
            if selection == 'c':
                add_item()
            # edit the properties of an existing item
            elif selection == 'e':
                # prompt user to choose an itemid
                item_id = 0
                while not item_id:
                    # Validate input is an integer
                    user_input = input(f'\nEnter an id for an item to edit.'
                                       f'\nEnter "0" to cancel.\nYour choice: ')
                    # Accept empty field as a flag for consistency with previous option
                    if not user_input:
                        print(exception_list['no_change'])
                    else:
                        try:
                            item_id = int(user_input)
                            # Use "0" as a flag in order to prevent its use as an ID
                            if item_id == 0:
                                print(exception_list['no_change'])
                            else:
                                # check if item exists in the menu before editing it
                                if item_id in sub_test_menu.keys():
                                    item_name = sub_test_menu[item_id][0]
                                    item_price = sub_test_menu[item_id][1]
                                    # loop works in reverse to normal operation to allow simple non-edits.
                                    new_name = 'foo'
                                    while new_name:
                                        new_name = input(f'\nEnter a new name for {item_name}. '
                                                         'Enter nothing to skip renaming'
                                                         '\nNew name: ')
                                        if not new_name:
                                            pass
                                        # item names cannot exceed the size of the display
                                        elif len(new_name) > 16:
                                            print('\nItem name too long.')
                                        else:
                                            item_name = new_name
                                            new_name = ''
                                    new_price = 'foo'
                                    while new_price:
                                        new_price = input(f'\nEnter a new price for {item_name}. '
                                                          'Enter nothing to skip repricing'
                                                          '\nNew price: $')
                                        if not new_price:
                                            pass
                                        else:
                                            try:
                                                # items prices cannot be lower than 0
                                                new_price = float(new_price)
                                                if new_price < 0:
                                                    print('\nNo negative prices.')
                                                else:
                                                    item_price = new_price
                                                    new_price = ''
                                            except ValueError:
                                                print('\nPlease enter the price in numeric dollars and cents.')
                                    # if confirmed, write the item to the working submenu
                                    confirm = ''
                                    while confirm not in ('y', 'n'):
                                        confirm = input(f'\n{item_id:2}: {item_name:16} - ${item_price:5,.2f}'
                                                        f'\n\nConfirm changes? (y or n)'
                                                        f'\nYour choice: ')
                                        if confirm == 'y':
                                            sub_test_menu[item_id] = [item_name, item_price]
                                        elif confirm == 'n':
                                            print(exception_list['no_change'])
                                        else:
                                            print(exception_list['binary_choice'])
                                else:
                                    print('\nItem ID not found.')
                        except ValueError:
                            print(exception_list['id_error'])
            # delete an item from the submenu
            elif selection == 'd':
                item_id = 0
                while not item_id:
                    # Validate input is an integer
                    user_input = input(f'\nEnter an id for an item to delete.'
                                       f'\nEnter "0" to cancel.\nYour choice: ')
                    # Accept empty field as a flag for consistency with previous option
                    if not user_input:
                        print(exception_list['no_change'])
                    else:
                        try:
                            item_id = int(user_input)
                            # Use "0" as a flag in order to prevent its use as an ID
                            if item_id == 0:
                                print(exception_list['no_change'])
                            else:
                                # check if item is in the submenu before deleting
                                if item_id in sub_test_menu.keys():
                                    confirm = ''
                                    item_name = sub_test_menu[item_id][0]
                                    item_price = sub_test_menu[item_id][1]
                                    # when confirmed, delete the item
                                    while confirm not in ('y', 'n'):
                                        confirm = input(f'\n{item_id:2}: {item_name:16} - ${item_price:5,.2f}'
                                                        f'\n\nConfirm deletion? (y or n)'
                                                        f'\nYour choice: ')
                                        if confirm == 'y':
                                            del sub_test_menu[item_id]
                                        elif confirm == 'n':
                                            print(exception_list['no_change'])
                                        else:
                                            print(exception_list['binary_choice'])
                                else:
                                    print('\nItem ID not found.')
                        except ValueError:
                            print(exception_list['id_error'])
            # save changes to submenu and exit the function
            elif selection == 's':
                save = ''
                # write the working submenu to submenu when confirmed
                while save not in ('y', 'n'):
                    save = input('\nDo you wish to save your changes? (y or n) ').lower()
                    if save == 'y':
                        submenu = copy.deepcopy(sub_test_menu)
                        print(f'\nChanges saved to current submenu.')
                    elif save == 'n':
                        print('\nChanges have not been saved.')
                    else:
                        print(exception_list['binary_choice'])
                # exit the program or keep editing
                confirm = ''
                while confirm not in ('y', 'n'):
                    confirm = input('\nDo you wish to continue editing the submenu? (y or n) \nYour choice: ').lower()
                    if confirm == 'n':
                        print('\nProgram will now close.')
                    elif confirm == 'y':
                        print('\nReturning to menu editing.')
                        selection = ''
                    else:
                        print(exception_list['binary_choice'])
            else:
                print(exception_list['menu_mishap'])
        # if submenu is empty, an item must be added before any other actions can be done
        else:
            confirm = ''
            while confirm not in ('y', 'n'):
                confirm = input('\nNo items exist in this submenu, create one now? (y or n)'
                                '\nYour choice: ').lower()
                if confirm == 'y':
                    add_item()
                elif confirm == 'n':
                    print(exception_list['no_item'])
                    selection = 's'
                else:
                    print(exception_list['binary_choice'])
    # return the saved menu
    return submenu


def delete_submenu(menu):
    """
    | Delete submenu entries from the supplied menu dictionary
    :param menu:
    :return:
    """
    def confirm_delete():
        """
        | Confirm and execute submenu deletion
        :return:
        """
        confirm = ''
        while confirm not in ('y', 'n'):
            confirm = input(f'\nAre you sure you wish to delete the {menu[submenu_id][0]} submenu? (y or n)'
                            f'\nYour choice: ').lower()
            if confirm == 'y':
                del menu[submenu_id]
            elif confirm == 'n':
                print(exception_list['no_change'])
            else:
                print(exception_list['binary_choice'])

    # Function will loop until a return statement is found
    while True:
        user_input = input('\nSelect a submenu to delete by entering the submenu ID.'
                           '\nEnter "0" to return to the menu editor.'
                           '\nSubmenu to delete: ').lower()
        # empty or "0" flags a canceled operation
        if not user_input:
            print(exception_list['no_change'])
            return menu
        else:
            try:
                submenu_id = int(user_input)
                if submenu_id == 0:
                    print(exception_list['no_change'])
                    return menu
                # check if id is in menu before proceeding
                elif submenu_id not in menu.keys():
                    print(exception_list['invalid_id'])
                else:
                    # if the menu is empty, delete with confirmation, but no warning
                    if not menu[submenu_id][1]:
                        confirm_delete()
                        return menu
                    # if the menu has contents, show the user the contents before confirming deletion
                    else:
                        print('\nSelected submenu has items saved to it.'
                              '\nDeleting the submenu will also delete these items.\n')
                        for index, menu_item in sorted(menu[submenu_id][1].items()):
                            print(f'{index:2}: {menu_item[0]:16} - ${menu_item[1]:5,.2f}')
                        confirm_delete()
                        return menu
            except ValueError:
                print(exception_list['id_error'])


def main():
    # binary file to be written
    menu_file = 'menu.pkl'
    print('Welcome to the menu editor.')
    # Read menu file (pkl) to master menu dictionary
    try:
        with open(menu_file, 'rb') as master_file:
            master_menu = pickle.load(master_file)
    # If no master menu file exists, create an empty dict
    except FileNotFoundError:
        print('\nMenu file not found, a new file will be created upon completion.')
        master_menu = {}
    # Confirm loop encompasses program operation
    confirm = ''
    while confirm != 'n':
        # If menu is empty, a submenu must be created before any other actions can take place
        if not master_menu:
            confirm = input('\nNo submenus exist, create one now? (y or n)'
                            '\nYour choice: ').lower()
            if confirm == 'y':
                master_menu = create_submenu(master_menu)
            # If user does not wish to add to the menu, program closes
            elif confirm == 'n':
                print('\nProgram will now close.')
            else:
                print(exception_list['binary_choice'])
        # Once the menu has at least once submenu, the user is presented all basic choices
        else:
            # display the submenus of the working menu
            print('\nMenu:')
            for index, submenu in sorted(master_menu.items()):
                print(f'{index:2}: {submenu[0]}')
            # user inputs a letter to flag options
            main_option = input('\nc - Create a new submenu.\ne - Edit the items of a submenu.'
                                '\nd - Delete a submenu.\ns - Save your changes.'
                                '\nPlease enter your choice: ').lower()
            # create new submenu
            if main_option == 'c':
                master_menu = create_submenu(master_menu)
            # edit existing submenu
            elif main_option == 'e':
                try:
                    # User selects the submenu they wish to edit before the function is called
                    submenu_id = int(input('\nEnter the ID of the submenu to edit: '))
                    # check if the submenu id exists in the menu
                    if submenu_id in master_menu.keys():
                        master_menu[submenu_id][1] = edit_submenu(master_menu[submenu_id][1])
                    else:
                        print(exception_list['invalid_id'])
                except ValueError:
                    print(exception_list['id_error'])
            # delete a submenu
            elif main_option == 'd':
                master_menu = delete_submenu(master_menu)
            # save changes
            elif main_option == 's':
                # loop to confirm writing menu to file
                save = ''
                while save not in ('y', 'n'):
                    save = input('\nDo you wish to save your changes? (y or n) ').lower()
                    if save == 'y':
                        with open(menu_file, 'wb') as new_master_file:
                            pickle.dump(master_menu, new_master_file)
                        print(f'\nChanges saved to file: "{menu_file}"')
                    elif save == 'n':
                        print('\nChanges have not been saved.')
                    else:
                        print(exception_list['binary_choice'])
                # loop to confirm program closure
                confirm = ''
                while confirm not in ('y', 'n'):
                    confirm = input('\nDo you wish to continue editing the menu? (y or n) \nYour choice: ').lower()
                    if confirm == 'n':
                        print('\nProgram will now close.')
                    elif confirm == 'y':
                        print('\nReturning to menu editing.')
                    else:
                        print(exception_list['binary_choice'])
            else:
                print(exception_list['menu_mishap'])


if __name__ == '__main__':
    main()
