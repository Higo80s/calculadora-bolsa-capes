import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from .core import calcular_prazo_bolsa

class CalculadoraBolsaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Prazo de Bolsa CAPES")
        self.root.geometry("440x320")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))
        style.configure("TCombobox", font=("Segoe UI", 10))

        ttk.Label(root, text="Data de ingresso no curso (DD/MM/AAAA):").pack(pady=(20, 5))
        self.entry_ingresso = ttk.Entry(root, width=20, font=("Consolas", 11))
        self.entry_ingresso.pack()

        ttk.Label(root, text="Data de início da bolsa (opcional):").pack(pady=(10, 5))
        self.entry_inicio = ttk.Entry(root, width=20, font=("Consolas", 11))
        self.entry_inicio.pack()

        ttk.Label(root, text="Nível do curso:").pack(pady=(10, 5))
        self.combo_nivel = ttk.Combobox(root, values=["Mestrado", "Doutorado"], state="readonly", width=18)
        self.combo_nivel.set("Selecione")
        self.combo_nivel.pack()

        ttk.Button(root, text="Calcular Prazo Máximo", command=self.calcular).pack(pady=25)

    def calcular(self):
        try:
            ingresso_str = self.entry_ingresso.get().strip()
            inicio_str = self.entry_inicio.get().strip()
            nivel_str = self.combo_nivel.get()

            if not ingresso_str:
                raise ValueError("Informe a data de ingresso.")
            if nivel_str == "Selecione":
                raise ValueError("Selecione o nível do curso.")

            dia, mes, ano = map(int, ingresso_str.split('/'))
            ingresso = date(ano, mes, dia)

            if inicio_str:
                dia, mes, ano = map(int, inicio_str.split('/'))
                inicio = date(ano, mes, dia)
            else:
                hoje = date.today()
                inicio = date(hoje.year, hoje.month, 1)

            resultado = calcular_prazo_bolsa(ingresso, inicio, nivel_str.lower())

            if resultado["ultimo_pagamento"]:
                mes_nome = resultado["ultimo_pagamento"].strftime("%B de %Y")
                meses_pt = {
                    "January": "janeiro", "February": "fevereiro", "March": "março",
                    "April": "abril", "May": "maio", "June": "junho",
                    "July": "julho", "August": "agosto", "September": "setembro",
                    "October": "outubro", "November": "novembro", "December": "dezembro"
                }
                for eng, pt in meses_pt.items():
                    mes_nome = mes_nome.replace(eng, pt)
            else:
                mes_nome = "—"

            msg = (
                f"✅ Período regular até: {resultado['data_limite_periodo']:%d/%m/%Y}\n"
                f"📅 Início da bolsa: {inicio:%d/%m/%Y}\n"
                f"🔢 Meses máximos permitidos: {resultado['max_meses']}\n"
                f"📆 Último mês com pagamento: {mes_nome}"
            )
            messagebox.showinfo("Resultado", msg)

        except Exception as e:
            messagebox.showerror("Erro de Validação", f"Entrada inválida:\n{e}\n\nUse DD/MM/AAAA.")

def main():
    root = tk.Tk()
    app = CalculadoraBolsaApp(root)
    root.mainloop()