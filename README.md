Напишите веб-приложение, с единственным методом API, которое принимало бы
   запрос в формате, указанном ниже, и возвращало бы какой-то сигнал, если в
   запросе присутствовал новый IP-адрес или NgToken для указанного пользователя.

```JSON
{
    'GUID': <GUID>,
    'Timestamp': '%Y-%m-%d %H:%M:%S'
    'OuterIP': <OuterIP>,
    'NgToken': <NgToken>
}
```

## Для корректной работы программы необходимо заполнить файл .env данными базы данных PostgreSQL
