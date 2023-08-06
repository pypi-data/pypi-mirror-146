import platform,os,sys


def main() :

    try :
        param1=sys.argv[1]
    except :    
        print("❌️ Impossible d'executer le script !!!\n   Argument manquant")
        sys.exit(1)

    if platform.system() == 'Windows':
        os.system("audit_pkg\dist\main.exe %s " % param1)
    else :
        os.system("./audit_pkg/dist/main %s " % param1)
