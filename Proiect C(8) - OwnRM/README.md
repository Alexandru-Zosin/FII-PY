Proiect C: 8 - OwnRM
"Realizati un script care să imite functionalitatea utilitarului rm din Linux."

Scriptul este realizat astfel incat sa urmeze indeaproape indicatiile de pe "rm(1) - Linux manual page", functionand pentru sisteme de operare Linux si Windows.
A fost facil de implementat, fiind o buna recapitulare pentru notiuni de la cursul de Programare in Python din prima parte a semestrului.

Module folosite (prezentate la curs):
- sys
- os
- re

Functionalitati:
1. suport wildcarduri (* si ?) pentru filename (ex.: "rm -r --interactive=always folder/*")
2. suport --dry-run
3. toate optiunile de pe rm(1) - Linux manual page, cu mentiunile urmatoare:
- am implementat doar "rm ./-foo" pentru stergerea unui fisier al carui nume incepe cu '-', nu si "rm -- -foo"
- nu am testat "rm -rf --no-preserve-root /" (ma tem, chiar si pe un VM)