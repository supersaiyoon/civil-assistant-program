# import modules
from datetime import datetime, date, timedelta
import sys
import time
import os

# third party modules
from colorama import Fore, Back, Style
from dateutil.relativedelta import relativedelta, MO, TH
import holidays


# app info
app_author = 'Brian Yoon'
app_name = 'The Civil Process Assistant'
app_version = 'Version 2.0.0'
app_copyright = f'Copyright (C) 2020 {app_author}'
app_info = [app_name, app_version, app_copyright]


# variables for calling colors
cyan_font = Fore.CYAN
green_font = Fore.GREEN
red_font = Fore.RED
yellow_font = Fore.YELLOW
reset_font = Style.RESET_ALL


# useful generic functions
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_title():
    clear()
    for info in app_info:
        print(info)
    print()
    print()


def press_enter():
    hide_cursor()
    input(f'\n{yellow_font}Press Enter to continue...{reset_font}')


# closing file messages
no_close_msg = '\n\t***DO NOT CLOSE THE FILE***'

close_msg = '\n\t***CLOSE THE FILE***'


# functions for showing/hiding cursor
if os.name == 'nt':
    import msvcrt
    import ctypes

    class _CursorInfo(ctypes.Structure):
        _fields_ = [("size", ctypes.c_int),
                    ("visible", ctypes.c_byte)]

def hide_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

def show_cursor():
    if os.name == 'nt':
        ci = _CursorInfo()
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
        ci.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
    elif os.name == 'posix':
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()


def format_date(user_date):
    return user_date.strftime('%m/%d/%Y')


def get_date(question):
    while True:
        print_title()
        show_cursor()
        user_date = input(question).strip()
        if user_date == '0':
            break
        try:
            user_date = datetime.strptime(user_date, "%m/%d/%y").date()
            break
        except ValueError:
            hide_cursor()
            print('\nInvalid date entered.')
            time.sleep(2)
    return user_date


class county_holidays(holidays.HolidayBase):
    def _populate(self, year):
        name = 'New Year\'s Day'
        self[date(year, 1, 1)] = name
        if date(year, 1, 1).weekday() == 5:
            self[date(year, 1, 1) - timedelta(days = 1)] = name + ' (Observed)'
        if date(year, 1, 1).weekday() == 6:
            self[date(year, 1, 1) + timedelta(days = 1)] = name + ' (Observed)'
        
        name = 'Martin Luther King Jr. Day'
        self[date(year, 1, 1) + relativedelta(weekday = MO(+3))] = name

        name = 'Lincoln\'s Birthday'
        self[date(year, 2, 12)] = name
        if date(year, 2, 12).weekday() == 5:
            self[date(year, 2, 12) - timedelta(days = 1)] = name + ' (Observed)'
        if date(year, 2, 12).weekday() == 6:
            self[date(year, 2, 12) + timedelta(days = 1)] = name + ' (Observed)'
        
        name = 'Washington\'s Birthday'
        self[date(year, 2, 1) + relativedelta(weekday = MO(+3))] = name
        
        name = 'Cesar Chavez Day'
        self[date(year, 3, 31)] = name
        if date(year, 3, 31).weekday() == 5:
            self[date(year, 3, 31) - timedelta(days = 1)] = name + ' (Observed)'
        if date(year, 3, 31).weekday() == 6:
            self[date(year, 3, 31) + timedelta(days = 1)] = name + ' (Observed)'
        
        name = 'Memorial Day'
        self[date(year, 5, 1) + relativedelta(day = 31, weekday = MO(-1))] = name
                
        name = 'Independence Day'
        self[date(year, 7, 4)] = name
        if date(year, 7, 4).weekday() == 5:
            self[date(year, 7, 4) - timedelta(days = 1)] = name + ' (Observed)'
        if date(year, 7, 4).weekday() == 6:
            self[date(year, 7, 4) + timedelta(days = 1)] = name + ' (Observed)'

        name = 'Labor Day'
        self[date(year, 9, 1) + relativedelta(weekday = MO)] = name

        name = 'Columbus Day'
        self[date(year, 10, 1) + relativedelta(weekday = MO(+2))] = name

        name = 'Veterans Day'
        self[date(year, 11, 11)] = name
        if date(year, 11, 11).weekday() == 5:
            self[date(year, 11, 11) - timedelta(days = 1)] = name + ' (Observed)'
        if date(year, 11, 11).weekday() == 6:
            self[date(year, 11, 11) + timedelta(days = 1)] = name + ' (Observed)'
        
        name = 'Thanksgiving Day'
        self[date(year, 11, 1) + relativedelta(weekday = TH(+4))] = name

        name = 'Day after Thanksgiving'
        self[date(year, 11, 1) + relativedelta(weekday = TH(+4)) + timedelta(days = 1)] = name

        name = 'Christmas Day'
        self[date(year, 12, 25)] = name
        if date(year, 12, 25).weekday() == 5:
            self[date(year, 12, 25) - timedelta(days = 1)] = name + ' (Observed)'
        if date(year, 12, 25).weekday() == 6:
            self[date(year, 12, 25) + timedelta(days = 1)] = name + ' (Observed)'

