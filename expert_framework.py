import pandas as pd


# Перечень необходимых для анализа полей (в исходном файле данных 250+ полей, которые не влазят в оперативку)
fields = [0,4,5,7,82]

#Считывание файла финансовых данных Росстата
data = pd.read_csv('data-20191029t000000-structure-20181231t000000.csv', sep=';', encoding='ansi', header=None, usecols=fields)


# Отделение от поля INN первых 2-х цифр для поиска по регионам
data['first_2_inn'] = data[5].astype(str).str[:2].astype(int)

# Фильтрация только компаний из Свердловской области
data3 =  data[data['first_2_inn']==66]

# Разделение поля ОКВЭД на 2 части - до и после '.'
data3['new_okved'] = data3[4].str.split(".", n = 1, expand = True)[0]

# Фильтрация компаний из ИТ-сферы по их коду ОКВЭД (код 62 и 63)
data_new_it1 =  data3[data3['new_okved']=='62'] 
data_new_it2 =  data3[data3['new_okved']=='63'] 

# Объединение датафреймов в один файл
it = pd.concat([data_new_it1, data_new_it2])

# Переименование колонок для лучшего восприятия
it2 = it.rename(columns={0: 'name', 4: 'full_okved', 5: 'inn', 7: 'size', 82: 'income'})

#Подготовка категорий для разделения выручки по ьинам
bin_labels_5 = ['Ниже среднего', 'Средняя', 'Выше среднего', 'Высокая']

# Приведение выручки от тыс. руб к млн. руб
it2['income'] = it2['income']/1000

#Бинаризация выручки
it2['quantile_ex_3'] = pd.qcut(it2['income'],
                              q=[ .2, .4, .6, .8, 1],
                              labels=bin_labels_5, duplicates='drop')

#Запись в файл
it2.to_csv('itcompanies.csv', sep=';', mode='a', index=True, header=True, encoding='ansi', decimal=',')
