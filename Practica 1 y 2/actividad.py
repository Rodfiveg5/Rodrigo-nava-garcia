import random
import tkinter as tk
from datetime import date, timedelta
from tkinter import messagebox, ttk


def generar_cita():
    dias = random.randint(1, 14)
    fecha = date.today() + timedelta(days=dias)
    ficha = random.randint(1, 50)
    return fecha.strftime("%d/%m/%Y"), ficha


def evaluar_datos(datos):
    oxigeno_bajo = datos["oxigeno"] < 90
    oxigeno_reducido = 90 <= datos["oxigeno"] < 95
    frecuencia_alta = datos["frecuencia"] > 100
    frecuencia_baja = datos["frecuencia"] < 60
    presion_alta = datos["presion"] >= 140
    presion_baja = datos["presion"] < 90
    fiebre = datos["fiebre"]
    tos = datos["tos"]
    dolor = datos["dolor"]
    dolor_cabeza = datos["dolorcabeza"]
    agotamiento = datos["agotamiento"]
    sintomas_respiratorios = fiebre and tos
    irritacion_respiratoria = tos and dolor
    alerta_vital = oxigeno_bajo or presion_alta or presion_baja
    frecuencia_anormal = frecuencia_alta or frecuencia_baja
    hallazgos = []

    if oxigeno_bajo:
        hallazgos.append(f"oxigeno bajo ({datos['oxigeno']:.0f}%)")
    elif oxigeno_reducido:
        hallazgos.append(f"oxigeno reducido ({datos['oxigeno']:.0f}%)")
    if frecuencia_alta:
        hallazgos.append(f"frecuencia cardiaca alta ({datos['frecuencia']:.0f} lpm)")
    elif frecuencia_baja:
        hallazgos.append(f"frecuencia cardiaca baja ({datos['frecuencia']:.0f} lpm)")
    if presion_alta:
        hallazgos.append(f"presion arterial alta ({datos['presion']:.0f} mmHg)")
    elif presion_baja:
        hallazgos.append(f"presion arterial baja ({datos['presion']:.0f} mmHg)")
    if fiebre:
        hallazgos.append("fiebre")
    if tos:
        hallazgos.append("tos")
    if dolor_cabeza:
        hallazgos.append("dolorcabeza")
    if agotamiento:
        hallazgos.append("agontamiento")
    if dolor:
        hallazgos.append("dolor de garganta")
    detalle = ", ".join(hallazgos) if hallazgos else "sin alteraciones detectadas"

    if oxigeno_bajo or (presion_alta and frecuencia_alta):
        diagnostico = f"Alerta medica por {detalle}. Requiere atencion inmediata."
        servicio = "Urgencias"
    elif sintomas_respiratorios and oxigeno_reducido:
        diagnostico = f"Posible infeccion respiratoria: {detalle}. Se recomienda valoracion."
        servicio = "Urgencias"
    elif sintomas_respiratorios:
        diagnostico = f"Posible infeccion respiratoria por {detalle}. Se sugieren estudios."
        servicio = "Estudios"
    elif irritacion_respiratoria:
        diagnostico = f"Posible irritacion respiratoria por {detalle}."
        servicio = "Farmacia"
    elif fiebre or tos or dolor or dolor_cabeza or agotamiento:
        diagnostico = f"Se detectaron sintomas: {detalle}. Se recomienda valoracion."
        servicio = "Estudios" if fiebre else "Farmacia"
    elif alerta_vital or frecuencia_anormal:
        diagnostico = f"Alteracion en signos vitales: {detalle}. Se recomienda valoracion profesional."
        servicio = "Estudios"
    else:
        diagnostico = "Estas muy sano. No se detectaron alteraciones."
        servicio = "Ninguno"

    return diagnostico, servicio


def validar_numero(valor, etiqueta, minimo):
    try:
        numero = float(valor)
    except ValueError as error:
        raise ValueError(f"{etiqueta} debe ser numerico.") from error
    if numero < minimo:
        raise ValueError(f"{etiqueta} debe ser mayor o igual a {minimo}.")
    return numero