holidays_list = county_holidays()
holidays_list.observed = False


# important variables
today = date.today()
hundred_eighty_ago = format_date(today - timedelta(days = 180))
two_years_ago = format_date(today + relativedelta(years =- 2))


def get_answer(question):
    while True:
        print_title()
        print(question)
        print('\n\t[1] Yes    [2] No    [0] Quit to Main Menu\n')
        
        show_cursor()
        answer = input('> ').lower().strip()
        if answer in ['0', '1', '2']:
            break
        else:
            hide_cursor()
            print(f'\nThat\'s not a valid choice!')
            time.sleep(2)
    return answer


def check_hwft():
    answer = get_answer(f'Are we instructed to {cyan_font}hold writ full term{reset_font}? ')
    if answer == '0':
        answer = 'quit'
    elif answer == '2':
        answer = 'close'
    elif answer == '1':
        answer = get_answer(f'Did the {cyan_font}writ expire{reset_font}? ')
        if answer == '0':
            answer = 'quit'
        elif answer == '1':
            answer = 'close'
        elif answer == '2':
            answer = 'no close'
    return answer


def eoj_inquiry():
    while True:
        # eoj question 1
        answer = get_answer(f'Did we receive a {cyan_font}Memorandum of Garnishee (MOG){reset_font}?')
        if answer == '0':
            answer = 'quit'
            break
        elif answer == '1':
            mog_received = True
        elif answer == '2':
            mog_received = False
        
        if mog_received:
            answer = get_answer(f'Are we {cyan_font}expecting $$ per MOG{reset_font} (including joint accounts or exempt Social Security funds)?')
            if answer == '0':
                answer = 'quit'
                break
            elif answer == '1':
                expect_funds = True
            elif answer == '2':
                answer = check_hwft()
                break

            if expect_funds:
                while True:
                    print_title()
                    print(f'Are you inquiring about a {cyan_font}bank levy{reset_font} or a {cyan_font}third party levy{reset_font}?\n')
                    print('\t[1] Bank levy')
                    print('\t[2] Third party levy\n')
                    
                    show_cursor()
                    answer = input('> ').lower().strip()
                
                    if answer in ['0', '1', '2']:
                        break
                    else:
                        hide_cursor()
                        print(f'\n"{answer}" is not a valid choice!')
                        time.sleep(2)

                if answer == '0':
                    answer = 'quit'
                    break
                elif answer == '1':
                    answer = get_answer(f'Did we {cyan_font}receive and pay out all $${reset_font} stated on MOG?')
                    if answer == '0':
                        answer = 'quit'
                        break
                    if answer == '1':
                        answer = check_hwft()
                        break
        
        # eoj question 2
        answer = get_answer(f'Was the {cyan_font}writ issued before {two_years_ago}{reset_font}?')
        if answer == '0':
            answer = 'quit'
            break
        elif answer == '1':
            answer = 'close'
            break
        elif answer == '2':
            answer = 'no close'
            break
    return answer


