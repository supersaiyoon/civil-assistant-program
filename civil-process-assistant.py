# import modules
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from sys import exit
import os


# app info
app_author = 'Brian Yoon'
app_name = 'The Civil Process Assistant'
app_version = 'Version 2.0'
app_copyright = f'Copyright (C) 2020 {app_author}'

app_info = [app_name, app_version, app_copyright]


# possible user responses
yes_list = ['yes', 'y', 'si', 'yeah', 'yup', 'yep', 'oui', 'ja']
no_list = ['no', 'n', 'nah', 'nope', 'non', 'nein']
quit_list = ['q', 'quit', 'exit']
er_menu = ['1', '2', '3', '4', '5', '6']
eoj_menu = ['1', '2']


# useful generic functions
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def press_enter():
    input('Press Enter to continue...')


# closing file messages
def no_close_msg():
    print('\n\t***DO NOT CLOSE THE FILE***')


def close_msg():
    print('\n\t***CLOSE THE FILE***')


# manipulating datetime objects
def format_date(user_date):
    return user_date.strftime('%m/%d/%Y')


def get_date(question):
    while True:
        user_date = input(question).strip()
        try:
            user_date = datetime.strptime(user_date, "%m/%d/%y").date()
            break
        except ValueError:
            print('Invalid date entered.', end = ' ')
    return user_date


# important variables
today = date.today()
hundred_eighty_ago = format_date(today + relativedelta(days =- 180))
two_years_ago = format_date(today + relativedelta(years =- 2))


def get_answer(question):
    while True:
        answer = input(question).lower().strip()

        if answer in yes_list:
            answer = 'y'
            break
        if answer in no_list:
            answer = 'n'
            break
        if answer in quit_list:
            answer = 'q'
            break
        else:
            print('Invalid entry. Only enter "Y" or "N"\n')
    return answer


def yes(answer):
    answer = answer.lower().strip()

    while (answer not in yes_list) and (answer not in no_list):
        answer = input('Invalid entry. Only enter "Y" or "N": ').lower().strip()
  
    if answer in yes_list:
        return True
    else:
        return False


def check_hwft():
    if not yes(answer = input('Are we instructed to hold writ full term (Y/N)? ')):
        close_msg()
        return

    if not yes(answer = input('Did the writ expire (Y/N)? ')):
        no_close_msg()
    else:
        close_msg()


def eoj_inquiry():
    if yes(answer = input('Did we receive a Memorandum of Garnishee (MOG) [Y/N]? ')):
        if yes(answer = input('Are we expecting $$ per MOG (including joint accounts or exempt Social Security funds) (Y/N)? ')):
            print()
            print('Are you inquiring about a bank levy or a third party levy?')
            print()
            print('  (1) Bank levy')
            print('  (2) Third party levy')
            print()

            while (answer := input('Service type: ')) not in eoj_menu:
                print('Invalid entry. Enter "1" for Bank Levy or "2" for Third Party Levy.', end = ' ')

            if answer == '1':                
                if yes(answer = input('Did we receive and pay out all $$ stated on MOG (Y/N)? ')):
                    check_hwft()
                    return
                else:
                    pass
            elif answer == '2':
                pass
        else:
            check_hwft()
            return

    if yes(answer = input(f'Was the writ issued before {two_years_ago} (Y/N)? ')):
        close_msg()
    else:
        no_close_msg()


def ewo_inquiry():
    # ewo question 1
    if yes(answer = input(f'Was any $$ posted on or after {hundred_eighty_ago} (Y/N)? ')):
        no_close_msg()
        return

    # ewo question 2
    if yes(answer = input('Did we receive a response or any correspondence from the employer (Y/N)? ')):
        print()
        print('What was the MOST RECENT communication we received from the employer?')
        print()
        print('  (1) Employer\'s Return: Effective')
        print('  (2) Employer\'s Return: Ineffective')
        print('  (3) Employer\'s Return: Undetermined')
        print('  (4) Employer\'s Correspondence: Leave of absence or intervening levy')
        print('  (5) Employer\'s Correspondence: Employee terminated')
        print('  (6) None of the above')
        print()

        while (answer := input('Employer\'s response type: ')) not in er_menu:
            print('Invalid entry. Only enter a number between 1-6.', end = ' ')

        if answer == '1':
            pass
        elif answer == '2':
            check_hwft()
            return
        elif answer == '3':
            pass
        elif answer == '4':
            if yes(answer = input(f'Did the intervening levy or employee\'s leave of absence start before {two_years_ago} (Y/N)? ')):
                close_msg()
                return
            else:
                no_close_msg()
                return
        elif answer == '5':
            if yes(answer = input(f'Did the employee terminate their employment before {hundred_eighty_ago} (Y/N)? ')):
                close_msg()
            else:
                no_close_msg()
            return
        elif answer == '6':
            pass

    # ewo question 3
    answer = input(f'Did we serve the EWO before {hundred_eighty_ago} (Y/N)? ')
    if yes(answer):
        close_msg()
    else:
        no_close_msg()


def judgment_inquiry():
    if yes(answer = input('Is the judgment for a Criminal or Family Law case (Y/N)? ')):
        no_close_msg()
    else:
        close_msg()
    return


def is_ewo():
    answer = input('Is the service type an EWO (Y/N)? ')
    if yes(answer):
        return True


def bk_inquiry():
    if not is_ewo():
        no_close_msg()
        return

    if yes(answer = input('Did the employer\'s stay expire (Y/N)? ')):
        close_msg()
    else:
        no_close_msg()
    return


