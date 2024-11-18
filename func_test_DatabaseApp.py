import unittest
from unittest.mock import patch, MagicMock
from DatabaseApp import DatabaseApp
import tkinter as tk


class FunctionalTestDatabaseApp(unittest.TestCase):
    def setUp(self):
        """Инициализация приложения перед выполнением тестов"""
        self.root = tk.Tk()
        self.app = DatabaseApp(self.root)

    @patch("pymysql.connect")
    def test_full_database_interaction(self, mock_connect):
        """Функциональный тест взаимодействия с базой данных"""
        # Мокаем подключение к базе данных
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        # Эмуляция работы с базой данных
        mock_cursor.execute.return_value = None
        mock_cursor.fetchall.return_value = [("Менеджер 1",), ("Менеджер 2",)]

        # Проверка вызовов базы данных
        self.app.conn = mock_connection
        self.app.create_tabs()
        self.app.tab_control.select(self.app.manager_tab)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM managers")
        data = mock_cursor.fetchall()
        self.assertEqual(len(data), 2)

    def test_gui_navigation(self):
        """Функциональный тест навигации GUI"""
        self.app.create_tabs()
        tabs = self.app.tab_control.tabs()
        self.assertIn("Менеджеры", self.app.tab_control.tab(tabs[0], "text"))

        # Эмуляция переключения вкладок
        self.app.tab_control.select(tabs[1])
        self.assertEqual(self.app.tab_control.tab(tabs[1], "text"), "Продукты")

    def tearDown(self):
        """Завершение работы приложения после тестов"""
        self.root.destroy()


if __name__ == "__main__":
    unittest.main()