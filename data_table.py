# Senti a necessidade de ter um DataTable onde eu possa reaproveitar em outras lógicas
# e assim evitar reescrita, com ajuda da documentação e de parceiros da web do curso 
# Programadoe Aventureiro já fazia uso de DataTable em meus projetos.
# Senti a necessidade de editar dados da tabela e por outro lado excluir linhas da tabela.
# Como poderia fazer isso se ao clicar na coluna ele apenas marcava o checkbox?
# Então criei uma coluna para os checkboxes. Mas como implementar o mesmo comportamento da função on_select_changed?
# Depois de muita briga e com a ajuda de duas inteligências Artificiais Chat GPT e BlackBox chegamos neste exemplo abaixo:

import flet as ft

class CustomDataTable:
    def __init__(self, colunas, linhas):
        self.colunas = colunas
        self.linhas = linhas
        self.checkbox_states = [False] * len(linhas)  # Estados dos checkboxes individuais.
        self.data_table = None  # Inicialização da tabela.

    def toggle_all_checkboxes(self, e):
        is_checked = e.control.value
        for i in range(len(self.checkbox_states)):
            self.checkbox_states[i] = is_checked
            self.data_table.rows[i].cells[0].content.value = is_checked
            self.data_table.rows[i].cells[0].content.update()
            self.data_table.update()  # Atualizando a Tabela.
        print(f"Todos os checkboxes foram {'marcados' if is_checked else 'desmarcados'}.")

    def checkbox_changed(self, e, index):
        self.checkbox_states[index] = e.control.value
        print(f"Checkbox da linha {index+1} {'marcado' if e.control.value else 'desmarcado'}.")
        if not e.control.value:
            self.data_table.columns[0].label.value = False
            self.data_table.columns[0].label.update()
        else:
            if all(self.checkbox_states):
                self.data_table.columns[0].label.value = True
                self.data_table.columns[0].label.update()
        self.data_table.update() # Atualizando a Tabela.

    # Função para ordenar as colunas
    def sort_column(self, e):
        column_index = e.column_index
        self.data_table.sort_ascending = not self.data_table.sort_ascending
        if column_index == 0:
            self.data_table.rows.sort(key=lambda x: x.cells[column_index].content.value, reverse=not self.data_table.sort_ascending)
            self.checkbox_states = [row.cells[0].content.value for row in self.data_table.rows]  # Update checkbox_states
        else:
            self.data_table.rows.sort(key=lambda x: x.cells[column_index].content.value, reverse=not self.data_table.sort_ascending)
        self.data_table.update()


    def criar_data_table(self, ref=None):
        # Cria a tabela com as colunas e as funções dos checkboxes
        self.data_table = ft.DataTable(
            data_row_max_height=25,
            border=ft.border.all(2, "red"),
            border_radius=10,
            vertical_lines=ft.BorderSide(3, "blue"),
            horizontal_lines=ft.BorderSide(1, "green"),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.colors.BLACK12,
            heading_row_height=55,
            data_row_color={ft.ControlState.HOVERED: "0x30FF0000"},
            show_checkbox_column=False,  # Desabilitar o checkbox padrão
            divider_thickness=0,
            data_row_min_height=15,  # Ajuste da altura mínima das linhas
            columns=[
                ft.DataColumn(
                    ft.Checkbox(
                        value=False, on_change=self.toggle_all_checkboxes  # Checkbox no cabeçalho
                    ), on_sort=self.sort_column  # Permitir ordenação pelos checkboxes
                )
            ] + [ft.DataColumn(col.label, on_sort=self.sort_column) for col in self.colunas],  # Adiciona as colunas extras com suporte à ordenação
            rows=[
                ft.DataRow(
                    [
                        ft.DataCell(ft.Checkbox(value=False, on_change=lambda e, idx=i: self.checkbox_changed(e, idx))),
                    ] + row,  # Adiciona os checkboxes nas linhas
                )
                for i, row in enumerate(self.linhas)
            ]
        )
        return self.data_table  # Retorna a DataTable pronta

def main(page: ft.Page):
    page.theme_mode = "dark"  # Define o tema como escuro
    page.window.center()  # Centraliza a janela na tela

    # Definindo colunas e linhas externas
    colunas_dos_itens_dos_pedidos = [
        ft.DataColumn(ft.Text("Coluna 1")),
        ft.DataColumn(ft.Text("Coluna 2"), numeric=True),
    ]
    
    linhas_dos_itens_dos_pedidos = [
        [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
        [ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))],
        [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
        [ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))],
        [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
        [ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))],
        [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
        [ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))],
        [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
        [ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))],
        [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
    ]

    # Instanciando a classe
    custom_table = CustomDataTable(colunas_dos_itens_dos_pedidos, linhas_dos_itens_dos_pedidos)
    
    # Adicionando a tabela pronta na página
    page.add(custom_table.criar_data_table())

ft.app(main)