def ewo_inquiry():
    while True:
        # ewo question 1
        answer = get_answer(f'Was any $$ posted {cyan_font}on or after {hundred_eighty_ago}{reset_font}?')
        if answer == '0':
            answer = 'quit'
            break
        elif answer == '1':
            answer = 'no close'
            break

        # ewo question 2
        er_menu = {
            '1': 'Employer\'s Return: Effective',
            '2': 'Employer\'s Return: Ineffective',
            '3': 'Employer\'s Return: Undetermined',
            '4': 'Employer\'s Correspondence: Leave of absence or intervening levy',
            '5': 'Employer\'s Correspondence: Employee terminated',
            '6': 'None of the above / None at all'
            }

        while True:
            print_title()
            
            print(f'What was the {cyan_font}most recent{reset_font} communication from the employer?\n')

            for item in er_menu:
                print(f'\t[{item}] {er_menu[item]}')
            
            show_cursor()
            answer = input('\n> ').lower().strip()
            if answer in ['0', '1', '2', '3', '4', '5', '6']:
                break
            else:
                hide_cursor()
                print(f'\n"{answer}" is not a valid choice!')
                time.sleep(2)

        if answer == '0':
            answer = 'quit'
            break
        if answer == '1':
            # no follow-up question. ask ewo question #3
            pass
        elif answer == '2':
            answer = check_hwft()
            break
        elif answer == '3':
            # no follow-up question. ask ewo question #3
            pass
        elif answer == '4':
            answer = get_answer(f'Did the {cyan_font}intervening levy{reset_font} / {cyan_font}employee\'s leave of absence{reset_font} start before {cyan_font}{two_years_ago}{reset_font}?')
            if answer == '0':
                answer = 'quit'
                break
            elif answer == '1':
                answer = 'close'
                break
            elif answer == '2':
                answer = 'no close'
                break
        elif answer == '5':
            answer = get_answer(f'Did the employee {cyan_font}terminate{reset_font} their employment {cyan_font}before {hundred_eighty_ago}{reset_font}?')
            if answer == '0':
                answer = 'quit'
                break
            elif answer == '1':
                answer = 'close'
                break
            elif answer == '2':
                answer = 'no close'
                break
        elif answer == '6':
            # no follow-up question. ask ewo question #3
            pass

        # ewo question 3
        answer = get_answer(f'Did we serve the EWO before {cyan_font}{hundred_eighty_ago}{reset_font}?')
        if answer == '0':
            answer = 'quit'
            break
        elif answer == '1':
            answer = 'close'
            break
        elif answer == '2':
            answer = 'no close'
            break
    return answer


def judgment_inquiry():
    answer = get_answer(f'Is the judgment for a {cyan_font}Criminal{reset_font} or {cyan_font}Family Law case{reset_font}? ')
    if answer == '0':
        answer = 'quit'
    elif answer == '1':
        answer = 'no close'
    elif answer == '2':
        answer = 'close'
    return answer


def is_ewo():
    return get_answer(f'Is the service type an {cyan_font}EWO{reset_font}? ')


def bk_inquiry():
    answer = is_ewo()
    if answer == '0':
        answer = 'quit'
    elif answer == '2':
        answer = 'no close'
    elif answer == '1':
        answer = get_answer(f'Did the {cyan_font}employer\'s stay expire{reset_font}? ')
        if answer == '0':
            answer = 'quit'
        elif answer == '1':
            answer = 'close'
        elif answer == '2':
            answer = 'no close'
    return answer


def can_i_close():
    while True:
        answer = get_answer(f'Is there an {cyan_font}open service{reset_font}?')
        if answer == '0':
            return
        elif answer == '1':
            answer = 'no close'
            break

        answer = get_answer(f'Is there a {cyan_font}pending Claim of Exemption{reset_font}?')
        if answer == '0':
            return
        elif answer == '1':
            answer = 'no close'
            break

        answer = get_answer(f'Is there {cyan_font}pending $$ in the File Ledger{reset_font}? Look for $$ held for bankruptcy too!')
        if answer == '0':
            return
        elif answer == '1':
            answer = 'no close'
            break
        
        answer = get_answer(f'Is the {cyan_font}levy released{reset_font}?')
        if answer == '0':
            return
        elif answer == '1':
            answer = check_hwft()
            break

        answer = get_answer(f'Is there a {cyan_font}pending bankruptcy{reset_font}?')
        if answer == '0':
            return
        elif answer == '1':
            answer = bk_inquiry()
            break
        
        answer = get_answer(f'Did the {cyan_font}judgment expire{reset_font}?')
        if answer == '0':
            return
        elif answer == '1':
            answer = judgment_inquiry()
            break
        
        answer = is_ewo()
        if answer == '0':
            return
        elif answer == '1':
            answer = ewo_inquiry()
            break
        elif answer == '2':
            answer = eoj_inquiry()
            break
    
    if answer == 'quit':
        return
    elif answer == 'close':
        print(close_msg)
    elif answer == 'no close':
        print(no_close_msg)
    press_enter()


