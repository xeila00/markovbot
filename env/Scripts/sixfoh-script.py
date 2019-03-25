#!C:\Users\porte\Desktop\tweetbot\markovbot\env\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'sixfoh==0.1.3','console_scripts','sixfoh'
__requires__ = 'sixfoh==0.1.3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('sixfoh==0.1.3', 'console_scripts', 'sixfoh')()
    )
