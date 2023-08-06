import platform,os,sys


def main() :

    try:
        client_id = sys.argv[1]
        client_secret = sys.argv[2]
    except:
        print("\n❌️ Erreur d'execution ❌️")
        print("   Cause : Arguments requis pour l'exécution du script.\n")
        sys.exit(1)

    if platform.system() == 'Windows':
        os.system("audit_pkg\dist\main.exe %s %s" % (client_id,client_secret))
    else :
        os.system("./audit_pkg/dist/main %s %s" % (client_id,client_secret))
main()