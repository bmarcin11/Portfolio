"""
| Bryan Marcin
| ITN160-603
| Beach Side Restaurant
| 11/14/23
"""

from guizero import *
from csv import reader

# CSV file has two columns, the first for item name and the second for item price
csv_file = 'ITN160 - Marcin, Final Project Sample Menu.csv'


def main():
    """
    | Display a dynamic restaurant menu according to supplied file
    | User inputs the quantity desired of each item and program reads pricing changes
    :return:
    """
    def change_quantity(operation, i):
        """
        Adjusts the desired quantity of the aligned row
        :param operation: Designates change as positive or negative
        :param i: Designates row
        :return:
        """
        nonlocal subtotal
        # First, check operator
        if operation == '+':
            # Then, check current quantity
            # Disable the button used if this operation will reach maximum or minimum
            # Enable the opposite button if this operation will bring quantity off ceiling/floor
            # Regardless, adjust quantity
            if lst_quantity[i] == 0:
                lst_quantity[i] += 1
                lst_psh_minus[i].enabled = True
            elif lst_quantity[i] < 9:
                lst_quantity[i] += 1
            else:
                lst_quantity[i] += 1
                lst_psh_plus[i].enabled = False
        elif operation == '-':
            if lst_quantity[i] == 10:
                lst_quantity[i] += -1
                lst_psh_plus[i].enabled = True
            elif lst_quantity[i] > 1:
                lst_quantity[i] += -1
            else:
                lst_quantity[i] += -1
                lst_psh_minus[i].enabled = False
        # With quantity adjusted, refresh relevant displays and do math
        lst_txt_quantity[i].value = lst_quantity[i]
        lst_item_total[i] = lst_quantity[i] * menu[i][1]
        lst_txt_item_total[i].value = f' ${lst_item_total[i]:6,.2f}'
        subtotal = sum(lst_item_total)
        txt_subtotal.value = f' ${subtotal:6,.2f}'
        status_check()

    def status_check():
        """
        Determine appropriate status of main menu buttons and adjust accordingly
        :return:
        """
        # Check of any item has any quantity, and disable the ability to clear input if so
        psh_clear.enabled = False
        for each in lst_quantity:
            if each:
                psh_clear.enabled = True
        # check if subtotal has value, enable confirmation if it does.
        if subtotal:
            psh_confirm.enabled = True
        else:
            psh_confirm.enabled = False

    def total_order():
        """
        Display a listing of items ordered, total cost, and request final confirmation
        :return:
        """
        nonlocal subtotal
        # Display pre-baked window
        wnd_confirm.visible = True
        # Disable main menu buttons while working in the dependent window
        psh_clear.enabled = False
        psh_confirm.enabled = False
        lbx_wnd_order.clear()
        for i, each in enumerate(menu):
            # Disable the rest of the main menu quantity controls
            lst_psh_plus[i].enabled = False
            lst_psh_minus[i].enabled = False
            # populate the current order listing and total charge
            if lst_quantity[i]:
                lbx_wnd_order.append(f'{each[0]}')
                pricing = f'{lst_quantity[i]:2} x ${each[1]:5,.2f} = ${lst_item_total[i]:6.2f}'
                lbx_wnd_order.append(f'{pricing:>55}')
                lbx_wnd_order.append('')
        lbx_wnd_order.append(f'{"Total = $":>51}{subtotal:6,.2f}')

    def clear_order():
        """
        Clear all item selections
        :return:
        """
        nonlocal subtotal
        for i, quantity in enumerate(lst_quantity):
            # set values to 0 and refresh display
            lst_quantity[i] = 0
            lst_txt_quantity[i].value = lst_quantity[i]
            lst_item_total[i] = 0.0
            lst_txt_item_total[i].value = f' ${lst_item_total[i]:6,.2f}'
            subtotal = 0.00
            txt_subtotal.value = f' ${subtotal:6,.2f}'
            # enable and disable relevant controls
            lst_psh_plus[i].enabled = True
            lst_psh_minus[i].enabled = False
        psh_confirm.enabled = False
        psh_clear.enabled = False

    def confirm_and_complete():
        """
        Pass to payment interface and make ready for next customer
        :return:
        """
        # placeholder popup for payment interface
        app.info(title='The Beach Side Restaurant',
                 text=f'${subtotal:.2f} has been charged to your card. '
                      f'\nThank you, and please come again!')
        clear_order()

    def cancel_return():
        """
        Return to main menu in a nondestructive fashion and reactivate controls
        :return:
        """
        wnd_confirm.visible = False
        # check if quantities are at the ceiling and make appropriate button status changes
        for i, each in enumerate(lst_psh_plus):
            if lst_quantity[i] != 10:
                each.enabled = True
        for i, each in enumerate(lst_psh_minus):
            if lst_quantity[i] != 0:
                each.enabled = True
        status_check()

    # Populate a menu listing with the contents of a supplied CSV file
    menu = []
    try:
        with open(csv_file, 'r') as menu_file:
            menu_reader = reader(menu_file)
            for row in menu_reader:
                menu.append([row[0], float(row[1])])
    # In the event of a failure to read the CSV file,
    # Present an error box without presenting the empty menu, then close the program
    except FileNotFoundError:
        bad_app = App(visible=False)
        bad_app.error(title='File Not Found!',
                      text='Please run this program again with a menu file in the same folder.')
        bad_app.destroy()
        bad_app.display()
        exit(1)
    except IndexError:
        bad_app = App(visible=False)
        bad_app.error(title='File Error!',
                      text='Menu file is incomplete or improperly formatted.')
        bad_app.destroy()
        bad_app.display()
        exit(1)

    # size of window dynamically scales to size of menu
    app = App(title='The Beach Side Restaurant', width=750, height=120 + (len(menu) * 50), bg='wheat')
    app.text_size = 15

    # Upper box contains static elements such as title and column labels
    box_top = Box(app, width=750, height=70, align='top')
    box_title = Box(box_top, width=750, height=35, align='top')
    Text(box_title, text='Please place your order below', align='top')
    box_contents = Box(box_top, width=750, height=35, align='bottom')
    box_name_label = Box(box_contents, width=315, height=35, align='left')
    box_price_label = Box(box_contents, width=125, height=35, align='left')
    box_quantity_label = Box(box_contents, width=160, height=35, align='left')
    box_item_total_label = Box(box_contents, width=150, height=35, align='left')
    Text(box_name_label, text='Item', align='bottom')
    Text(box_price_label, text='Price', align='bottom')
    Text(box_quantity_label, text='Quantity', align='bottom')
    Text(box_item_total_label, text='Item Total', align='bottom')
    Box(app, width=750, height=1, align='top', border=1)

    # establish the lists that will give the expandable menu functionality
    lst_txt_name = []
    lst_txt_price = []
    lst_psh_minus = []
    lst_quantity = []
    lst_txt_quantity = []
    lst_psh_plus = []
    lst_item_total = []
    lst_txt_item_total = []
    # Create a box for each item, then populate it with a pre-structured item listing with quantity controls
    for index, item in enumerate(menu):
        box_item = Box(app, width=750, height=50, align='top')
        box_name = Box(box_item, width=315, height=50, align='left')
        box_price = Box(box_item, width=125, height=50, align='left')
        box_plus = Box(box_item, width=75, height=40, align='left')
        box_quantity = Box(box_item, width=45, height=50, align='left')
        box_minus = Box(box_item, width=75, height=40, enabled=False, align='left')
        box_item_total = Box(box_item, width=115, height=50, align='left')
        lst_txt_name.append(Text(box_name, text=item[0], align='right'))
        lst_txt_price.append(Text(box_price, text=f' :  ${item[1]:6,.2f}', align='left'))
        lst_psh_minus.append(PushButton(box_minus, text='-', command=change_quantity, args=['-', index], align='left'))
        lst_psh_minus[index].text_color = 'red'
        lst_quantity.append(0)
        lst_txt_quantity.append(Text(box_quantity, text=lst_quantity[index], align='left'))
        lst_psh_plus.append(PushButton(box_plus, text='+', command=change_quantity, args=['+', index], align='left'))
        lst_psh_plus[index].text_color = 'green'
        lst_item_total.append(0.00)
        lst_txt_item_total.append(Text(box_item_total, text=f' ${lst_item_total[index]:6,.2f}', align='left'))

    # Lower box contains running total and function buttons
    box_bottom = Box(app, width=750, height=50, align='bottom')
    box_confirm = Box(box_bottom, width=330, height=50, align='left')
    box_clear = Box(box_bottom, width=110, height=50, align='left')
    box_subtotal_label = Box(box_bottom, width=195, height=50, align='left')
    box_subtotal = Box(box_bottom, width=115, height=50, align='left')
    psh_confirm = PushButton(box_confirm, text='Order Done', align='right',
                             command=total_order, enabled=False)
    psh_clear = PushButton(box_clear, text='Clear Order', command=clear_order, align='left', enabled=False)
    subtotal = 0.00
    Text(box_subtotal_label, text='Subtotal :', align='right')
    txt_subtotal = Text(box_subtotal, text=f' ${subtotal:6,.2f}', align='left')

    # Confirm window, does not scale but contains a listing with a scrollbar for excessively sized orders
    wnd_confirm = Window(app, title='The Beach Side Restaurant', width=400, height=500, bg='wheat', visible=False)
    box_wnd_title = Box(wnd_confirm, width=400, height=35, align='top')
    lbx_wnd_order = ListBox(wnd_confirm, width=375, height=430, align='top', scrollbar=True)
    lbx_wnd_order.text_size = 14
    box_wnd_buttons = Box(wnd_confirm, width=400, height=35, align='bottom')
    box_wnd_confirm = Box(box_wnd_buttons, width=200, height=35, align='left')
    box_wnd_cancel = Box(box_wnd_buttons, width=2000, height=35, align='right')
    Text(box_wnd_title, text='Confirm Your Order', align='bottom')
    PushButton(box_wnd_confirm, text='Confirm Order', align='right', command=confirm_and_complete)
    PushButton(box_wnd_cancel, text='Cancel & Return', align='left', command=cancel_return)
    wnd_confirm.when_closed = cancel_return

    app.info(title='The Beach Side Restaurant',
             text='Welcome to the Beach Side Restaurant.\nMay we take your order?')

    app.display()


if __name__ == '__main__':
    main()