def acceptable_services():
    #for day, name in county_holidays(years = 2020).items():
    #    print(day, name)

    start_date = get_date(f'When are the documents being submitted (mm/dd/yy)?: ')

    if start_date == '0':
        return

    # compute 'temporary restraining order' hearing date accepted today
    tro_deadline = start_date + timedelta(days = 15)

    while (tro_deadline in holidays_list) or (tro_deadline.weekday() == 5) or (tro_deadline.weekday() == 6):
        tro_deadline = tro_deadline + timedelta(days = 1)

    # compute 'plaintiff's claim & order (in county)' hearing date accepted today
    pco_in_deadline = start_date + timedelta(days = 25)

    while (pco_in_deadline in holidays_list) or (pco_in_deadline.weekday() == 5) or (pco_in_deadline.weekday() == 6):
        pco_in_deadline = pco_in_deadline + timedelta(days = 1)
    
    # compute 'plaintiff's claim & order (out of county)' hearing date accepted today
    pco_out_deadline = start_date + timedelta(days = 30)

    while (pco_out_deadline in holidays_list) or (pco_out_deadline.weekday() == 5) or (pco_out_deadline.weekday() == 6):
        pco_out_deadline = pco_out_deadline + timedelta(days = 1)

    # compute 'request for order' hearing date accepted today
    # rfo_deadline = start_date + timedelta(days = 10)
    rfo_deadline = start_date

    court_day = 0

    # change 23 -> 16 if we are mixing calendar days with court days
    while court_day < 23:
        rfo_deadline = rfo_deadline + timedelta(days = 1)
        while (rfo_deadline in holidays_list) or (rfo_deadline.weekday() == 5) or (rfo_deadline.weekday() == 6):
            rfo_deadline = rfo_deadline + timedelta(days = 1)
        court_day += 1

    # compute 'civil subpoena' hearing date accepted today
    sub_deadline = start_date + timedelta(days = 20)

    while (sub_deadline in holidays_list) or (sub_deadline.weekday() == 5) or (sub_deadline.weekday() == 6):
        sub_deadline = sub_deadline + timedelta(days = 1)

    service_dict = {
        'Temporary Restraining Order': tro_deadline,
        'Plaintiff\'s Claim & Order (in county)': pco_in_deadline,
        'Plaintiff\'s Claim & Order (out of county)': pco_out_deadline,
        'Request for Order': rfo_deadline,
        'Subpoena (Civil)': sub_deadline
    }

    title_column_one = 'Document Type'
    title_column_two = 'Hearing Date'
    
    # table automatically adjusts column width
    column_one_width = len(title_column_one)
    column_two_width = len(title_column_two)

    for key in service_dict:
        if len(key) > column_one_width:
            column_one_width = len(key)

    if len(format_date(start_date)) > column_two_width:
        column_two_width = len(format_date(start_date))

    # final column width
    column_one_width += 4
    column_two_width += 4

    horizontal_line = '+' + ('-' * column_one_width) + '+' + ('-' * column_two_width) + '+'

    print_title()
    print(f'{green_font}Hearing Dates accepted as of {format_date(start_date)}{reset_font}:')
    print(horizontal_line)
    print(f'|{cyan_font}{title_column_one.center(column_one_width)}{reset_font}|{cyan_font}{title_column_two.center(column_two_width)}{reset_font}|')
    print(horizontal_line)

    
    for service in service_dict:
        deadline = format_date(service_dict[service])
        print(f'|  {green_font}{service.ljust(column_one_width - 2)}{reset_font}|{deadline.center(column_two_width)}|')
        print(horizontal_line)
    
    press_enter()


