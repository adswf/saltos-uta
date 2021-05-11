
import re
import os
import sys
import tkinter as tk
from tkinter import filedialog as fd

corte_en = 40
saltos_en = 30

###################################################################################

archivos = [obj.name for obj in os.scandir(os.getcwd()) if obj.is_file()]
txt = [e for e in archivos if e.endswith(".txt")]

######################################################################################


def cortar_lineas(linea, lista, corte_en):
    while len(linea) > corte_en:
        posicion = linea[:corte_en].rfind(" ")
        substring = linea[:posicion + 1]
        linea = linea[posicion + 1:]
        lista.append(substring)
    substring = linea
    lista.append(substring)


#   la lista de salida debe ser un lista-elemento de la lista final o auxiliar
#######################################################################################


def sumar_a_posiciones(i, posiciones, ocurrencias):
    for j in range(len(posiciones[i])):
        posiciones[i][j] = posiciones[i][j] + ocurrencias

####################################################################################


def reponer(i, linea, posiciones, retirado):
    for j in range(len(posiciones[i])):
        if j == 0:
            if linea[:posiciones[i][j]].count("あ") == 0:
                linea = linea[:posiciones[i][j]] + retirado[i][j] + linea[posiciones[i][j]:]
            elif linea[:posiciones[i][j]].count("あ") > 0:
                sumar_a_posiciones(i, posiciones, linea[:posiciones[i][j]].count("あ"))
        elif j > 0:
            if linea[posiciones[i][j]].count("あ") == 0:
                linea = linea[:posiciones[i][j]] + retirado[i][j] + linea[posiciones[i][j]:]
            elif linea[posiciones[i][j]].count("あ") > 0:
                sumar_a_posiciones(i, posiciones, linea[posiciones[i][j]].count("あ"))
                linea = linea[:posiciones[i][j]] + retirado[i][j] + linea[posiciones[i][j]:]
    return linea

##################################################################################################


