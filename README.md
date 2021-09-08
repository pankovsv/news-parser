### news-parser
Парсер новостей с сайта [Lenta.ru](https://lenta.ru).
При нажатии на кнопку **Parse** проходит по всем новостям за сегодняшнюю дату, записывает название новости и ссылку на данную новость в базу данных под управлением **PostgreSQL**.
Если новость уже присутствует в базе данных, повторной записи не происходит.
Чтобы получить список новостей и ссылки на них за определенную дату и месяц, нужно ввести в соответствующие поля дату и месяц и нажать **Read DB**.

Для запуска тестов нужно закомментировать код графической части и раскомментировать код тестов.