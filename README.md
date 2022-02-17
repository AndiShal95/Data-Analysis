# Портфолио по анализу данных на Python

### Базовый анализ данных
&emsp; В рамках курса изучена работа с прикладными библиотеками *NumPy* и *Pandas* для базовой подготовки данных для анализа, а именно:
- импорт данных(*формата .csv, .tsv*) из различных интернет ресурсов и локальных источников 
[link to code import data](https://github.com/AndiShal95/Data-Analysis/blob/main/1_Basic%20Data%20Analysis/Import-data-Pandas.py)
- объединение данных из нескольких источников 
в один "dataframe" [link to code multiple-sourses data](https://github.com/AndiShal95/Data-Analysis/blob/main/1_Basic%20Data%20Analysis/Multiple-sourses-data.py)
- фильтрацию и извлечение нужных данных из "dataframe", а также преобразование данных для дальнейшего анализа
[link to code extraction data](https://github.com/AndiShal95/Data-Analysis/blob/main/1_Basic%20Data%20Analysis/data-extraction.py)
- группировка данных и построение простого предсказания события на основе модели линейной регрессии
[link to code predicting data](https://github.com/AndiShal95/Data-Analysis/blob/main/1_Basic%20Data%20Analysis/Predicting_LR.py)

### Импорт и парсинг данных
&emsp; В данном курсе рассмотрена работа с прикладными библиотеками requests и bs4 для работы с API и получением данных из HTML, то есть:
- работа с программным интерфейсом приложения(_API_) для получения необходимых данных; получены координаты города с помощью API геокодера Яндекса
[link to code receiving data](https://github.com/AndiShal95/Data-Analysis/blob/main/2_Import%20and%20Parsing%20Data/reseiving_data_by_API.py) 
- получение данных из неструктурированных источников(_HTML_) с использованием библиотеки BeautifulSoup со следующим извлечением данных для анализа
[link to code receiving data from HTML](https://github.com/AndiShal95/Data-Analysis/blob/main/2_Import%20and%20Parsing%20Data/receiving_stock_quotes.py)
- последовательный обход ссылок с главной страницы сайта для получения данных с множества страниц
[link to code parsing data](https://github.com/AndiShal95/Data-Analysis/blob/main/2_Import%20and%20Parsing%20Data/Parsing_internet_shop.py)
- в заключение, после обработки данных, полученных в результате парсинга, рассмотрено добавление результатов в базу данных при помощи *sqlite3*
[link to code download data](https://github.com/AndiShal95/Data-Analysis/blob/main/2_Import%20and%20Parsing%20Data/SQL-download_rezults_to%20database.py)

### Визуализация данных
&emsp; В курсе по визуализации данных изучено применение библиотек matplotlib, seaborn и geopandas, а именно:
- базовые типы визуализации(линейный график, областная, столбчатая и круговая диаграммы), 
комбинирование разных типов визуализации на одном графике
[link to code visualisation data](https://github.com/AndiShal95/Data-Analysis/blob/main/3_Visualisation%20Data/Visualisation_data_EGE.py)
- рассмотрены построения зависимостей между сериями однотипных данных при помощи ящичковых диаграмм с применением 
библиотеки *seaborn* [link to code dependency visualisation](https://github.com/AndiShal95/Data-Analysis/blob/main/3_Visualisation%20Data/Marathon_results.py)
- рассмотрена визуализация последовательных временных данных на примере свечных графиков
[link to code time series data](https://github.com/AndiShal95/Data-Analysis/blob/main/3_Visualisation%20Data/moving_average_on_stock_charts.py)
- рассмотрены способы работы с гео-данными и редактирование объектов на карте при помощи библиотеки *geopandas*
[link to code geo-map data](https://github.com/AndiShal95/Data-Analysis/blob/main/3_Visualisation%20Data/Culture%20heritage%20objects/culture_heritage_objects.py) 

### Создание отчетов и автоматизация задач
&emsp; В завершающем курсе изучена методика составления PDF-отчетов и работа с шаблонизаторами для автоматизации задач, а именно:
- создан PDF-документ при помощи библиотеки *reportlab*, рассмотрены методики изменения документа и
создание многостраничных отчетов [link to code PDF report](https://github.com/AndiShal95/Data-Analysis/blob/main/4_Reports%20and%20automations/work%20with%20PDF/Assembly_PDF_doc.py)
- создан HTML-отчет и преобразован в PDF-документ при помощи библиотеки *pdfkit* и бинарного файла wkhtmltopdf.exe
[link to code HTML to PDF](https://github.com/AndiShal95/Data-Analysis/blob/main/4_Reports%20and%20automations/basic%20reports/Geraldic_symbols.py)
- рассмотрена работа шаблонизатора *jinja2* для генерации HTML-строк и преобразование данных изображения в bs64-кодировку для совместного 
объединения в PDF-отчет [link to code autocomplete HTML](https://github.com/AndiShal95/Data-Analysis/blob/main/4_Reports%20and%20automations/generation%20reports/Manypages_report.py)
- в заключение, после создания отчетов рассмотрена отправка документации по e-mail с помощью библиотеки *smtplib*
[link to code send e-mail](https://github.com/AndiShal95/Data-Analysis/blob/main/4_Reports%20and%20automations/Send%20E-mail%20and%20Integrations/auto_report.py)