def evaluar():
    try:
        nombre = nombre_var.get().strip()
        if not nombre:
            raise ValueError("Escribe el nombre del paciente.")

        edad = validar_numero(edad_var.get(), "La edad", 0)
        oxigeno = validar_numero(oxigeno_var.get(), "El oxigeno", 0)
        frecuencia = validar_numero(frecuencia_var.get(), "La frecuencia cardiaca", 0)
        presion = validar_numero(presion_var.get(), "La presion arterial", 0)
        peso = validar_numero(peso_var.get(), "El peso", 0.1)
        talla = validar_numero(talla_var.get(), "La talla", 0.1) / 100
        if talla <= 16:
            raise ValueError("La talla debe ser mayor que 16")

        datos = {
            "edad": edad,
            "oxigeno": oxigeno,
            "frecuencia": frecuencia,
            "presion": presion,
            "peso": peso,
            "talla": talla,
            "fiebre": fiebre_var.get(),
            "tos": tos_var.get(),
            "dolor": dolor_var.get(),
            "dolor_cabeza": dolorcab_var.get(),
            "agotamiento": agotamiento_var.get(),
            
        }
        diagnostico, servicio = evaluar_datos(datos)
        fecha, ficha = generar_cita()
        menu_var.set(servicio)
        resultado_var.set(
            f"Paciente: {nombre} | Edad: {edad:.0f} anos\n"
            f"Cita: {fecha} | Ficha: {ficha}\n"
            f"Resultado: {diagnostico}\n"
            f"Servicio sugerido: {servicio}"
        )
    except ValueError as error:
        messagebox.showerror("Datos invalidos", str(error))


def mostrar_servicio():
    servicio = menu_var.get()
    acciones = {
        "Urgencias": "Dirigirse a urgencias para valoracion prioritaria.",
        "Farmacia": "Consultar al personal de farmacia antes de tomar medicamentos.",
        "Estudios": "Solicitar estudios y llevar este resultado a valoracion profesional.",
        "Ninguno": "No necesitas acudir a un servicio. Continua cuidando tu salud.",
    }
    messagebox.showinfo(servicio, acciones[servicio])


# ==========================================================
# VENTANA Y PALETA DE COLORES (Blanco y Azul)
# ==========================================================
ventana = tk.Tk()
ventana.title("Sistema experto de diagnostico")
ventana.geometry("620x720")
ventana.resizable(False, False)
ventana.configure(bg="#ffffff")

COLOR_AZUL_PRINCIPAL = "#0052cc"
COLOR_AZUL_SUAVE = "#e9f2ff"
COLOR_TEXTO_OSCURO = "#172b4d"
COLOR_BLANCO = "#ffffff"

estilo = ttk.Style()
estilo.theme_use("clam")

# Configuración global de componentes ttk
estilo.configure(".", background=COLOR_BLANCO, foreground=COLOR_TEXTO_OSCURO)
estilo.configure("TFrame", background=COLOR_BLANCO)

estilo.configure(
    "Titulo.TLabel",
    font=("Segoe UI", 16, "bold"),
    foreground=COLOR_AZUL_PRINCIPAL,
    background=COLOR_BLANCO
)

estilo.configure(
    "TLabelframe",
    background=COLOR_BLANCO,
    foreground=COLOR_AZUL_PRINCIPAL,
    bordercolor="#c1c7d0",
    borderwidth=1,
    relief="solid"
)
estilo.configure(
    "TLabelframe.Label",
    font=("Segoe UI", 10, "bold"),
    foreground=COLOR_AZUL_PRINCIPAL,
    background=COLOR_BLANCO
)

estilo.configure(
    "TButton",
    font=("Segoe UI", 10, "bold"),
    background=COLOR_AZUL_PRINCIPAL,
    foreground=COLOR_BLANCO,
    borderwidth=0,
    padding=6
)
estilo.map("TButton", background=[("active", "#003d99")])

