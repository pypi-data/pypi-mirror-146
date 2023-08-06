import os
import sys

def main():
    if len(sys.argv) != 2:
        print('This script do the setup for cmd.exe', 'Run:', '> win-basic-tools setup', 'Then refresh your cmd.exe', sep='\n')
        quit(0)
    
    if sys.argv[1] == 'uninstall':
        uninstall()
        quit(0)

    if sys.argv[1] != 'setup':
        print('This script do the setup for cmd.exe', 'Run:', '> win-basic-tools setup', sep='\n')
        quit(0)

    assert sys.platform == 'win32'
    
    sources_path = f'{sys.exec_prefix}/Lib/site-packages/win_basic_tools/sources'
    home_path = os.path.expanduser('~')

    with open(f'{home_path}\\.macros.doskey', 'w') as file:
        file.write(
            f'''ls=python {sources_path}\\ls.py $1 $2\n
            ll=python {sources_path}\\ls.py -lac\n
            which=python {sources_path}\\which.py $1\n
            touch=python {sources_path}\\touch.py $*\n
            cat=type $1\n
            pwd=cd\n
            mv=move $1 $2\n
            rm=del $*\n''')
        
        
    os.system(f'reg add "HKCU\\Software\\Microsoft\\Command Processor" /v Autorun /d "doskey /macrofile=\\"{home_path}\\.macros.doskey\"" /f')

def uninstall():
    home_path = os.path.expanduser('~')

    os.system(f'reg delete "HKCU\\Software\\Microsoft\\Command Processor" /v Autorun')
    os.system(f'del {home_path}\\.macros.doskey')
    print('Refresh you cmd.exe for complete uninstall')

if __name__ == '__main__':
    main()