import tkinter as tk
import locale

# Configura a localização para o uso de vírgula como separador decimal
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def formatar_valor(valor_text):
    valor_text = valor_text.replace(',', '.')
    return valor_text

def calcular_medicao():
    medicao_final_anterior = 0
    for i in range(31):
        abertura_text = formatar_valor(abertura_entries[i].get())
        compra_text = formatar_valor(compra_entries[i].get())
        vendas_text = formatar_valor(vendas_entries[i].get())

        try:
            abertura = float(abertura_text)
            compra = float(compra_text)
            vendas = float(vendas_text)
            medicao_calculada = abertura + compra - vendas
            medicao_sem_margem_entries[i].set(f'{medicao_calculada:.3f}'.replace('.', ','))

            margem = 0.006
            resultado_mc_margem = medicao_calculada * margem
            resultado_mc_margem_entries[i].set(f'{resultado_mc_margem:.3f}'.replace('.', ','))

            if i < 30:
                medicao_inicial_dia_seguinte = medicao_final_anterior
                if medicao_final_entries[i].get() != '':
                    medicao_inicial_dia_seguinte = float(medicao_final_entries[i].get().replace(',', '.'))
                abertura_entries[i + 1].set(f'{medicao_inicial_dia_seguinte:.3f}'.replace('.', ','))

                if i < 29:
                    margem_dia_seguinte = medicao_calculada * margem
                    resultado_mc_margem_entries[i + 1].set(f'{margem_dia_seguinte:.3f}'.replace('.', ','))

                medicao_final = medicao_calculada - margem_dia_seguinte
                medicao_final_entries_calculadas[i].set(f'{medicao_final:.3f}'.replace('.', ','))

                medicao_final_anterior = medicao_final

        except ValueError:
            medicao_sem_margem_entries[i].set("0,000")
            resultado_mc_margem_entries[i].set("0,000")
            medicao_final_entries_calculadas[i].set("0,000")

def limpar_campos():
    for entry in abertura_entries + compra_entries + vendas_entries + medicao_final_entries:
        entry.set("")

def on_enter(event):
    calcular_medicao()

def calcular_perdas_ganhos():
    for i in range(31):
        medicao_final_text = formatar_valor(medicao_final_entries[i].get())
        try:
            medicao_final = float(medicao_final_text)
            medicao_calculada = float(medicao_sem_margem_entries[i].get().replace(',', '.'))
            perdas_ganhos = medicao_final - medicao_calculada
            perdas_ganhos_entries[i].set(f'{perdas_ganhos:.3f}'.replace('.', ','))
        except ValueError:
            perdas_ganhos_entries[i].set("0,000")

janela = tk.Tk()
janela.title("Correção LMC")

frame = tk.Frame(janela)
frame.pack()

abertura_entries = []
compra_entries = []
vendas_entries = []
medicao_sem_margem_entries = []
margem_entries = []
resultado_mc_margem_entries = []
medicao_final_entries = []
perdas_ganhos_entries = []
medicao_final_entries_calculadas = []

tk.Label(frame, text="Dia").grid(row=0, column=0)
tk.Label(frame, text="Medição Inicial").grid(row=0, column=1)
tk.Label(frame, text="Compra Dia (Litros)").grid(row=0, column=2)
tk.Label(frame, text="Vendas Dia (Litros)").grid(row=0, column=3)
tk.Label(frame, text="Medição Calculada").grid(row=0, column=4)
tk.Label(frame, text="Margem").grid(row=0, column=5)
tk.Label(frame, text="Resultado M.C * Margem").grid(row=0, column=6)
tk.Label(frame, text="Medição Final Calculada 0.6%").grid(row=0, column=7)
tk.Label(frame, text="Medição Final").grid(row=0, column=8)
tk.Label(frame, text="Perdas/Ganhos (LT)").grid(row=0, column=9)

for i in range(31):
    tk.Label(frame, text=f"{i+1}").grid(row=i+1, column=0)

    abertura_var = tk.StringVar()
    abertura_entry = tk.Entry(frame, textvariable=abertura_var)
    abertura_entry.grid(row=i+1, column=1)
    abertura_entries.append(abertura_var)

    compra_var = tk.StringVar()
    compra_entry = tk.Entry(frame, textvariable=compra_var)
    compra_entry.grid(row=i+1, column=2)
    compra_entries.append(compra_var)

    vendas_var = tk.StringVar()
    vendas_entry = tk.Entry(frame, textvariable=vendas_var)
    vendas_entry.grid(row=i+1, column=3)
    vendas_entries.append(vendas_var)

    medicao_sem_margem_var = tk.StringVar()
    medicao_sem_margem_entry = tk.Entry(frame, textvariable=medicao_sem_margem_var, state='readonly')
    medicao_sem_margem_entry.grid(row=i+1, column=4)
    medicao_sem_margem_entries.append(medicao_sem_margem_var)

    margem_var = tk.StringVar()
    margem_var.set("0,006")
    margem_entry = tk.Entry(frame, textvariable=margem_var, state='readonly')
    margem_entry.grid(row=i+1, column=5)
    margem_entries.append(margem_var)

    resultado_mc_margem_var = tk.StringVar()
    resultado_mc_margem_entry = tk.Entry(frame, textvariable=resultado_mc_margem_var, state='readonly')
    resultado_mc_margem_entry.grid(row=i+1, column=6)
    resultado_mc_margem_entries.append(resultado_mc_margem_var)

    medicao_final_var_calculada = tk.StringVar()
    medicao_final_entry_calculada = tk.Entry(frame, textvariable=medicao_final_var_calculada, state='readonly')
    medicao_final_entry_calculada.grid(row=i+1, column=7)
    medicao_final_entries_calculadas.append(medicao_final_var_calculada)

    medicao_final_var = tk.StringVar()
    medicao_final_entry = tk.Entry(frame, textvariable=medicao_final_var)
    medicao_final_entry.grid(row=i+1, column=8)
    medicao_final_entries.append(medicao_final_var)

    perdas_ganhos_var = tk.StringVar()
    perdas_ganhos_entry = tk.Entry(frame, textvariable=perdas_ganhos_var, state='readonly')
    perdas_ganhos_entry.grid(row=i+1, column=9)
    perdas_ganhos_entries.append(perdas_ganhos_var)

calcular_button = tk.Button(frame, text="Calcular", command=calcular_medicao)
calcular_button.grid(row=32, column=0, columnspan=5)

calcular_pg_button = tk.Button(frame, text="Calcular Perdas/Ganhos", command=calcular_perdas_ganhos)
calcular_pg_button.grid(row=32, column=5, columnspan=5)

limpar_button = tk.Button(frame, text="Limpar Campos", command=limpar_campos)
limpar_button.grid(row=33, column=0, columnspan=5)

# Texto "By Júlio Cesar" no canto direito da tela
by_label = tk.Label(frame, text="By Júlio Cesar")
by_label.grid(row=34, column=9, sticky="se")

# Configurar a tecla "Del" para limpar os campos
janela.bind("<Delete>", lambda event=None: limpar_campos())

# Configurar a tecla "Enter" para calcular
janela.bind("<Return>", on_enter)

janela.mainloop()