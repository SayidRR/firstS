import flet as ft
import requests
import gspread


API_KEY = 'AIzaSyBzXxsW3KIaRyuE3CQxzMseilsSgpXH2mw'

def get_book_info(query):
    url = 'https://www.googleapis.com/books/v1/volumes'
    params = {
        'q': query,
        'key': API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if 'items' in data:
        book = data['items'][0]['volumeInfo'] 
        title = book.get('title', 'Нет названия')
        authors = book.get('authors', 'Нет авторов')
        return title, authors
    else:
        return "Книги не найдены"

def main(page: ft.Page):
    page.title = "Поиск книги"
    book_title_input = ft.TextField(label="Введите название книги", width=300)
    result_title = ft.Text("")
    result_authors = ft.Text("")
    
    name=ft.TextField(label="Имя",width=250, visible=False)
    email=ft.TextField(label="Email",width=250, visible=False)
    phone=ft.TextField(label="Телефон",width=250, visible=False)
    address=ft.TextField(label="Адрес",width=250, visible=False) 
    aser=ft.ElevatedButton(text="Купить", on_click=lambda e: register(e))
    def sheets(e):
        a=name.value
        b=email.value
        v=phone.value
        d=address.value
        gc = gspread.service_account(filename='creds.json')
        wks = gc.open("GetBook").sheet1
        wks.update([[a],[b],[v],[d],[result_title.value],[result_authors.value]], 'A1')
        wks.update_acell('B42', "it's down there somewhere, let me take another look.")
        wks.format('A1:B1', {'textFormat': {'bold': True}})
    get=ft.ElevatedButton(text="Получить",visible=False,on_click=lambda e: sheets(e))
    def search_book(e):
        query = book_title_input.value  
        title, authors = get_book_info(query) 
        result_title.value = f"Название: {title}"
        result_authors.value = f"Авторы: {', '.join(authors) if isinstance(authors, list) else authors}"
        page.add(
            aser
        )
        page.update()
    search_button = ft.ElevatedButton(text="Получить", on_click=lambda e: search_book(e))    
        
    def register(e):
        name.visible = True
        email.visible = True
        phone.visible = True
        address.visible = True
        alignment=ft.MainAxisAlignment.CENTER
        aser.visible=False
        get.visible=True
        page.update()

    page.add(
        book_title_input,
        search_button,
        result_title,
        result_authors,
    )

    page.add(
        ft.Row([
            ft.Column([
                name,
                email,
                phone,
                address,
                get
                ],
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER),
    )
ft.app(target=main,view=ft.AppView.WEB_BROWSER)