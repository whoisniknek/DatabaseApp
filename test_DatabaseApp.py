import unittest
from unittest.mock import patch, MagicMock
from DatabaseApp import DatabaseApp
import tkinter as tk

class TestDatabaseApp(unittest.TestCase):
    def setUp(self):
        """Инициализация перед тестами"""
        self.root = tk.Tk()  # Создаем корневой элемент для тестов
        self.app = DatabaseApp(self.root)

    @patch("pymysql.connect")
    def test_database_connection(self, mock_connect):
        """Тест подключения к базе данных"""
        mock_connect.return_value = MagicMock()
        self.assertIsNotNone(self.app.conn)

    def test_create_tabs(self):
        """Тест создания вкладок"""
        self.app.create_tabs()
        tabs = self.app.tab_control.tabs()
        self.assertEqual(len(tabs), 5)
        expected_tabs = ["Менеджеры", "Продукты", "Поставщики", "Партнеры", "Заказы"]
        for i, tab in enumerate(tabs):
            self.assertIn(expected_tabs[i], self.app.tab_control.tab(tab, "text"))

if __name__ == "__main__":
    unittest.main()
