
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# =====================================
# BANCO DE DADOS
# =====================================

conn = sqlite3.connect("stockmanager.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    min_stock INTEGER NOT NULL
)
""")

conn.commit()


# =====================================
# APLICAÇÃO PRINCIPAL
# =====================================

class StockManager:

    def __init__(self, root):
        self.root = root
        self.root.title("StockManager - Controle de Estoque")
        self.root.geometry("1050x650")
        self.root.configure(bg="#F1F5F9")

        self.selected_id = None

        self.create_interface()
        self.load_products()
        self.update_dashboard()

    # =================================
    # INTERFACE
    # =================================

    def create_interface(self):

        header = tk.Frame(
            self.root,
            bg="#172554",
            height=85
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text="StockManager",
            font=("Arial", 24, "bold"),
            bg="#172554",
            fg="white"
        ).pack(pady=20)

        dashboard = tk.Frame(
            self.root,
            bg="#F1F5F9"
        )
        dashboard.pack(fill="x", padx=20, pady=15)

        self.total_label = tk.Label(
            dashboard,
            text="Produtos: 0",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#1E40AF",
            padx=20,
            pady=20
        )
        self.total_label.pack(side="left", padx=5)

        self.stock_label = tk.Label(
            dashboard,
            text="Unidades: 0",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#166534",
            padx=20,
            pady=20
        )
        self.stock_label.pack(side="left", padx=5)

        self.low_label = tk.Label(
            dashboard,
            text="Estoque baixo: 0",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#DC2626",
            padx=20,
            pady=20
        )
        self.low_label.pack(side="left", padx=5)

        # FORMULÁRIO

        form = tk.LabelFrame(
            self.root,
            text="Cadastro de produtos",
            bg="#F1F5F9",
            padx=10,
            pady=10
        )
        form.pack(fill="x", padx=20, pady=10)

        tk.Label(form, text="Produto:", bg="#F1F5F9").grid(
            row=0, column=0, sticky="w"
        )

        self.name_entry = tk.Entry(form, width=20)
        self.name_entry.grid(row=1, column=0, padx=5)

        tk.Label(form, text="Categoria:", bg="#F1F5F9").grid(
            row=0, column=1, sticky="w"
        )

        self.category_entry = tk.Entry(form, width=18)
        self.category_entry.grid(row=1, column=1, padx=5)

        tk.Label(form, text="Quantidade:", bg="#F1F5F9").grid(
            row=0, column=2, sticky="w"
        )

        self.quantity_entry = tk.Entry(form, width=12)
        self.quantity_entry.grid(row=1, column=2, padx=5)

        tk.Label(form, text="Preço:", bg="#F1F5F9").grid(
            row=0, column=3, sticky="w"
        )

        self.price_entry = tk.Entry(form, width=12)
        self.price_entry.grid(row=1, column=3, padx=5)

        tk.Label(form, text="Estoque mínimo:", bg="#F1F5F9").grid(
            row=0, column=4, sticky="w"
        )

        self.min_entry = tk.Entry(form, width=12)
        self.min_entry.grid(row=1, column=4, padx=5)

        # BOTÕES

        buttons = tk.Frame(self.root, bg="#F1F5F9")
        buttons.pack(fill="x", padx=20, pady=5)

        tk.Button(
            buttons,
            text="Cadastrar",
            bg="#2563EB",
            fg="white",
            command=self.add_product
        ).pack(side="left", padx=5)

        tk.Button(
            buttons,
            text="Atualizar",
            bg="#D97706",
            fg="white",
            command=self.update_product
        ).pack(side="left", padx=5)

        tk.Button(
            buttons,
            text="Excluir",
            bg="#DC2626",
            fg="white",
            command=self.delete_product
        ).pack(side="left", padx=5)

        tk.Button(
            buttons,
            text="Limpar",
            command=self.clear_form
        ).pack(side="left", padx=5)

        # PESQUISA

        search_frame = tk.Frame(
            self.root,
            bg="#F1F5F9"
        )
        search_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(
            search_frame,
            text="Pesquisar produto:",
            bg="#F1F5F9"
        ).pack(side="left")

        self.search_entry = tk.Entry(
            search_frame,
            width=30
        )
        self.search_entry.pack(side="left", padx=10)

        tk.Button(
            search_frame,
            text="Pesquisar",
            command=self.search_product
        ).pack(side="left")

        tk.Button(
            search_frame,
            text="Mostrar todos",
            command=self.load_products
        ).pack(side="left", padx=5)

        # TABELA

        table_frame = tk.Frame(self.root)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "ID", "Produto", "Categoria",
            "Quantidade", "Preço", "Estoque mínimo"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:
            self.table.heading(column, text=column)
            self.table.column(column, width=140)

        self.table.pack(fill="both", expand=True)

        self.table.bind(
            "<<TreeviewSelect>>",
            self.select_product
        )

        self.table.tag_configure(
            "low",
            background="#FEE2E2"
        )

    # =================================
    # CADASTRAR PRODUTO
    # =================================

    def add_product(self):

        try:
            name = self.name_entry.get().strip()
            category = self.category_entry.get().strip()
            quantity = int(self.quantity_entry.get())
            price = float(
                self.price_entry.get().replace(",", ".")
            )
            minimum = int(self.min_entry.get())

            if not name or not category:
                raise ValueError

            if quantity < 0 or price < 0 or minimum < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Preencha todos os campos corretamente."
            )
            return

        cursor.execute("""
            INSERT INTO products
            (name, category, quantity, price, min_stock)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name, category, quantity, price, minimum
        ))

        conn.commit()

        self.load_products()
        self.update_dashboard()
        self.clear_form()

        messagebox.showinfo(
            "Sucesso",
            "Produto cadastrado!"
        )

    # =================================
    # CARREGAR PRODUTOS
    # =================================

    def load_products(self):

        self.search_entry.delete(0, tk.END)

        for item in self.table.get_children():
            self.table.delete(item)

        cursor.execute(
            "SELECT * FROM products ORDER BY name"
        )

        for product in cursor.fetchall():

            tag = (
                "low"
                if product[3] <= product[5]
                else ""
            )

            self.table.insert(
                "",
                "end",
                values=product,
                tags=(tag,)
            )

        self.update_dashboard()

    # =================================
    # SELECIONAR PRODUTO
    # =================================

    def select_product(self, event):

        selected = self.table.selection()

        if not selected:
            return

        values = self.table.item(
            selected[0], "values"
        )

        self.selected_id = values[0]

        self.clear_entries_only()

        self.name_entry.insert(0, values[1])
        self.category_entry.insert(0, values[2])
        self.quantity_entry.insert(0, values[3])
        self.price_entry.insert(0, values[4])
        self.min_entry.insert(0, values[5])

    # =================================
    # ATUALIZAR PRODUTO
    # =================================

    def update_product(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "Atenção",
                "Selecione um produto na tabela."
            )
            return

        try:
            name = self.name_entry.get().strip()
            category = self.category_entry.get().strip()
            quantity = int(self.quantity_entry.get())
            price = float(
                self.price_entry.get().replace(",", ".")
            )
            minimum = int(self.min_entry.get())

            if not name or not category:
                raise ValueError

            if quantity < 0 or price < 0 or minimum < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Erro",
                "Verifique os dados informados."
            )
            return

        cursor.execute("""
            UPDATE products
            SET name = ?,
                category = ?,
                quantity = ?,
                price = ?,
                min_stock = ?
            WHERE id = ?
        """, (
            name,
            category,
            quantity,
            price,
            minimum,
            self.selected_id
        ))

        conn.commit()

        self.load_products()
        self.clear_form()

        messagebox.showinfo(
            "Sucesso",
            "Produto atualizado!"
        )

    # =================================
    # EXCLUIR PRODUTO
    # =================================

    def delete_product(self):

        if self.selected_id is None:
            messagebox.showwarning(
                "Atenção",
                "Selecione um produto."
            )
            return

        confirm = messagebox.askyesno(
            "Confirmação",
            "Deseja excluir este produto?"
        )

        if confirm:

            cursor.execute(
                "DELETE FROM products WHERE id = ?",
                (self.selected_id,)
            )

            conn.commit()

            self.load_products()
            self.clear_form()

    # =================================
    # PESQUISAR
    # =================================

    def search_product(self):

        term = self.search_entry.get().strip()

        for item in self.table.get_children():
            self.table.delete(item)

        cursor.execute("""
            SELECT * FROM products
            WHERE name LIKE ?
            ORDER BY name
        """, (f"%{term}%",))

        for product in cursor.fetchall():

            tag = (
                "low"
                if product[3] <= product[5]
                else ""
            )

            self.table.insert(
                "",
                "end",
                values=product,
                tags=(tag,)
            )

    # =================================
    # DASHBOARD
    # =================================

    def update_dashboard(self):

        cursor.execute("""
            SELECT COUNT(*),
                   COALESCE(SUM(quantity), 0),
                   COALESCE(SUM(
                       CASE WHEN quantity <= min_stock
                       THEN 1 ELSE 0 END
                   ), 0)
            FROM products
        """)

        total, units, low = cursor.fetchone()

        self.total_label.config(
            text=f"Produtos: {total}"
        )

        self.stock_label.config(
            text=f"Unidades: {units}"
        )

        self.low_label.config(
            text=f"Estoque baixo: {low}"
        )

    # =================================
    # LIMPAR FORMULÁRIO
    # =================================

    def clear_entries_only(self):

        for entry in (
            self.name_entry,
            self.category_entry,
            self.quantity_entry,
            self.price_entry,
            self.min_entry
        ):
            entry.delete(0, tk.END)

    def clear_form(self):

        self.clear_entries_only()
        self.selected_id = None
        self.table.selection_remove(
            self.table.selection()
        )


# =====================================
# EXECUÇÃO
# =====================================

if __name__ == "__main__":

    root = tk.Tk()
    app = StockManager(root)

    def close_application():
        conn.close()
        root.destroy()

    root.protocol(
        "WM_DELETE_WINDOW",
        close_application
    )

    root.mainloop()