def principal(entrada, salida, corte_en, saltos_en):
    try:
        original = open(entrada, "r", encoding="utf-8").read()
    except:
        print("Error: No se seleccionó ningún archivo válido")


    #   Archivo leido en formato string con n° líneas originales
    #######################################################################

    original = original.split("\n")
    lineas_original = len(original)

    original = "\n".join(original)

    #   Convertido a lista para ver cuantas lineas tiene originalmente
    #   y reconvertido a string
    #######################################################################

    original = original.replace("\\\\n \n", "あ")
    original = original.replace("\\\\n\n", "あ")
    original = original.replace("\\n", " ")
    original = original.replace("\\", "")

    #   Reemplazando todos los \\n + salto por あ y eliminando los \\n que
    #   estén en medio de las lineas

    #   Archivo en formato string donde toda la caja esta en una sola linea
    #   y las lineas anteriores estan unidas por una あ
    ########################################################################

    original = original.split("\n")

    #   Lista que contiene a todas las lineas anteriores como elementos
    #   número de elementos (lineas) menor al original
    #########################################################################

    auxiliar = []

    #   Lista de listas que nos servira de auxiliar
    #########################################################################

    #   Para cada elemento en original, si es que no tiene あ, agregar a la lista
    #   Si es que si tiene, agregar a la lista y agregar listas vacias cuantas
    #   veces あ tenga

    for elemento in original:
        ocurrencias1 = elemento.count("あ")
        auxiliar.append(elemento)
        if ocurrencias1 > 0:
            for ocurrencia in range(ocurrencias1):
                auxiliar.append("")

    #   Lista auxiliar donde tendremos por cada elemento una caja de texto llena
    #   y las lineas vacias como elementos
    #########################################################################################


    auxiliar2 = [[] for aux2 in range(len(auxiliar))]

    posiciones = [[] for z in range(len(auxiliar2))]
    retirado = [[] for z in range(len(auxiliar2))]

    for i in range(len(auxiliar)):
        elemento = auxiliar[i]
        ocurrencias2 = elemento.count("あ")
        if elemento.count("{W") == 0:
            if ocurrencias2 == 0:
                cortar_lineas(elemento, auxiliar2[i], corte_en)
            elif ocurrencias2 == 1:
                if elemento.find("あ") < saltos_en:
                    if len(elemento) <= corte_en:
                        auxiliar2[i].append(elemento)
                    elif len(elemento) >= corte_en:
                        primero = elemento[:elemento.find("あ")]
                        auxiliar2[i].append(primero)
                        resto = elemento[elemento.find("あ")+1:]
                        cortar_lineas(resto, auxiliar2[i], corte_en)
                elif elemento.find("あ") >= saltos_en:
                    elemento = elemento.replace("あ", " ")
                    cortar_lineas(elemento, auxiliar2[i], corte_en)
            elif ocurrencias2 > 1:
                if elemento.find("あ") < saltos_en:
                        primero = elemento[:elemento.find("あ")]
                        auxiliar2[i].append(primero)
                        resto = elemento[elemento.find("あ")+1:]
                        resto = resto.replace("あ", " ")
                        cortar_lineas(resto, auxiliar2[i], corte_en)
                elif elemento.find("あ") >= saltos_en:
                    elemento = elemento.replace("あ", " ")
                    cortar_lineas(elemento, auxiliar2[i], corte_en)
        elif elemento.count("{W") > 0:
            posiciones[i] = [z.start() for z in re.finditer("{W..}", elemento)]
            retirado[i] = [z for z in re.findall("{W..}", elemento)]
            elemento_sub = re.sub("{W..}", "", elemento)
            if len(elemento_sub) < corte_en:
                auxiliar2[i].append(elemento)
            elif len(elemento_sub) >= corte_en:
                ocurrencias2 = elemento_sub.count("あ")
                if ocurrencias2 == 0:
                    cortar_lineas(elemento_sub, auxiliar2[i], corte_en)
                    # obtener el resultado del corte
                    # lineas cortadas en una lista y luego unidas para que
                    # puedan regresarse lo retirado
                    # regresar_retirado(elemento_sub)
                    elemento_sub = "あ".join(auxiliar2[i])
                    resultado = reponer(i, elemento_sub, posiciones, retirado)
                    auxiliar2[i] = []
                    auxiliar2[i].append(resultado)
                elif ocurrencias2 == 1:
                    if elemento_sub.find("あ") < saltos_en:
                        if len(elemento_sub) <= corte_en:
                            auxiliar2[i].append(elemento)
                        elif len(elemento_sub) > corte_en:
                            primero = elemento_sub[:elemento_sub.find("あ")]
                            auxiliar2[i].append(primero)
                            resto = elemento[elemento_sub.find("あ") + 1:]
                            cortar_lineas(resto, auxiliar2[i], corte_en)
                            # regresar_retirado()
                            elemento_sub = "あ".join(auxiliar2[i])
                            resultado = reponer(i, elemento_sub, posiciones, retirado)
                            auxiliar2[i] = []
                            auxiliar2[i].append(resultado)
                            ################################
                    elif elemento.find("あ") >= saltos_en:
                        elemento = elemento.replace("あ", " ")
                        cortar_lineas(elemento, auxiliar2[i], corte_en)
                        # regresar_retirado()
                        elemento_sub = "あ".join(auxiliar2[i])
                        resultado = reponer(i, elemento_sub, posiciones, retirado)
                        auxiliar2[i] = []
                        auxiliar2[i].append(resultado)
                        ################################
                elif ocurrencias2 > 1:
                    if elemento_sub.find("あ") < saltos_en:
                        primero = elemento_sub[:elemento_sub.find("あ")]
                        auxiliar2[i].append(primero)
                        resto = elemento_sub[elemento_sub.find("あ") + 1:]
                        resto = resto.replace("あ", " ")
                        cortar_lineas(resto, auxiliar2[i], corte_en)
                        # regresar_retirado()
                        elemento_sub = "あ".join(auxiliar2[i])
                        resultado = reponer(i, elemento_sub, posiciones, retirado)
                        auxiliar2[i] = []
                        auxiliar2[i].append(resultado)
                        ################################
                    elif elemento.find("あ") >= saltos_en:
                        elemento = elemento.replace("あ", " ")
                        cortar_lineas(elemento, auxiliar2[i], corte_en)
                        # regresar_retirado()
                        elemento_sub = "あ".join(auxiliar2[i])
                        resultado = reponer(i, elemento_sub, posiciones, retirado)
                        auxiliar2[i] = []
                        auxiliar2[i].append(resultado)
                        ################################

    semifinal = [[] for k in range(len(auxiliar2))]

    for i in range(len(auxiliar2)):
        for e in auxiliar2[i]:
            if e.count("あ") > 0:
                e = e.replace("あ", "\\\\n")
                semifinal[i].append(e)
            else:
                e = e
                semifinal[i].append(e)
    final = []

    for i in range(len(semifinal)):
        shit = "\\\\n".join(semifinal[i])
        final.append(shit)

    #   Lista donde todos los elementos representan una linea en el archivo final
    #   Y una linea representa a una caja llena
    #######################################################################

    lineas_salida = len(final)
    print("Archivo actual: " + entrada + " - Líneas entrada: " + str(lineas_original) + " - Líneas salida: " + str(lineas_salida))

    final = "\n".join(final)

    try:
        os.makedirs("arreglados")
    except:
        pass

    if salida.count(":") == 0:
        f = open(".\\arreglados\\" + salida, "w", encoding="utf-8")
        f.write(final)
        f.close()
    else:
        salida = salida[salida.rfind("\\"):]
        f = open(os.getcwd() + "/arreglados/" + salida, "w", encoding="utf-8")
        f.write(final)
        f.close()


