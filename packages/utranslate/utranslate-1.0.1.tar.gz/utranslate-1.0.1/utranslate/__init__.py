from utranslate.setup import my_setup
import os
import time

import sys
import subprocess


subprocess.check_call([sys.executable, '-m', 'pip', 'install',
'tensorflow-addons==0.12.1'])


def do_the_setup():

    # this script will do all the nesserry setup action requried for the application..

    print('\n\n')

    setup = my_setup()

    #setting up the directories...
    setup.driectory_setup()

    os.environ['utranslate_data_path'] = setup.root_dir

    print(f"Created directory utranslate_data in { os.environ['utranslate_data_path'] } \n\n")


data_path = os.environ.get('utranslate_data_path')


if data_path == None:
    print("Welcome to utranslate! \n")

    print("completing the basic setup......")
    do_the_setup()

    i = 0
    while(i < 10):
        print('█ ',end='')
        time.sleep(0.5)
        i+=1

    print("\n\n setup completed .. ")
