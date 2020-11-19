# import modules
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from sys import exit
import os


# app info
app_author = 'Brian Yoon'
app_name = 'The Civil Process Assistant'
app_version = 'Version 2.0'
app_copyright = f'Copyright (C) 2020 {app_author}'

app_info = [app_name, app_version, app_copyright]


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
    input('\nPress Enter to continue...')


# closing file messages
no_close_msg = '\n\t***DO NOT CLOSE THE FILE***'

close_msg = '\n\t***CLOSE THE FILE***'


# manipulating datetime objects
def format_date(user_date):
    return user_date.strftime('%m/%d/%Y')


def get_date(question):
    while True:
        print_title()
        user_date = input(question).strip()
        if user_date == '0':
            break
        try:
            user_date = datetime.strptime(user_date, "%m/%d/%y").date()
            break
        except ValueError:
            input('\nInvalid date entered. Press Enter to continue...')
    return user_date


# important variables
today = date.today()
hundred_eighty_ago = format_date(today + relativedelta(days =- 180))
two_years_ago = format_date(today + relativedelta(years =- 2))


def get_answer(question):
    while True:
        print_title()
        print(question)
        print('\n\t[1] Yes    [2] No    [0] Quit to Main Menu\n')
        
        answer = input('> ').lower().strip()
        if answer in ['0', '1', '2']:
            break
        else:
            print(f'\nThat\'s not a valid choice!')
            press_enter()
    return answer


def check_hwft():
    answer = get_answer('Are we instructed to hold writ full term? ')
    if answer == '0':
        answer = 'quit'
    elif answer == '2':
        answer = 'close'
    elif answer == '1':
        answer = get_answer('Did the writ expire? ')
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
        answer = get_answer('Did we receive a Memorandum of Garnishee (MOG)?')
        if answer == '0':
            answer = 'quit'
            break
        elif answer == '1':
            mog_received = True
        elif answer == '2':
            mog_received = False
        
        if mog_received:
            answer = get_answer('Are we expecting $$ per MOG (including joint accounts or exempt Social Security funds)?')
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
                    print('Are you inquiring about a bank levy or a third party levy?\n')
                    print('\t[1] Bank levy')
                    print('\t[2] Third party levy\n')
                    
                    answer = input('> ').lower().strip()
                
                    if answer in ['0', '1', '2']:
                        break
                    else:
                        print(f'That\'s not a valid choice!\n')

                if answer == '0':
                    answer = 'quit'
                    break
                elif answer == '1':
                    answer = get_answer('Did we receive and pay out all $$ stated on MOG?')
                    if answer == '0':
                        answer = 'quit'
                        break
                    if answer == '1':
                        answer = check_hwft()
                        break
        
        # eoj question 2
        answer = get_answer(f'Was the writ issued before {two_years_ago}?')
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
        answer = get_answer(f'Was any $$ posted on or after {hundred_eighty_ago}?')
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
            
            print('What was the MOST RECENT communication from the employer?\n')

            for item in er_menu:
                print(f'\t[{item}] {er_menu[item]}')
            
            answer = input('\n> ').lower().strip()
            if answer in ['0', '1', '2', '3', '4', '5', '6']:
                break
            else:
                print(f'That\'s not a valid choice!\n')
                press_enter()

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
            answer = get_answer(f'Did the intervening levy or employee\'s leave of absence start before {two_years_ago}?')
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
            answer = get_answer(f'Did the employee terminate their employment before {hundred_eighty_ago}?')
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
        answer = get_answer(f'Did we serve the EWO before {hundred_eighty_ago}?')
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
    answer = get_answer('Is the judgment for a Criminal or Family Law case? ')
    if answer == '0':
        answer = 'quit'
    elif answer == '1':
        answer = 'no close'
    elif answer == '2':
        answer = 'close'
    return answer


def is_ewo():
    return get_answer('Is the service type an EWO? ')


def bk_inquiry():
    answer = is_ewo()
    if answer == '0':
        answer = 'quit'
    elif answer == '2':
        answer = 'no close'
    elif answer == '1':
        answer = get_answer('Did the employer\'s stay expire? ')
        if answer == '0':
            answer = 'quit'
        elif answer == '1':
            answer = 'close'
        elif answer == '2':
            answer = 'no close'
    return answer


def can_i_close():
    while True:
        print('\nBefore starting, check the file for any of the following:\n')
        print('\t1. Open service')
        print('\t2. Pending Claim of Exemption')
        print('\t3. $$ pending shown in the File Ledger (Look for $$ held for bankruptcy too!)\n')
        print('If any of the above applies to your file, STOP. Do not close the file.')
        print('If there are multiple services in the file, run this program for each service.\n')

        # get_answer function below is clearing the above string. maybe change the above string into a y/n question instead?
        answer = get_answer('Do you want to continue?')
        if (answer == '0') or (answer == '2'):
            return
        
        answer = get_answer('Is the levy released?')
        if answer == '0':
            return
        elif answer == '1':
            answer = check_hwft()
            break

        answer = get_answer('Is there a pending bankruptcy?')
        if answer == '0':
            return
        elif answer == '1':
            answer = bk_inquiry()
            break
        
        answer = get_answer('Did the judgment expire?')
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


