import flet as ft
import re
#Cria o app
def main(page: ft.Page):          
    page.bgcolor = ft.colors.WHITE

#Título da página 
    page.title = 'Genetic Helper'
    
#Título com a caixa azul, em negrito
    page.add(
        ft.Container(ft.Text(value='                  VNTR \nUniversidade de Brasília - UnB', size=80, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),bgcolor = ft.colors.BLUE_200,  alignment=ft.alignment.center)
    )

#Inputs para os primers foward, reverse e resultado  
    primer_foward = ft.TextField(
        label='Primer foward', 
        text_size=45,
        label_style=ft.TextStyle(size=45)
        )

    primer_reverse = ft.TextField(
        label='Primer reverse', 
        text_size=45,
        label_style=ft.TextStyle(size=45)
        )
    
    sequencia = ft.TextField(
        label='Sequência', 
        text_size=45,
        label_style=ft.TextStyle(size=45)
        )
    qt_bases = ft.TextField(value= "")

#Select box para os alelos
    select_box = ft.Dropdown(
                label="",
                options=[
                    ft.dropdown.Option(key = 1, text ="maior que"),
                    ft.dropdown.Option(key = 2, text ="menor que"),
                    ft.dropdown.Option(key = 3, text ="igual a"),
                    ft.dropdown.Option(key = 4, text ="entre")
                    ]
                )
    alelo_result = ft.TextField(value= "")

#Posicionar a frase na mesma linha para identificação dos alelos
    alelo = ft.Row(
        controls= [
            ft.Text(value= "Caso o valor de pares de base"),
            qt_bases,
            ft.Text(value= "pares de base"),
            select_box,
            ft.Text(value= "então o alelo será"),
            alelo_result,
        ]
    )    
    page.add(primer_foward, primer_reverse, sequencia, alelo)             

#Lógica
    def analisar(e):
#Puxa as informações dos alelos
        qt_bases_valor = qt_bases.value
        select_box_valor = select_box.value
        alelo_result_valor = alelo_result.value

#Puxa os valores dos imputs do primer foward e reverse
        primer_foward_cru = primer_foward.value.upper()
        primer_reverse_cru = primer_reverse.value.upper()

#Faz o primer reverse virar fita complementar
        seq_substituida = ""
        for conjunto in primer_reverse_cru:
             conjunto_substituido = conjunto.replace("A", "B").replace("T", "V").replace("C", "D").replace("G", "H")
             for nucleotideo in conjunto_substituido:
                    conjunto_substituido2 = nucleotideo.replace("B", "T").replace("V", "A").replace("D", "G").replace("H", "C")
                    seq_substituida += conjunto_substituido2
        seq_invertida = seq_substituida[::-1]

#Puxa a sequência do imput retirando os espaços e etc
        seq_busca = sequencia.value.replace(" ", "").upper()
        seq_busca = re.sub(r'\s+', '', seq_busca)
        seq_busca = re.sub(r'\d', '', seq_busca)
        seq_busca = re.sub(r'\n', '', seq_busca)

#Procura o texto
        if primer_foward_cru and seq_invertida in seq_busca:
            pos_foward = seq_busca.find(primer_foward_cru)
            fragmento_1 = seq_busca[:pos_foward]
            fragmento_primer_foward = primer_foward_cru
            pos_reverse = seq_busca.find(seq_invertida, pos_foward + 1)
            fragmento_2 = seq_busca[pos_foward + len(primer_foward_cru):pos_reverse]
            pares_de_base = str(len(fragmento_2) + len(primer_foward_cru) + len(seq_invertida))
            inf_alelo = "\nForam encontrados " + pares_de_base + " pares de base na sequência"
            fragmento_primer_reverse = seq_invertida
            fragmento_3 = seq_busca[pos_reverse+len(seq_invertida):]

        if primer_foward_cru in seq_busca and seq_invertida not in seq_busca:
            pos_foward = seq_busca.find(primer_foward_cru)
            fragmento_1 = seq_busca[:pos_foward]
            fragmento_primer_foward = primer_foward_cru
            fragmento_2 = seq_busca[pos_foward + len(primer_foward_cru):]
            fragmento_primer_reverse = ''
            fragmento_3 =''
            inf_alelo = "\nApenas o primer foward foi encontrado"  

        if primer_foward_cru not in seq_busca and seq_invertida in seq_busca:
            pos_reverse = seq_busca.find(seq_invertida)
            fragmento_1 = seq_busca[:pos_reverse]
            fragmento_primer_reverse = seq_invertida
            fragmento_3 = seq_busca[pos_reverse + len(seq_invertida):]
            fragmento_primer_foward = ''
            fragmento_2 =''
            inf_alelo = "\nApenas o primer reverse foi encontrado" 

#Adiciona o texto com formatação mista
        resultado = ft.Text(spans = [
            ft.TextSpan(text=fragmento_1),
            ft.TextSpan(text=fragmento_primer_foward, style=ft.TextStyle(color=ft.colors.BLUE)),
            ft.TextSpan(text=fragmento_2),
            ft.TextSpan(text=fragmento_primer_reverse, style=ft.TextStyle(color=ft.colors.BLUE)),
            ft.TextSpan(text=fragmento_3),
            ft.TextSpan(text=inf_alelo)
            ],
        )            
        
        page.add(
        resultado,
        )

        page.update()
        
#Habilita a barra de rolagem
    page.scroll = "always"
    
#Botão
    page.add(
        ft.ElevatedButton(text='Localizar', on_click=analisar)
    )

    
#Faz com que as alterações sejam lançadas
    page.update()
#Roda o app
ft.app(target=main)
