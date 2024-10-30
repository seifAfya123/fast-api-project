import os

from termcolor import colored 
path = os.getenv("MY_DB_URL")

print(colored(path,"red"))