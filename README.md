Тестовое задание
1. Задача
Написать 2 приложения в Qt5:
	Сервер (имитирует систему управления оборудованием);
	Клиент (имитирует рабочее место оператора). 
 
2. Описание Сервера
При старте сервер вычитывает из статически заданного каталога все XML-файлы, разбирает полученные данные и записывает их в БД SQLite. Далее сервер начинает ждать TCP подключение. После установления соединения с клиентом и при получении запроса от клиента сервер выдает ему все данные из БД. 
2.1. XML-файлы
Каждый XML-файл содержит в себе описание (структуру) одной единицы оборудования:
 
Именем файла является IP-адрес оборудования (например 10.1.6.115).
Набор XML файлов прилагается.
2.2. База данных
В качестве базы данных используется SQLite. Формат хранения данных разрабатывается самостоятельно.
2.3. Взаимодействие с клиентом
Сервер ждет TCP подключения. После установлении соединения сервер ждет запроса. При получении запроса от клиента передает ему все данные из БД. Формат запроса/ответа и передаваемых данных разрабатывается самостоятельно.
Сетевые настройки IP/TCP-порт выбираются исполнителем и не изменяются.
2.4. Фоновые задачи сервера
Сервер контролирует раз в минуту наличие изменений в файлах XML.
При обнаружении изменений сервер перечитывает соответствующий XML файл и обновляет информацию в БД.
3. Клиент
Клиент при старте подключается к серверу, запрашивает и выводит на экран ПК полученные данные в qtreeview/qtreewidget. 
Клиент отображает состояние соединения с сервером и информацию об ошибках.
4. Требования к процессу разработки
Использовать контроль версий Git.
Разработку функционала вести в ветке dev.
Отлаженный стабильный код загружать в ветку master.
Файлы XMLи БД исключить из контроля версий.
Результирующий проект выгрузить в репозиторий на Github и предоставить ссылку.