estilo.configure(
    "TCheckbutton",
    background=COLOR_BLANCO,
    font=("Segoe UI", 9)
)

estilo.configure(
    "TEntry",
    fieldbackground=COLOR_AZUL_SUAVE,
    foreground=COLOR_TEXTO_OSCURO,
    padding=3
)

# ==========================================================
# ESTRUCTURA DE LA INTERFAZ
# ==========================================================
contenedor = ttk.Frame(ventana, padding=20)
contenedor.pack(fill="both", expand=True)

ttk.Label(contenedor, text="Sistema experto de diagnostico", style="Titulo.TLabel").pack(pady=(0, 14))

# Datos del paciente
datos_frame = ttk.LabelFrame(contenedor, text=" Datos del paciente ", padding=12)
datos_frame.pack(fill="x")

nombre_var = tk.StringVar()
edad_var = tk.StringVar()
oxigeno_var = tk.StringVar()
frecuencia_var = tk.StringVar()
presion_var = tk.StringVar()
peso_var = tk.StringVar()
talla_var = tk.StringVar()

campos = [
    ("Nombre", nombre_var, 0),
    ("Edad", edad_var, 1),
    ("Oxigeno (%)", oxigeno_var, 2),
    ("Frecuencia cardiaca (lpm)", frecuencia_var, 3),
    ("Presion arterial (mmHg)", presion_var, 4),
    ("Peso (kg)", peso_var, 5),
    ("Talla (cm)", talla_var, 6),
]

for etiqueta, variable, fila in campos:
    ttk.Label(datos_frame, text=etiqueta).grid(row=fila, column=0, sticky="w", padx=(0, 10), pady=4)
    ttk.Entry(datos_frame, textvariable=variable, width=34).grid(row=fila, column=1, sticky="ew", pady=4)

datos_frame.columnconfigure(1, weight=1)

# Síntomas
sintomas_frame = ttk.LabelFrame(contenedor, text=" Sintomas ", padding=12)
sintomas_frame.pack(fill="x", pady=12)
fiebre_var = tk.BooleanVar()
tos_var = tk.BooleanVar()
dolor_var = tk.BooleanVar()
dolorcab_var = tk.BooleanVar()
agotamiento_var = tk.BooleanVar()
ttk.Checkbutton(sintomas_frame, text="Fiebre", variable=fiebre_var).pack(side="left", padx=12)
ttk.Checkbutton(sintomas_frame, text="Tos", variable=tos_var).pack(side="left", padx=12)
ttk.Checkbutton(sintomas_frame, text="Dolor de garganta", variable=dolor_var).pack(side="left", padx=12)
ttk.Checkbutton(sintomas_frame, text="Dolor de cabeza", variable=dolorcab_var).pack(side="left", padx=12)
ttk.Checkbutton(sintomas_frame, text="Agotamiento", variable=agotamiento_var).pack(side="left", padx=12)

# Botón principal
ttk.Button(contenedor, text="Evaluar y generar cita", command=evaluar).pack(fill="x", pady=(0, 12))

# Resultado
resultado_var = tk.StringVar(value="Completa los datos y presiona Evaluar.")
resultado_frame = ttk.LabelFrame(contenedor, text=" Resultado ", padding=12)
resultado_frame.pack(fill="x")
ttk.Label(resultado_frame, textvariable=resultado_var, justify="left", wraplength=550).pack(anchor="w")

# Menú de atención
menu_frame = ttk.LabelFrame(contenedor, text=" Menu de atencion ", padding=12)
menu_frame.pack(fill="x", pady=12)
menu_var = tk.StringVar(value="Ninguno")
ttk.Combobox(menu_frame, textvariable=menu_var, values=("Urgencias", "Farmacia", "Estudios", "Ninguno"), state="readonly", width=25).pack(side="left", padx=(0, 10))
ttk.Button(menu_frame, text="Ver indicacion", command=mostrar_servicio).pack(side="left")

ventana.mainloop()