def can_i_close():
    print()
    print('Before starting, check the file for any of the following:')
    print()
    print('  1. Open service')
    print('  2. Pending Claim of Exemption')
    print('  3. $$ pending shown in the File Ledger (Look for $$ held for bankruptcy too!)')
    print()
    print('If any of the above applies to your file, STOP. Do not close the file.')
    print('If there are multiple services in the file, run this program for each service.')
    print()

    if not yes(answer = input('Do you want to continue (Y/N)? ')):
        return

    if yes(answer = input('Is the levy released (Y/N)? ')):
        check_hwft()
        return
    if yes(answer = input('Is there a pending bankruptcy (Y/N)? ')):
        bk_inquiry()
        return
    if yes(answer = input('Did the judgment expire (Y/N)? ')):
        judgment_inquiry()
        return
    if is_ewo():
        ewo_inquiry()
        return
    else:
        eoj_inquiry()
        return


# functions for computing dates
def compute_lien_period():
    print_title()
    
    lien_duration = 2
    print('\nCalculating lien period expiration date...\n')

    if yes(answer = input('Are you calculating for an attachment lien (Y/N)? ')):
        lien_duration = 3

    print(f'\nI need a few important dates...\n')

    writ_issued = get_date('Enter writ issued date (mm/dd/yy): ')
    bk_filing = get_date('Enter bankruptcy filing date (mm/dd/yy): ')

    if bk_filing <= writ_issued:
        print('\n\tWARNING! The debtor filed for bankruptcy before the writ was issued.')
        print('\tVerify that we did not serve the levy during the automatic stay.\n')

        if yes(answer = input('Was the levy served during the automatic stay (Y/N)? ')):
            print()
            print('    Refer to the bankruptcy training manual on how to proceed from here.')
            return

    # this loop ensures that the bk disposition date is AFTER the bk filing date
    while (bk_disp := get_date('Enter bankruptcy disposition date (mm/dd/yy): ')) < bk_filing:
        print('\nBankruptcy disposition cannot occur before bankrupty was filed.')
    print()

    if bk_disp < writ_issued:
        print('  There is no need to include any bankruptcies that ended before the writ was issued.')
        return

    norm_lien_exp = writ_issued + relativedelta(years =+ lien_duration)

    if bk_filing <= writ_issued:
        days_in_bk = (bk_disp - writ_issued).days
    else:
        days_in_bk = (bk_disp - bk_filing).days

    # add more days to days_in_bk if there are multiple BKs
    while True:
        answer = input('Do you have another bankruptcy outcome that occurred after the previous bankruptcy outcome (This is more common with complex levies) [Y/N]? ')
        print()
        if not yes(answer):
            break

        while (bk_filing := get_date('Enter bankruptcy filing date (mm/dd/yy): ')) < bk_disp:
            print()
            print('New bankruptcy filing cannot occur before the previous bankruptcy outcome.')

        # need to check if lien expired before new BK filing
        actual_lien_exp = norm_lien_exp + relativedelta(days =+ (days_in_bk + 1))
        if bk_filing >= actual_lien_exp:
            print()
            print(f'    The levy lien period already expired on {format_date(actual_lien_exp)}.')
            print('    There is no need to calculate any more bankruptcy stays.')
            return

        # this is repeated code from above. make this a function?
        while (bk_disp := get_date('Enter bankruptcy disposition date (mm/dd/yy): ')) < bk_filing:
            print()
            print('Bankruptcy disposition cannot occur before bankrupty was filed.')
        print()

        days_in_bk += (bk_disp - bk_filing).days

    print(f'{days_in_bk} days spent in automatic stay. Therefore...')
    print()
    actual_lien_exp = norm_lien_exp + relativedelta(days =+ (days_in_bk + 1))

    if actual_lien_exp <= today:
        print(f'  Levy lien period EXPIRED on {format_date(actual_lien_exp)}.')
    else:
        print(f'  Levy lien period expires on {format_date(actual_lien_exp)}.')


def compute_employer_stay():
    #calculate 180 days from sheriff timestamp
    print_title()
    
    print('\nCalculating employer stay expiration date...\n')

    timestamp = get_date('Enter Sheriff timestamp date (mm/dd/yy): ')

    stay_date = timestamp + relativedelta(days =+ 180)
    print(f'\n\tEmployer is to stay the wage garnishment until {format_date(stay_date)}.')


menu_items = {
    1: 'Bankruptcy: Calculate EWO stay expiration date for employer',
    2: 'Bankruptcy: Calculate levy lien period expiration date',
    3: 'Can I close this file?',
    'Q': 'QUIT'
    }


def print_title():
    for info in app_info:
        print(info)


def main_menu():
    while True:
        print_title()

        width = os.get_terminal_size().columns
        print('--={ MAIN MENU }=--'.center(width))

        print('\nSelect a menu option:\n')

        for item in menu_items:
            print(f'\t({item}) {menu_items[item]}')
        print()
        
        menu_choice = input('Menu option: ').lower().strip()

        if menu_choice == 'q':
            break
        
        if menu_choice == '1':
            clear()
            compute_employer_stay()
        elif menu_choice == '2':
            clear()
            compute_lien_period()
        elif menu_choice == '3':
            clear()
            can_i_close()
        else:
            print(f'Menu option "{menu_choice}" does not exist.')
        print()
        press_enter()
        clear()


def main():
    main_menu()
    print(app_name, 'terminated. Goodbye.')
    exit()


if __name__ == '__main__':
    main()