def compute_lien_period():
    while True:
        print_title()

        answer = get_answer(f'Are you calculating for an {cyan_font}attachment lien{reset_font}?')
        if answer == '0':
            return
        elif answer == '1':
            lien_duration = 3
        elif answer == '2':
            lien_duration = 2

        writ_issued = get_date(f'Enter {cyan_font}writ issued{reset_font} date (mm/dd/yy): ')
        if writ_issued == '0':
            return
        
        bk_filing = get_date(f'Enter {cyan_font}bankruptcy filing{reset_font} date (mm/dd/yy): ')
        if bk_filing == '0':
            return
        
        # if bk was filed before writ was issued, check if we served levy during automatic stay
        if bk_filing <= writ_issued:
            print(f'\n\t{red_font}WARNING!{reset_font} The debtor filed for bankruptcy before the writ was issued. Verify that we did not serve the levy during the automatic stay.')
            press_enter()

            answer = get_answer(f'Was the levy {cyan_font}served during the automatic stay{reset_font}?')
            if answer == '0':
                return
            elif answer == '1':
                print('\n\tRefer to the bankruptcy training manual on how to proceed from here.')
                press_enter()
                return

        # this loop ensures that the bk disposition date is AFTER the bk filing date
        while True:
            show_cursor()
            bk_disp = get_date(f'Enter {cyan_font}bankruptcy disposition{reset_font} date (mm/dd/yy): ')
            if bk_disp == '0':
                return

            if bk_disp < bk_filing:
                hide_cursor()
                print('\nBankruptcy disposition cannot occur before bankrupty was filed.')
                time.sleep(2)
            else:
                break
        print()

        if bk_disp < writ_issued:
            print('\tThere is no need to include any bankruptcies that ended before the writ was issued.')
            press_enter()
            return

        norm_lien_exp = writ_issued + relativedelta(years =+ lien_duration)

        if bk_filing <= writ_issued:
            days_in_bk = (bk_disp - writ_issued).days
        else:
            days_in_bk = (bk_disp - bk_filing).days

        # add more days to days_in_bk if there are multiple BKs
        while True:
            answer = get_answer(f'Do you have {cyan_font}another bankruptcy outcome{reset_font} that occurred {cyan_font}after{reset_font} the previous bankruptcy outcome (This is more common with complex levies)?')
            if answer == '0':
                return
            elif answer == '2':
                break
            
            while True:
                show_cursor()
                bk_filing = get_date(f'Enter {cyan_font}bankruptcy filing{reset_font} date (mm/dd/yy): ')
                if bk_filing == '0':
                    return
                
                if bk_filing < bk_disp:
                    hide_cursor()
                    print('\nNew bankruptcy filing cannot occur before the previous bankruptcy outcome.')
                    time.sleep(2)
                else:
                    break

            # need to check if lien expired before new BK filing
            actual_lien_exp = norm_lien_exp + timedelta(days = (days_in_bk + 1))
            if bk_filing >= actual_lien_exp:
                print(f'\n\tThe levy lien period already {cyan_font}expired on {format_date(actual_lien_exp)}{reset_font}.')
                print('\tThere is no need to calculate any more bankruptcy stays.')
                press_enter()
                return

            # this is repeated code from above. make this a function?
            while True:
                show_cursor()
                bk_disp = get_date(f'Enter {cyan_font}bankruptcy disposition{reset_font} date (mm/dd/yy): ')
                if bk_disp == '0':
                    return

                if bk_disp < bk_filing:
                    hide_cursor()
                    print('\nBankruptcy disposition cannot occur before bankrupty was filed.')
                    time.sleep(2)
                else:
                    break
            print()

            days_in_bk += (bk_disp - bk_filing).days
        break
    
    print_title()
    print(f'{days_in_bk} days spent in automatic stay. Therefore...\n')
    actual_lien_exp = norm_lien_exp + timedelta(days = (days_in_bk + 1))

    if actual_lien_exp <= today:
        print(f'\tLevy lien period {red_font}EXPIRED on {format_date(actual_lien_exp)}{reset_font}.')
    else:
        print(f'\tLevy lien period {cyan_font}expires on {format_date(actual_lien_exp)}{reset_font}.')
    press_enter()


def compute_employer_stay():
    timestamp = get_date(f'Enter {cyan_font}Sheriff timestamp{reset_font} date (mm/dd/yy): ')

    if timestamp == '0':
        return

    stay_date = timestamp + timedelta(days = 180)
    print(f'\n\tEmployer is to stay the wage garnishment until {cyan_font}{format_date(stay_date)}{reset_font}.')
    press_enter()


menu_items = {
    '1': f'{cyan_font}Bankruptcy:{reset_font} Until when is the employer to stay the wage garnishment?',
    '2': f'{cyan_font}Bankruptcy:{reset_font} Did the levy lien period expire?',
    '3': f'{cyan_font}Miscellaneous:{reset_font} Can I close this file?',
    '4': f'{cyan_font}Services:{reset_font} What Hearing Dates are we accepting?',
    '0': 'QUIT'
    }


def main_menu():
    while True:
        print_title()

        width = os.get_terminal_size().columns
        print('--={ MAIN MENU }=--'.center(width))

        print('\nSelect a menu option:\n')

        for item in menu_items:
            print(f'\t[{item}] {menu_items[item]}')
        
        show_cursor()
        menu_choice = input('\n> ').lower().strip()

        if menu_choice == '0':
            break
        elif menu_choice == '1':
            compute_employer_stay()
        elif menu_choice == '2':
            compute_lien_period()
        elif menu_choice == '3':
            can_i_close()
        elif menu_choice == '4':
            acceptable_services()
        else:
            hide_cursor()
            print(f'\n"{menu_choice}" is not a valid choice!')
            time.sleep(2)
            continue
        print_title()
        hide_cursor()
        print('Returning to the main menu...')
        time.sleep(2)


def main():
    main_menu()
    print(f'\n{app_name} terminated. Goodbye.')
    time.sleep(2)
    sys.exit()


if __name__ == '__main__':
    main()
