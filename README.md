<<<<<<< HEAD
# ABAnalizer
=======
# ABAnalizer
>>>>>>> c5562ff6d9707ba36720446373a7ba474cae22b0

# Git using
Обновить/проверить состояние ветки - git pull origin 'Branchname'
Создать новую ветку и перейти в нее- git checkout -b 'Branchname'
Перейти в ветку - git checkout 'Branchname'
Подгрузить себе чужие ветки для последующего перехода - git fetch
Добавить в ветку изменения в мастере - git merge origin master
Скоммитить изменения - git commit "text of the commit"
Пушнуть изменения на сервер github - git push origin 'Branchname'
Понять, в какой ветке находишься - git branch
Скоммитить и пушнуть можно еще через Version Control (внизу)
=========

# Git example
К примеру, если нужно сделать новую задачу, то последовательность команд будет такая:
1) git pull origin master (убедились, что мастер последний или обновили его)
2) git checkout -b NS/NewTaskBranch (создали новую ветку от мастера!!!!! (новые ветки создаются всегда от мастера), и перешли
в нее. Нужно заметить, что в начале названия ветки стоят инициалы автора)
3) Codding...
4) git commit "text of the commit" ("сохранили изменения" локально и написали к ним комментарии)
5) git push origin NS/NewTaskBranch (отправили изменения на сервер) 
После чего на сервере во вкладке "Pull requests" нажать на кнопку "New pull request" и во вкладке "compare" выбрать свою ветку.
После чего нажать "Create pull request".
Вернуться в pycharm и продолжить Codding...
После логического блока повторить пункты 4-5.
После чего, обсудить с коллегами работу новшеств и примержить к мастеру ветку.

P.S. Пункты 4 и 5 можно проделать мышкой (по-человечески) во вкладке "Version Control" внизу pycharm. Внутри вкладки есть
окно "Local Changes" и при нажатии правой клавишей на "Default" - выбрать пункт "Commit Changes", а в нем "Commit and push".


