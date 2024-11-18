import unittest
from unittest.mock import patch, MagicMock
from DatabaseApp import DatabaseApp
import tkinter as tk


class IntegrationTestDatabaseApp(unittest.TestCase):
    def setUp(self):
        """Инициализация приложения перед выполнением тестов"""
        self.root = tk.Tk()
        self.app = DatabaseApp(self.root)

    @patch("pymysql.connect")
    def test_integration_with_database(self, mock_connect):
        """Интеграционный тест: взаимодействие GUI и базы данных"""
        # Мокаем подключение к базе данных
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        # Заглушка данных из базы
        mock_cursor.fetchall.return_value = [
            (1, "Менеджер 1", "Тип 1", "Адрес 1", "1234567890", "email1@example.com", 4.5, "123456789"),
        ]

        # Подключаем приложение к "базе"
        self.app.conn = mock_connection
        self.app.load_partners()  # Загрузка данных партнеров из базы

        # Проверка, что данные корректно отображены в интерфейсе
        partner_tree = self.app.partner_tree
        self.assertEqual(partner_tree.get_children(), ('1',))  # Проверяем, что данные загружены

    def test_gui_database_flow(self):
        """Интеграционный тест GUI: проверка полного цикла работы"""
        self.app.create_tabs()  # Создаем вкладки
        tabs = self.app.tab_control.tabs()

        # Проверяем, что можно переключаться между вкладками
        self.app.tab_control.select(tabs[1])  # Переключение на "Продукты"
        self.assertEqual(self.app.tab_control.tab(tabs[1], "text"), "Продукты")

    def tearDown(self):
        """Завершение работы приложения после тестов"""
        self.root.destroy()


if __name__ == "__main__":
    unittest.main()