def compute_lien_period():
    while True:
        print_title()

        answer = get_answer('Are you calculating for an attachment lien?')
        if answer == '0':
            return
        elif answer == '1':
            lien_duration = 3
        elif answer == '2':
            lien_duration = 2

        writ_issued = get_date('Enter writ issued date (mm/dd/yy): ')
        if writ_issued == '0':
            return
        
        bk_filing = get_date('Enter bankruptcy filing date (mm/dd/yy): ')
        if bk_filing == '0':
            return
        
        # if bk was filed before writ was issued, check if we served levy during automatic stay
        if bk_filing <= writ_issued:
            print('\n\tWARNING! The debtor filed for bankruptcy before the writ was issued. Verify that we did not serve the levy during the automatic stay.')
            press_enter()

            answer = get_answer('Was the levy served during the automatic stay?')
            if answer == '0':
                return
            elif answer == '1':
                print('\n\tRefer to the bankruptcy training manual on how to proceed from here.')
                return

        # this loop ensures that the bk disposition date is AFTER the bk filing date
        while True:
            bk_disp = get_date('Enter bankruptcy disposition date (mm/dd/yy): ')
            if bk_disp == '0':
                return

            if bk_disp < bk_filing:
                print('\nBankruptcy disposition cannot occur before bankrupty was filed.')
                press_enter()
            else:
                break
        print()

        if bk_disp < writ_issued:
            print('\tThere is no need to include any bankruptcies that ended before the writ was issued.')
            press_enter()

        norm_lien_exp = writ_issued + relativedelta(years =+ lien_duration)

        if bk_filing <= writ_issued:
            days_in_bk = (bk_disp - writ_issued).days
        else:
            days_in_bk = (bk_disp - bk_filing).days

        # add more days to days_in_bk if there are multiple BKs
        while True:
            answer = get_answer('Do you have another bankruptcy outcome that occurred after the previous bankruptcy outcome (This is more common with complex levies)?')

            if answer == '0':
                return
            elif answer == '2':
                break
            
            while True:
                bk_filing = get_date('Enter bankruptcy filing date (mm/dd/yy): ')
                if bk_filing == '0':
                    return
                
                if bk_filing < bk_disp:
                    print('\nNew bankruptcy filing cannot occur before the previous bankruptcy outcome.')
                    press_enter()
                else:
                    break

            # need to check if lien expired before new BK filing
            actual_lien_exp = norm_lien_exp + relativedelta(days =+ (days_in_bk + 1))
            if bk_filing >= actual_lien_exp:
                print(f'\n\tThe levy lien period already expired on {format_date(actual_lien_exp)}.')
                print('\tThere is no need to calculate any more bankruptcy stays.')
                return

            # this is repeated code from above. make this a function?
            while True:
                bk_disp = get_date('Enter bankruptcy disposition date (mm/dd/yy): ')
                if bk_disp == '0':
                    return

                if bk_disp < bk_filing:
                    print('\nBankruptcy disposition cannot occur before bankrupty was filed.')
                    press_enter()
                else:
                    break
            print()

            days_in_bk += (bk_disp - bk_filing).days
        break
    
    print(f'\n{days_in_bk} days spent in automatic stay. Therefore...\n')
    actual_lien_exp = norm_lien_exp + relativedelta(days =+ (days_in_bk + 1))

    if actual_lien_exp <= today:
        print(f'\tLevy lien period EXPIRED on {format_date(actual_lien_exp)}.')
    else:
        print(f'\tLevy lien period expires on {format_date(actual_lien_exp)}.')


def compute_employer_stay():
    #calculate 180 days from sheriff timestamp

    timestamp = get_date('Enter Sheriff timestamp date (mm/dd/yy): ')

    if timestamp == '0':
        return

    stay_date = timestamp + timedelta(days = 180)
    print(f'\n\tEmployer is to stay the wage garnishment until {format_date(stay_date)}.')


menu_items = {
    '1': 'Bankruptcy: Get EWO stay expiration date for employer',
    '2': 'Bankruptcy: Get levy lien period expiration date',
    '3': 'Can I close this file?',
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
        print()

        while True:
            menu_choice = input('> ').lower().strip()
        
            if menu_choice in menu_items:
                break
            else:
                input('That\'s not a valid choice! Press Enter to try again.')

        if menu_choice == '0':
            break
        elif menu_choice == '1':
            compute_employer_stay()
        elif menu_choice == '2':
            compute_lien_period()
        elif menu_choice == '3':
            can_i_close()
        print('\nReturning to the main menu...')
        press_enter()


def main():
    main_menu()
    print(app_name, 'terminated. Goodbye.')
    exit()


if __name__ == '__main__':
    main()
