import os


def clean(numFiles=100):
    for i in range(numFiles):
        try:
            os.remove('varlist{}'.format(i))
            os.remove('trace{}'.format(i))
            print('Deleted varlist{} and trace{}'.format(i,i))
        except:
            print('No varlist{} and trace{}'.format(i,i))
    
