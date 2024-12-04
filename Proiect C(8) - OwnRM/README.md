# Proiect C: 8 - OwnRM

*Realizati un script care să imite functionalitatea utilitarului rm din Linux.*

Scriptul este realizat astfel incat sa urmeze indeaproape indicatiile de pe *rm(1) - Linux manual page*, functionand pentru sisteme de operare Linux si Windows.
A fost facil de implementat, fiind o buna recapitulare pentru notiuni de la cursul de *Programare in Python* din prima parte a semestrului.
Fiecare functionalitate descrisa si implementata de pe *rm(1) - Linux manual page* este indicata corespunzator in cod printr-un comentariu.

Logica din spatele scriptului:
1. se executa de la linia de comanda *python rm.py [OPTIONS] [PATHS]*
2. se parseaza comanda (argumentele) cu functia *parse_command(args)*
- validare argumente
- unpacking in options(aceleasi pentru toate paths) si paths
3. pentru fiecare path, se verifica daca este sau nu director
- Y => *remove_dir(path, options)*, care foloseste *os.walk(topdown=False)* astfel incat sa utilizam mai intai *remove_file()*, dupa care *remove_empty_dir()* pe directoarele ramase fara continut
- N => *remove_file(path, options)*

Module folosite (prezentate la curs):
- *sys*
- *os*
- *re*

Functionalitati:
1. suport wildcarduri (* si ?) pentru filename (ex.: "rm -r --interactive=always folder/*")
2. suport --dry-run
3. toate optiunile de pe *rm(1) - Linux manual page*, cu mentiunile urmatoare:
- niciun bug *cunoscut* (am testat scriptul pe Windows 10 si intr-un Kali Linux VM)
- posibil sa fi omis/nu fie plasate perfect blocuri *try-except*
- am implementat doar "rm ./-foo" pentru stergerea unui fisier al carui nume incepe cu '-', nu si "rm -- -foo"
- am testat --one-file-system si --preserve-root=all doar pe Windows 10 cu symlinks si un USB Drive (D:)
- nu am testat "rm -rf --no-preserve-root /" (ma tem, chiar si pe un VM)