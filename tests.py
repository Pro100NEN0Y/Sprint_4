import pytest
from main import BooksCollector

class TestBooksCollector:

    # Пример теста из заготовки: проверка добавления двух книг
    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    # 1. Параметризованный тест на добавление книг с валидной длиной названия (1 символ, 40 символов)
    @pytest.mark.parametrize('book_name', ['A', 'Книга ровно из сорока символов (40)!!'])
    def test_add_new_book_valid_name_len_added(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert book_name in collector.get_books_genre()

    # 2. Негативный тест: книга с названием 41 символ не должна добавляться
    def test_add_new_book_name_41_symbols_not_added(self):
        collector = BooksCollector()
        bad_name = 'Имя книги состоящее из сорока одного симв!'  # Ровно 41 символ
        collector.add_new_book(bad_name)
        assert bad_name not in collector.get_books_genre()

    # 3. Негативный тест: повторное добавление одной и той же книги
    def test_add_new_book_double_add_not_duplicated(self):
        collector = BooksCollector()
        collector.add_new_book('Русалочка')
        collector.add_new_book('Русалочка')
        assert len(collector.get_books_genre()) == 1

    # 4. Проверка успешной установки жанра из разрешенного списка
    def test_set_book_genre_existing_genre_set_successfully(self):
        collector = BooksCollector()
        collector.add_new_book('Дракула')
        collector.set_book_genre('Дракула', 'Ужасы')
        assert collector.get_book_genre('Дракула') == 'Ужасы'

    # 5. Проверка, что нельзя установить жанр, которого нет в списке доступных
    def test_set_book_genre_not_existing_genre_not_set(self):
        collector = BooksCollector()
        collector.add_new_book('Дракула')
        collector.set_book_genre('Дракула', 'Киберпанк')
        assert collector.get_book_genre('Дракула') == ''

    # 6. Проверка получения списка книг по конкретному жанру
    def test_get_books_with_specific_genre_returns_matching_books(self):
        collector = BooksCollector()
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        collector.set_book_genre('Книга 1', 'Фантастика')
        collector.set_book_genre('Книга 2', 'Комедии')
        
        books = collector.get_books_with_specific_genre('Фантастика')
        assert 'Книга 1' in books and 'Книга 2' not in books

    # 7. Проверка фильтрации книг для детей (жанры с возрастным рейтингом исключаются)
    def test_get_books_for_children_excludes_age_rating_genres(self):
        collector = BooksCollector()
        collector.add_new_book('Винни Пух')
        collector.add_new_book('Сияние')
        collector.set_book_genre('Винни Пух', 'Мультфильмы')
        collector.set_book_genre('Сияние', 'Ужасы')
        
        children_books = collector.get_books_for_children()
        assert 'Винни Пух' in children_books and 'Сияние' not in children_books

    # 8. Проверка добавления существующей книги в избранное
    def test_add_book_in_favorites_added_successfully(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.add_book_in_favorites('Дюна')
        assert 'Дюна' in collector.get_list_of_favorites_books()

    # 9. Проверка, что нельзя добавить в избранное книгу, которой нет в коллекции
    def test_add_book_in_favorites_not_in_collector_not_added(self):
        collector = BooksCollector()
        collector.add_book_in_favorites('Несуществующая книга')
        assert 'Несуществующая книга' not in collector.get_list_of_favorites_books()

    # 10. Проверка удаления книги из избранного
    def test_delete_book_from_favorites_deleted_successfully(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.add_book_in_favorites('Дюна')
        collector.delete_book_from_favorites('Дюна')
        assert 'Дюна' not in collector.get_list_of_favorites_books()