##################################################################################


if len(sys.argv) == 2:
    if sys.argv[1] == "*":
        for entrada in txt:
            principal(entrada, entrada, corte_en, saltos_en)
            print("Listo")
        print("Se arreglaron: " + str(len(txt)) + " archivos")
    else:
        principal(sys.argv[1], sys.argv[1], corte_en, saltos_en)
        print("Listo")


elif len(sys.argv) == 1:

    def get():
        corte_en = int(corte_en_entry.get())
        saltos_en = int(saltos_en_entry.get())

        entrada = fd.askopenfilename(title="Seleccionar un archivo:", filetypes=(("Archivos de texto", "*.txt"),
                                                                                 ("Todos los archivos", "*.*")))
        entrada = entrada[entrada.rfind("/") + 1:]
        if entrada != "":
            try:
                os.makedirs("arreglados")
            except:
                pass
            salida = fd.asksaveasfilename(defaultextension=".jpeg", title="Guardar archivo como:", initialfile=entrada,
                                          initialdir="arreglados",
                                          filetypes=(("Archivos txt", "*.txt"), ("Todos los archivos", "*.*")))
            if salida != "":
                salida = salida[salida.rfind("/") + 1:]
                principal(entrada, salida, corte_en, saltos_en)
                print("Listo.")
            else:
                print("Error: No se seleccionó una ubicación válida")
        else:
            print("Error: No se seleccionó un archivo válido")


    root = tk.Tk()
    root.title("angelord se la come 2021")
    # root.iconbitmap("icono.ico")
    root.configure(bg="white")

    # image = tk.PhotoImage(file="saltos")
    # image = image.subsample(3, 3)
    # label = tk.Label(image=image)
    # label.place(x=0, y=0, relwidth=1.0, relheight=1.0)

    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    positionRight = int(root.winfo_screenwidth() / 2.2 - windowWidth / 2)
    positionDown = int(root.winfo_screenheight() / 2.5 - windowHeight / 2)
    # root.geometry(f"340x450+{positionRight}+{positionDown}")
    root.geometry(f"340x400")

    corte_en_var = tk.IntVar(value=corte_en)
    saltos_en_var = tk.IntVar(value=saltos_en)

    etiqueta1 = tk.Label(root, text="Corte en:", bg="pink", fg="white")
    etiqueta2 = tk.Label(root, text="Ignorar primer salto\ncuando sea menor que:", bg="pink", fg="white")
    corte_en_entry = tk.Entry(root, textvariable=corte_en_var, font="Consolas 12")
    saltos_en_entry = tk.Entry(root, textvariable=saltos_en_var, font="Consolas 12")
    arreglar = tk.Button(root, text="Arreglar", width=20, height=2, bg="pink", fg="white",
                         font=("helvetica", 12, "bold"), command=get)

    etiqueta1.place(bordermode=tk.OUTSIDE,
                    x=90, y=120, width=70, height=30)
    corte_en_entry.place(bordermode=tk.OUTSIDE,
                    x=220, y=120, width=30, height=30)

    etiqueta2.place(bordermode=tk.OUTSIDE,
                    x=50, y=170, width=150, height=44)
    saltos_en_entry.place(bordermode=tk.OUTSIDE,
                    x=220, y=176, width=30, height=30)

    arreglar.place(bordermode=tk.OUTSIDE,
                    x=20, y=270, width=300, height=50)

    root.mainloop()


else: # len(sys.argv) >= 3
    args = sys.argv[1:]
    for arg in args:
        principal(arg, arg, corte_en, saltos_en)
        print("Listo")
    print("Se arreglaron: " + str(len(args)) + " archivos")


