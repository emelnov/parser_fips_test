# Проверка возможности парсинга
## Тестовый парсинг, для проверки возможности сбора данных о свежих публикациях на сайте fips.ru

Проверка возможности и анализ возможных сложностей при сборе данных сайта fips.ru

Сбор данных начинается со страницы
https://www.fips.ru/publication-web/publications/UsrTM?pageNumber=1&inputSelectOIS=TM,CKTM,AOG,ERAOG,TMIR&tab=UsrTM&searchSortSelect=dtPublish&searchSortDirection=true

Файл readme.docx содержит обзор на возможности сбора информации 

Папка "parsed_data" содержит результаты сбора иинформации сайта fips.ru
По каждой отдельной публикации хранится:
Файл маленького изображения
Файл большого изображения
PDF бюллютень
XML результат сбора информации о товарном знаке (тестовый, можно расширить)
JSON формат результата

### Пока не стояла цель "собрать данные максимально подоробно", это быстрая тестовая версия скрита для выявления возможных проблем при сборе инфорации. Поэтому:
***В  json и xml файлах содержится инфомрация:***
+ ***о цветах***
+ ***наличии/отсутствии не охраняемых элеметов***
+ ***классах мкту***
+ ***файлы изображений***
+ ***документы в PDF***
+ ***даты публикации и регистрации сведений***

###Исследование на текущий момент показывает, что припятствий к сбору и структурированию данных нет.***