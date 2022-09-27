
import sys
import os
import shutil
import glob



if __name__ == '__main__':

    if 'EAZY' in os.environ:
        
        eazypath = os.getenv('EAZY')
        print('EAZY PATH:', eazypath)

        if len(sys.argv) == 2:
            template_set = sys.argv[1] # need to add version number
        else:
            template_set = 'Wilkins22' # need to add version number

        print(template_set)

        src = f'templates/{template_set}'
        dst = f'{eazypath}/templates/{template_set}/'

        # --- copy template folder
        shutil.copytree(src, dst, dirs_exist_ok=True)

        for src in glob.glob(f'templates/{template_set}*.param'):

            print(src)

            # --- copy template param file
            dst = f'{eazypath}/templates/'
            shutil.copy(src, dst)
