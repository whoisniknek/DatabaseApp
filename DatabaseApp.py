import tkinter as tk
from tkinter import ttk, messagebox
import pymysql


class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление Базой Данных")
        self.root.geometry("1000x600")
        self.page_index = 0
        self.partners_per_page = 3

        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            database='master_pol'
        )

        self.create_tabs()
    def create_tabs(self):
        self.tab_control = ttk.Notebook(self.root)

        self.manager_tab = ttk.Frame(self.tab_control)
        self.product_tab = ttk.Frame(self.tab_control)
        self.supplier_tab = ttk.Frame(self.tab_control)
        self.partner_tab = ttk.Frame(self.tab_control)
        self.order_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.manager_tab, text="Менеджеры")
        self.tab_control.add(self.product_tab, text="Продукты")
        self.tab_control.add(self.supplier_tab, text="Поставщики")
        self.tab_control.add(self.partner_tab, text="Партнеры")
        self.tab_control.add(self.order_tab, text="Заказы")


        self.tab_control.pack(expand=1, fill='both')

        self.create_manager_tab()
        self.create_product_tab()
        self.create_supplier_tab()
        self.create_partner_tab()
        self.create_order_tab()
    def calculate_discount(self, partner_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT SUM(price) FROM sales_history WHERE partner_id=%s", (partner_id,))
        total_sales = cursor.fetchone()[0] or 0

        if total_sales > 300000:
            return "15%"
        elif total_sales > 50000:
            return "10%"
        elif total_sales > 10000:
            return "5%"
        else:
            return "0%"
    def create_partner_tab(self):
        self.canvas = tk.Canvas(self.partner_tab)
        self.scrollbar = ttk.Scrollbar(self.partner_tab, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.partner_frame = ttk.Frame(self.partner_tab)

        ttk.Button(self.partner_tab, text="Добавить партнера", command=self.open_add_partner_window).pack(pady=10)

        self.load_partners()
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.root.bind("<Configure>", self.adjust_card_width)

        self.load_partners()
    def adjust_card_width(self, event=None):
        canvas_width = self.canvas.winfo_width()
        self.canvas.itemconfig(self.canvas.find_withtag("all")[0], width=canvas_width)
    def load_partners(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        cursor = self.conn.cursor()
        cursor.execute("SELECT partner_id, name, type, address, phone, email, rating,inn FROM partners")
        partners = cursor.fetchall()

        for partner in partners:
            partner_id, name, partner_type, address, phone, email, rating,inn = partner

            partner_card = tk.Frame(self.scrollable_frame, borderwidth=1, relief="solid", padx=10, pady=10)
            partner_card.pack(pady=5, fill=tk.X)

            tk.Label(partner_card, text=f"ID: {partner_id}").grid(row=0, column=0, sticky="w")
            tk.Label(partner_card, text=f"Название: {name}").grid(row=1, column=0, sticky="w")
            tk.Label(partner_card, text=f"Тип: {partner_type}").grid(row=2, column=0, sticky="w")
            tk.Label(partner_card, text=f"Адрес: {address}").grid(row=3, column=0, sticky="w")
            tk.Label(partner_card, text=f"Телефон: {phone}").grid(row=4, column=0, sticky="w")
            tk.Label(partner_card, text=f"Email: {email}").grid(row=5, column=0, sticky="w")
            tk.Label(partner_card, text=f"Рэйтинг: {rating}").grid(row=6, column=0, sticky="w")
            tk.Label(partner_card, text=f"ИНН: {inn}").grid(row=5, column=2, sticky="w")
            discount = self.calculate_discount(partner_id)
            tk.Label(partner_card, text=f"Скидка: {discount}").grid(row=6, column=2, sticky="w")
            ttk.Button(partner_card, text="Редактировать",
                       command=lambda pid=partner_id: self.open_edit_partner_window(pid)).grid(row=7, column=0)
            ttk.Button(partner_card, text="Удалить", command=lambda pid=partner_id: self.delete_partner(pid)).grid(
                row=7, column=1)
            ttk.Button(partner_card, text="История", command=lambda pid=partner_id: self.show_sales_history(pid)).grid(
                row=7, column=2)
    def save_partner_changes(self, partner_id, name_entry, type_entry, address_entry, phone_entry, email_entry, rating_entry):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE partners SET name=%s, type=%s, address=%s, phone=%s, email=%s, rating=%s WHERE partner_id=%s
        """, (
            name_entry.get(),
            type_entry.get(),
            address_entry.get(),
            phone_entry.get(),
            email_entry.get(),
            rating_entry.get(),
            partner_id
        ))
        self.conn.commit()
        self.load_partners()
    def open_edit_partner_window(self, partner_id):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактирование партнера")
        edit_window.geometry("400x300")

        cursor = self.conn.cursor()
        cursor.execute("SELECT name, type, address, phone, email, rating FROM partners WHERE partner_id=%s",
                       (partner_id,))
        partner_data = cursor.fetchone()

        if partner_data:
            name, type_, address, phone, email, rating = partner_data

            tk.Label(edit_window, text="Название").grid(row=0, column=0, padx=10, pady=10)
            name_entry = tk.Entry(edit_window)
            name_entry.insert(0, name)
            name_entry.grid(row=0, column=1)

            tk.Label(edit_window, text="Тип").grid(row=1, column=0, padx=10, pady=10)
            type_entry = tk.Entry(edit_window)
            type_entry.insert(0, type_)
            type_entry.grid(row=1, column=1)

            tk.Label(edit_window, text="Адрес").grid(row=2, column=0, padx=10, pady=10)
            address_entry = tk.Entry(edit_window)
            address_entry.insert(0, address)
            address_entry.grid(row=2, column=1)

            tk.Label(edit_window, text="Телефон").grid(row=3, column=0, padx=10, pady=10)
            phone_entry = tk.Entry(edit_window)
            phone_entry.insert(0, phone)
            phone_entry.grid(row=3, column=1)

            tk.Label(edit_window, text="Email").grid(row=4, column=0, padx=10, pady=10)
            email_entry = tk.Entry(edit_window)
            email_entry.insert(0, email)
            email_entry.grid(row=4, column=1)

            tk.Label(edit_window, text="Рейтинг").grid(row=5, column=0, padx=10, pady=10)
            rating_entry = tk.Entry(edit_window)
            rating_entry.insert(0, rating)
            rating_entry.grid(row=5, column=1)

            ttk.Button(edit_window, text="Сохранить",
                       command=lambda: self.save_partner_changes(partner_id, name_entry, type_entry, address_entry,
                                                                 phone_entry, email_entry, rating_entry)).grid(row=6,
                                                                                                               column=0,
                                                                                                               columnspan=2,
                                                                                                               pady=10)
    def create_order_tab(self):
        self.order_frame = ttk.Frame(self.order_tab)
        self.order_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        search_frame = ttk.Frame(self.order_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(search_frame, text="Поиск заказа:").pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_button = ttk.Button(search_frame, text="Найти", command=self.search_order)
        self.search_button.pack(side=tk.LEFT)

        self.order_tree = ttk.Treeview(self.order_frame,
                                       columns=("sale_id", "partner_id", "product_id", "price", "sale_date"),
                                       show="headings")
        self.order_tree.pack(fill=tk.BOTH, expand=True)

        for col in self.order_tree["columns"]:
            self.order_tree.heading(col, text=col)

        self.load_orders()

        button_frame = ttk.Frame(self.order_frame)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Добавить заказ", command=self.open_add_order_window).pack(side=tk.LEFT, padx=5)
    def load_orders(self):
        for row in self.order_tree.get_children():
            self.order_tree.delete(row)
        cursor = self.conn.cursor()
        cursor.execute("SELECT sale_id, partner_id, product_id, price, sale_date FROM sales_history")
        for row in cursor.fetchall():
            self.order_tree.insert("", tk.END, values=row)
    def search_order(self):
        search_term = self.search_entry.get()
        if not search_term:
            messagebox.showerror("Ошибка", "Введите данные для поиска.")
            return

        for row in self.order_tree.get_children():
            self.order_tree.delete(row)

        cursor = self.conn.cursor()
        query = """
            SELECT sale_id, partner_id, product_id, price, sale_date 
            FROM sales_history 
            WHERE sale_id LIKE %s OR partner_id LIKE %s OR product_id LIKE %s OR price LIKE %s OR sale_date LIKE %s
        """
        cursor.execute(query, (f"%{search_term}%",) * 5)
        results = cursor.fetchall()

        if results:
            for row in results:
                self.order_tree.insert("", tk.END, values=row)
        else:
            messagebox.showinfo("Результаты поиска", "Заказы не найдены.")
    def open_add_order_window(self):
        self.add_order_window = tk.Toplevel(self.root)
        self.add_order_window.title("Добавить заказ")
        self.add_order_window.geometry("320x150")

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT partner_id, name FROM partners")
        self.partners = cursor.fetchall()
        partner_choices = [f"{partner[0]} - {partner[1]}" for partner in self.partners]

        tk.Label(self.add_order_window, text="Выберите партнера:").grid(row=0, column=0)
        self.partner_combobox = ttk.Combobox(self.add_order_window, values=partner_choices, state="readonly")
        self.partner_combobox.grid(row=0, column=1)

        cursor.execute(
            "SELECT product_id, product FROM products")
        self.products = cursor.fetchall()
        product_choices = [f"{product[0]} - {product[1]}" for product in self.products]

        tk.Label(self.add_order_window, text="Выберите продукт:").grid(row=1, column=0)
        self.product_combobox = ttk.Combobox(self.add_order_window, values=product_choices, state="readonly")
        self.product_combobox.grid(row=1, column=1)

        tk.Label(self.add_order_window, text="Цена:").grid(row=2, column=0)
        self.price_entry = tk.Entry(self.add_order_window)
        self.price_entry.grid(row=2, column=1)

        tk.Label(self.add_order_window, text="Дата продажи (ГГГГ-ММ-ДД):").grid(row=3, column=0)
        self.sale_date_entry = tk.Entry(self.add_order_window)
        self.sale_date_entry.grid(row=3, column=1)

        save_button = ttk.Button(self.add_order_window, text="Сохранить", command=self.add_order)
        save_button.grid(row=4, columnspan=2, pady=10)
    def add_order(self):
        selected_partner = self.partner_combobox.get()
        selected_product = self.product_combobox.get()
        price = self.price_entry.get()
        sale_date = self.sale_date_entry.get()

        if not selected_partner or not selected_product or not price or not sale_date:
            messagebox.showerror("Ошибка", "Заполните все поля.")
            return

        partner_id = selected_partner.split(" - ")[0]
        product_id = selected_product.split(" - ")[0]

        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO sales_history (partner_id, product_id, price, sale_date) VALUES (%s, %s, %s, %s)",
                (partner_id, product_id, price, sale_date)
            )
            self.conn.commit()
            messagebox.showinfo("Успех", "Заказ добавлен успешно.")
            self.add_order_window.destroy()
            self.load_orders()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить заказ: {e}")
    def show_sales_history(self, partner_id):
        history_window = tk.Toplevel(self.root)
        history_window.title("История реализации продукции")
        history_window.geometry("1000x400")

        history_frame = ttk.Frame(history_window)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tree = ttk.Treeview(history_frame, columns=("sale_id", "partner_id", "product_id", "price", "sale_date"), show='headings')
        tree.heading("sale_id", text="ID продажи")
        tree.heading("partner_id", text="ID партнера")
        tree.heading("product_id", text="ID товара")
        tree.heading("price", text="Цена")
        tree.heading("sale_date", text="Дата продажи")

        tree.pack(fill=tk.BOTH, expand=True)

        cursor = self.conn.cursor()
        cursor.execute("SELECT sale_id, partner_id, product_id, price, sale_date FROM sales_history WHERE partner_id=%s", (partner_id,))
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
    def show_partner_card(self, index):
        for widget in self.partner_frame.winfo_children():
            widget.destroy()

        partner = self.partners[index]

        partner_card = tk.Frame(self.partner_frame, borderwidth=1, relief="solid", padx=10, pady=10)
        partner_card.pack(pady=5, fill=tk.X)

        partner_id, name, type, address, phone, email, rating = partner

        tk.Label(partner_card, text=f"ID: {partner_id}").grid(row=0, column=0, sticky="w")
        tk.Label(partner_card, text=f"Название: {name}").grid(row=1, column=0, sticky="w")
        tk.Label(partner_card, text=f"Тип: {type}").grid(row=2, column=0, sticky="w")
        tk.Label(partner_card, text=f"Адрес: {address}").grid(row=3, column=0, sticky="w")
        tk.Label(partner_card, text=f"Телефон: {phone}").grid(row=4, column=0, sticky="w")
        tk.Label(partner_card, text=f"Email: {email}").grid(row=5, column=0, sticky="w")
        tk.Label(partner_card, text=f"Рэйтинг: {rating}").grid(row=6, column=0, sticky="w")
        discount = self.calculate_discount(partner_id)
        tk.Label(partner_card, text=f"Скидка: {discount}").grid(row=7, column=0, sticky='w')
    def open_add_partner_window(self):
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("Добавить партнера")
        self.add_window.geometry("300x400")

        tk.Label(self.add_window, text="Название:").grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(self.add_window)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.add_window, text="Тип:").grid(row=1, column=0, padx=10, pady=5)
        self.type_entry = tk.Entry(self.add_window)
        self.type_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.add_window, text="Адрес:").grid(row=2, column=0, padx=10, pady=5)
        self.address_entry = tk.Entry(self.add_window)
        self.address_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.add_window, text="Телефон:").grid(row=3, column=0, padx=10, pady=5)
        self.phone_entry = tk.Entry(self.add_window)
        self.phone_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.add_window, text="Email:").grid(row=4, column=0, padx=10, pady=5)
        self.email_entry = tk.Entry(self.add_window)
        self.email_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self.add_window, text="Рейтинг:").grid(row=5, column=0, padx=10, pady=5)
        self.rating_entry = tk.Entry(self.add_window)
        self.rating_entry.grid(row=5, column=1, padx=10, pady=5)

        save_button = ttk.Button(self.add_window, text="Сохранить", command=self.add_partner)
        save_button.grid(row=6, columnspan=2, pady=10)
    def add_partner(self):
        name = self.name_entry.get()
        type_ = self.type_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        rating = self.rating_entry.get()

        if name and type_ and address and phone and email and rating:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO partners (name, type, address, phone, email, rating) VALUES (%s, %s, %s, %s, %s, %s)",
                (name, type_, address, phone, email, rating)
            )
            self.conn.commit()
            self.add_window.destroy()
            self.load_partners()
        else:
            messagebox.showerror("Ошибка", "Заполните все поля корректно!")
    def edit_partner(self, partner_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, type, address, phone, email, rating FROM partners WHERE partner_id=%s",
                       (partner_id,))
        partner_data = cursor.fetchone()

        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Редактировать партнера")
        self.edit_window.geometry("300x400")

        tk.Label(self.edit_window, text="Название:").grid(row=0, column=0, padx=10, pady=5)
        self.edit_name_entry = tk.Entry(self.edit_window)
        self.edit_name_entry.insert(0, partner_data[0])
        self.edit_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.edit_window, text="Тип:").grid(row=1, column=0, padx=10, pady=5)
        self.edit_type_entry = tk.Entry(self.edit_window)
        self.edit_type_entry.insert(0, partner_data[1])
        self.edit_type_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.edit_window, text="Адрес:").grid(row=2, column=0, padx=10, pady=5)
        self.edit_address_entry = tk.Entry(self.edit_window)
        self.edit_address_entry.insert(0, partner_data[2])
        self.edit_address_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.edit_window, text="Телефон:").grid(row=3, column=0, padx=10, pady=5)
        self.edit_phone_entry = tk.Entry(self.edit_window)
        self.edit_phone_entry.insert(0, partner_data[3])
        self.edit_phone_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.edit_window, text="Email:").grid(row=4, column=0, padx=10, pady=5)
        self.edit_email_entry = tk.Entry(self.edit_window)
        self.edit_email_entry.insert(0, partner_data[4])
        self.edit_email_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self.edit_window, text="Рейтинг:").grid(row=5, column=0, padx=10, pady=5)
        self.edit_rating_entry = tk.Entry(self.edit_window)
        self.edit_rating_entry.insert(0, partner_data[5])
        self.edit_rating_entry.grid(row=5, column=1, padx=10, pady=5)

        save_button = ttk.Button(self.edit_window, text="Сохранить", command=lambda: self.update_partner(partner_id))
        save_button.grid(row=6, columnspan=2, pady=10)
    def update_partner(self, partner_id):
        name = self.edit_name_entry.get()
        type_ = self.edit_type_entry.get()
        address = self.edit_address_entry.get()
        phone = self.edit_phone_entry.get()
        email = self.edit_email_entry.get()
        rating = self.edit_rating_entry.get()

        if name and type_ and address and phone and email and rating:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE partners SET name=%s, type=%s, address=%s, phone=%s, email=%s, rating=%s WHERE partner_id=%s",
                (name, type_, address, phone, email, rating, partner_id)
            )
            self.conn.commit()
            self.edit_window.destroy()
            self.load_partners()
        else:
            messagebox.showerror("Ошибка", "Заполните все поля корректно!")
    def delete_partner(self, partner_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM partners WHERE partner_id = %s", (partner_id,))
        self.conn.commit()
        self.load_partners()
    def create_manager_tab(self):
        self.manager_frame = ttk.Frame(self.manager_tab)
        self.manager_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.manager_tree = ttk.Treeview(self.manager_frame, columns=("ID", "Имя", "Фамилия", "Телефон", "Email"),
                                         show='headings')
        self.manager_tree.pack(fill=tk.BOTH, expand=True)

        for col in self.manager_tree["columns"]:
            self.manager_tree.heading(col, text=col)

        self.load_managers()

        button_frame = ttk.Frame(self.manager_tab)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Добавить менеджера", command=self.open_add_manager_window).pack(side=tk.LEFT,
                                                                                                       padx=5)
        ttk.Button(button_frame, text="Редактировать менеджера", command=self.open_edit_manager_window).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить менеджера", command=self.delete_manager).pack(side=tk.LEFT, padx=5)
    def create_product_tab(self):
        self.product_frame = ttk.Frame(self.product_tab)
        self.product_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.product_tree = ttk.Treeview(self.product_frame,
                                         columns=("ID", "Название", "Описание", "Минимальная цена", "Размер упаковки"),
                                         show='headings')
        self.product_tree.pack(fill=tk.BOTH, expand=True)

        for col in self.product_tree["columns"]:
            self.product_tree.heading(col, text=col)

        self.load_products()

        button_frame = ttk.Frame(self.product_tab)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Добавить продукт", command=self.open_add_product_window).pack(side=tk.LEFT,
                                                                                                     padx=5)
        ttk.Button(button_frame, text="Редактировать продукт", command=self.open_edit_product_window).pack(side=tk.LEFT,
                                                                                                           padx=5)
        ttk.Button(button_frame, text="Удалить продукт", command=self.delete_product).pack(side=tk.LEFT, padx=5)
    def create_supplier_tab(self):
        self.supplier_frame = ttk.Frame(self.supplier_tab)
        self.supplier_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.supplier_tree = ttk.Treeview(self.supplier_frame, columns=("ID", "Название", "Тип", "ИНН", "История"),
                                          show='headings')
        self.supplier_tree.pack(fill=tk.BOTH, expand=True)

        for col in self.supplier_tree["columns"]:
            self.supplier_tree.heading(col, text=col)

        self.load_suppliers()

        button_frame = ttk.Frame(self.supplier_tab)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Добавить поставщика", command=self.open_add_supplier_window).pack(side=tk.LEFT,
                                                                                                         padx=5)
        ttk.Button(button_frame, text="Редактировать поставщика", command=self.open_edit_supplier_window).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить поставщика", command=self.delete_supplier).pack(side=tk.LEFT, padx=5)
    def load_managers(self):
        for row in self.manager_tree.get_children():
            self.manager_tree.delete(row)
        cursor = self.conn.cursor()
        cursor.execute("SELECT manager_id, first_name, last_name, phone, email FROM managers")
        for row in cursor.fetchall():
            self.manager_tree.insert("", tk.END, values=row)
    def load_products(self):
        for row in self.product_tree.get_children():
            self.product_tree.delete(row)
        cursor = self.conn.cursor()
        cursor.execute("SELECT product_id, product, partnier_name,quantity, date_sale FROM products")
        for row in cursor.fetchall():
            self.product_tree.insert("", tk.END, values=row)
    def load_suppliers(self):
        for row in self.supplier_tree.get_children():
            self.supplier_tree.delete(row)
        cursor = self.conn.cursor()
        cursor.execute("SELECT supplier_id, name, type, inn, supply_history FROM suppliers")
        for row in cursor.fetchall():
            self.supplier_tree.insert("", tk.END, values=row)
    def open_add_manager_window(self):
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("Добавить Менеджера")
        self.add_window.geometry("300x300")

        tk.Label(self.add_window, text="Имя:").grid(row=0, column=0)
        self.first_name_entry = tk.Entry(self.add_window)
        self.first_name_entry.grid(row=0, column=1)

        tk.Label(self.add_window, text="Фамилия:").grid(row=1, column=0)
        self.last_name_entry = tk.Entry(self.add_window)
        self.last_name_entry.grid(row=1, column=1)

        tk.Label(self.add_window, text="Телефон:").grid(row=2, column=0)
        self.phone_entry = tk.Entry(self.add_window)
        self.phone_entry.grid(row=2, column=1)

        tk.Label(self.add_window, text="Email:").grid(row=3, column=0)
        self.email_entry = tk.Entry(self.add_window)
        self.email_entry.grid(row=3, column=1)

        save_button = ttk.Button(self.add_window, text="Сохранить", command=self.add_manager)
        save_button.grid(row=4, columnspan=2)
    def add_manager(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        if first_name and last_name and phone and email:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO managers (first_name, last_name, phone, email) VALUES (%s, %s, %s, %s)",
                (first_name, last_name, phone, email)
            )
            self.conn.commit()
            self.add_window.destroy()
            self.load_managers()
        else:
            messagebox.showerror("Ошибка", "Заполните все поля корректно!")
    def open_edit_manager_window(self):
        selected_item = self.manager_tree.selection()
        if not selected_item:
            messagebox.showwarning("Выбор", "Пожалуйста, выберите менеджера для редактирования.")
            return

        manager_id = self.manager_tree.item(selected_item)['values'][0]
        cursor = self.conn.cursor()
        cursor.execute("SELECT first_name, last_name, phone, email FROM managers WHERE manager_id=%s", (manager_id,))
        manager_data = cursor.fetchone()

        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Редактировать Менеджера")
        self.edit_window.geometry("300x300")

        tk.Label(self.edit_window, text="Имя:").grid(row=0, column=0)
        self.edit_first_name_entry = tk.Entry(self.edit_window)
        self.edit_first_name_entry.insert(0, manager_data[0])
        self.edit_first_name_entry.grid(row=0, column=1)

        tk.Label(self.edit_window, text="Фамилия:").grid(row=1, column=0)
        self.edit_last_name_entry = tk.Entry(self.edit_window)
        self.edit_last_name_entry.insert(0, manager_data[1])
        self.edit_last_name_entry.grid(row=1, column=1)

        tk.Label(self.edit_window, text="Телефон:").grid(row=2, column=0)
        self.edit_phone_entry = tk.Entry(self.edit_window)
        self.edit_phone_entry.insert(0, manager_data[2])
        self.edit_phone_entry.grid(row=2, column=1)

        tk.Label(self.edit_window, text="Email:").grid(row=3, column=0)
        self.edit_email_entry = tk.Entry(self.edit_window)
        self.edit_email_entry.insert(0, manager_data[3])
        self.edit_email_entry.grid(row=3, column=1)

        save_button = ttk.Button(self.edit_window, text="Сохранить", command=lambda: self.update_manager(manager_id))
        save_button.grid(row=4, columnspan=2)
    def update_manager(self, manager_id):
        first_name = self.edit_first_name_entry.get()
        last_name = self.edit_last_name_entry.get()
        phone = self.edit_phone_entry.get()
        email = self.edit_email_entry.get()

        if first_name and last_name and phone and email:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE managers SET first_name=%s, last_name=%s, phone=%s, email=%s WHERE manager_id=%s",
                (first_name, last_name, phone, email, manager_id)
            )
            self.conn.commit()
            self.edit_window.destroy()
            self.load_managers()
        else:
            messagebox.showerror("Ошибка", "Заполните все поля корректно!")
    def delete_manager(self):
        selected_item = self.manager_tree.selection()
        if not selected_item:
            messagebox.showwarning("Выбор", "Пожалуйста, выберите менеджера для удаления.")
            return

        manager_id = self.manager_tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этого менеджера?"):
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM managers WHERE manager_id=%s", (manager_id,))
            self.conn.commit()
            self.load_managers()
    def open_add_product_window(self):
        self.add_product_window = tk.Toplevel(self.root)
        self.add_product_window.title("Добавить Продукт")
        self.add_product_window.geometry("300x300")

        tk.Label(self.add_product_window, text="Название:").grid(row=0, column=0)
        self.product_name_entry = tk.Entry(self.add_product_window)
        self.product_name_entry.grid(row=0, column=1)

        tk.Label(self.add_product_window, text="Имя партнера:").grid(row=1, column=0)
        self.product_description_entry = tk.Entry(self.add_product_window)
        self.product_description_entry.grid(row=1, column=1)

        tk.Label(self.add_product_window, text="Количество:").grid(row=2, column=0)
        self.product_min_price_entry = tk.Entry(self.add_product_window)
        self.product_min_price_entry.grid(row=2, column=1)

        tk.Label(self.add_product_window, text="Дата продажи:").grid(row=3, column=0)
        self.product_size_entry = tk.Entry(self.add_product_window)
        self.product_size_entry.grid(row=3, column=1)

        save_button = ttk.Button(self.add_product_window, text="Сохранить", command=self.add_product)
        save_button.grid(row=4, columnspan=2)
    def add_product(self):
        product = self.product_name_entry.get()
        partnier_name = self.product_description_entry.get()
        quantity = self.product_min_price_entry.get()
        date_sale = self.product_size_entry.get()

        if product and partnier_name and quantity and date_sale:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO products (product, partnier_name, quantity, date_sale) VALUES (%s, %s, %s, %s)",
                (product, partnier_name, quantity, date_sale)
            )

            self.conn.commit()
            self.add_product_window.destroy()
            self.load_products()
        else:
            messagebox.showerror("Ошибка", "Заполните все поля корректно!")
    def open_edit_product_window(self):
        selected_item = self.product_tree.selection()
        if not selected_item:
            messagebox.showwarning("Выбор", "Пожалуйста, выберите продукт для редактирования.")
            return

        product_id = self.product_tree.item(selected_item)['values'][0]
        cursor = self.conn.cursor()
        cursor.execute("SELECT product, partnier_name, quantity, date_sale FROM products WHERE product_id=%s",
                       (product_id,))
        product_data = cursor.fetchone()

        self.edit_product_window = tk.Toplevel(self.root)
        self.edit_product_window.title("Редактировать Продукт")
        self.edit_product_window.geometry("300x300")

        tk.Label(self.edit_product_window, text="Название:").grid(row=0, column=0)
        self.edit_product_name_entry = tk.Entry(self.edit_product_window)
        self.edit_product_name_entry.insert(0, product_data[0])
        self.edit_product_name_entry.grid(row=0, column=1)

        tk.Label(self.edit_product_window, text="Имя партнера:").grid(row=1, column=0)
        self.edit_product_description_entry = tk.Entry(self.edit_product_window)
        self.edit_product_description_entry.insert(0, product_data[1])
        self.edit_product_description_entry.grid(row=1, column=1)

        tk.Label(self.edit_product_window, text="Количество:").grid(row=2, column=0)
        self.edit_product_min_price_entry = tk.Entry(self.edit_product_window)
        self.edit_product_min_price_entry.insert(0, product_data[2])
        self.edit_product_min_price_entry.grid(row=2, column=1)

        tk.Label(self.edit_product_window, text="Дата продажи:").grid(row=3, column=0)
        self.edit_product_size_entry = tk.Entry(self.edit_product_window)
        self.edit_product_size_entry.insert(0, product_data[3])
        self.edit_product_size_entry.grid(row=3, column=1)

        save_button = ttk.Button(self.edit_product_window, text="Сохранить",
                                 command=lambda: self.update_product(product_id))
        save_button.grid(row=4, columnspan=2)
    def update_product(self, product_id):
        name = self.edit_product_name_entry.get()
        description = self.edit_product_description_entry.get()
        min_price = self.edit_product_min_price_entry.get()
        size = self.edit_product_size_entry.get()

        if name and description and min_price and size:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE products SET product=%s, partnier_name=%s, quantity=%s, date_sale=%s WHERE product_id=%s",
                (name, description, min_price, size, product_id)
            )

            self.conn.commit()
            self.edit_product_window.destroy()
            self.load_products()
        else:
            messagebox.showerror("Ошибка", "Заполните все поля корректно!")
    def delete_product(self):
        selected_item = self.product_tree.selection()
        if not selected_item:
            messagebox.showwarning("Выбор", "Пожалуйста, выберите продукт для удаления.")
            return

        product_id = self.product_tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот продукт?"):
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
            self.conn.commit()
            self.load_products()
    def open_add_supplier_window(self):
        self.add_supplier_window = tk.Toplevel(self.root)
        self.add_supplier_window.title("Добавить Поставщика")
        self.add_supplier_window.geometry("300x300")

        tk.Label(self.add_supplier_window, text="Название:").grid(row=0, column=0)
        self.supplier_name_entry = tk.Entry(self.add_supplier_window)
        self.supplier_name_entry.grid(row=0, column=1)

        tk.Label(self.add_supplier_window, text="Тип:").grid(row=1, column=0)
        self.supplier_type_entry = tk.Entry(self.add_supplier_window)
        self.supplier_type_entry.grid(row=1, column=1)

        tk.Label(self.add_supplier_window, text="ИНН:").grid(row=2, column=0)
        self.supplier_inn_entry = tk.Entry(self.add_supplier_window)
        self.supplier_inn_entry.grid(row=2, column=1)

        tk.Label(self.add_supplier_window, text="История:").grid(row=3, column=0)
        self.supply_history_entry = tk.Entry(self.add_supplier_window)
        self.supply_history_entry.grid(row=3, column=1)

        save_button = ttk.Button(self.add_supplier_window, text="Сохранить", command=self.add_supplier)
        save_button.grid(row=4, columnspan=2)
    def add_supplier(self):
        name = self.supplier_name_entry.get()
        type = self.supplier_type_entry.get()
        inn = self.supplier_inn_entry.get()
        supply_history = self.supply_history_entry.get()

        if name and type and inn and supply_history:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO suppliers (name, type, inn, supply_history) VALUES (%s, %s, %s, %s)",
                (name, type, inn, supply_history)
            )
            self.conn.commit()
            self.add_supplier_window.destroy()
            self.load_suppliers()
        else:
            messagebox.showerror("Ошибка", "Заполните все поля корректно!")
    def open_edit_supplier_window(self):
        selected_item = self.supplier_tree.selection()
        if not selected_item:
            messagebox.showwarning("Выбор", "Пожалуйста, выберите поставщика для редактирования.")
            return

        supplier_id = self.supplier_tree.item(selected_item)['values'][0]
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, type, inn, supply_history FROM suppliers WHERE supplier_id=%s", (supplier_id,))
        supplier_data = cursor.fetchone()

        self.edit_supplier_window = tk.Toplevel(self.root)
        self.edit_supplier_window.title("Редактировать Поставщика")
        self.edit_supplier_window.geometry("300x300")

        tk.Label(self.edit_supplier_window, text="Название:").grid(row=0, column=0)
        self.edit_supplier_name_entry = tk.Entry(self.edit_supplier_window)
        self.edit_supplier_name_entry.insert(0, supplier_data[0])
        self.edit_supplier_name_entry.grid(row=0, column=1)

        tk.Label(self.edit_supplier_window, text="Тип:").grid(row=1, column=0)
        self.edit_supplier_type_entry = tk.Entry(self.edit_supplier_window)
        self.edit_supplier_type_entry.insert(0, supplier_data[1])
        self.edit_supplier_type_entry.grid(row=1, column=1)

        tk.Label(self.edit_supplier_window, text="ИНН:").grid(row=2, column=0)
        self.edit_supplier_inn_entry = tk.Entry(self.edit_supplier_window)
        self.edit_supplier_inn_entry.insert(0, supplier_data[2])
        self.edit_supplier_inn_entry.grid(row=2, column=1)

        tk.Label(self.edit_supplier_window, text="История:").grid(row=3, column=0)
        self.edit_supplier_history_entry = tk.Entry(self.edit_supplier_window)
        self.edit_supplier_history_entry.insert(0, supplier_data[3])
        self.edit_supplier_history_entry.grid(row=3, column=1)

        save_button = ttk.Button(self.edit_supplier_window, text="Сохранить",
                                 command=lambda: self.update_supplier(supplier_id))
        save_button.grid(row=4, columnspan=2)
    def update_supplier(self, supplier_id):
        name = self.edit_supplier_name_entry.get()
        type = self.edit_supplier_type_entry.get()
        inn = self.edit_supplier_inn_entry.get()
        supply_history = self.edit_supplier_history_entry.get()

        if name and type and inn and supply_history:
            cursor = self.conn.cursor()

            cursor.execute(
                "UPDATE suppliers SET name=%s, type=%s, inn=%s, supply_history=%s WHERE supplier_id=%s",
                (name, type, inn, supply_history, supplier_id)
            )

            self.conn.commit()
            self.edit_supplier_window.destroy()
            self.load_suppliers()
        else:
            messagebox.showerror("Ошибка", "Заполните все поля корректно!")
    def delete_supplier(self):
        selected_item = self.supplier_tree.selection()
        if not selected_item:
            messagebox.showwarning("Выбор", "Пожалуйста, выберите поставщика для удаления.")
            return

        supplier_id = self.supplier_tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этого поставщика?"):
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM suppliers WHERE supplier_id=%s", (supplier_id,))
            self.conn.commit()
            self.load_suppliers()

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
