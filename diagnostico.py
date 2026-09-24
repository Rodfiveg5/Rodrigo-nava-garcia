import os
import random
import tkinter as tk
from datetime import date, datetime, timedelta
from pathlib import Path
from tkinter import messagebox, ttk
from urllib.parse import quote_plus

from dotenv import load_dotenv
from pymongo import MongoClient

# ==========================================================
# CONEXIÓN CON MONGODB ATLAS
# ==========================================================
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

user = os.getenv("Mongo_User")
password_env = os.getenv("Mongo_password")
cluster = os.getenv("Mongo_cluster")
database = os.getenv("Mongo_db")
colleccion_name = os.getenv("Mongo_colleccion")

if not all([user, password_env, cluster, database, colleccion_name]):
    raise ValueError(
        "Faltan variables en el archivo .env. "
        "Verifica Mongo_User, Mongo_password, Mongo_cluster, "
        "Mongo_db y Mongo_colleccion."
    )

password = quote_plus(password_env)
mongo_uri = f"mongodb+srv://{user}:{password}@{cluster}"

client = MongoClient(mongo_uri)
db = client[database]
coleccion = db[colleccion_name]

# ==========================================================
# VARIABLES GLOBALES PARA LA EVALUACIÓN
# ==========================================================
ultima_evaluacion = {
    "diagnostico": "",
    "servicio": "",
    "cita": ""
}

# ==========================================================
# FUNCIONES LÓGICAS Y DE BASE DE DATOS
# ==========================================================
def guardar_datos():
    """Guarda los datos actuales del paciente en MongoDB Atlas."""
    try:
        val_nombre = nombre_var.get().strip()
        val_edad = edad_var.get().strip()
        val_oxigeno = oxigeno_var.get().strip()
        val_frecuencia = frecuencia_var.get().strip()
        val_presion = presion_var.get().strip()
        val_peso = peso_var.get().strip()
        val_talla = talla_var.get().strip()

        if not val_nombre:
            messagebox.showwarning("Dato faltante", "Ingresa el nombre del paciente.")
            return

        if not val_edad:
            messagebox.showwarning("Dato faltante", "Ingresa la edad del paciente.")
            return

        if not val_oxigeno:
            messagebox.showwarning("Dato faltante", "Ingresa el nivel de oxígeno.")
            return

        if not ultima_evaluacion["diagnostico"]:
            messagebox.showwarning("Evaluación pendiente", "Primero realiza la evaluación del paciente.")
            return

        documento = {
            "nombre": val_nombre,
            "edad": int(val_edad) if val_edad else None,
            "oxigeno": float(val_oxigeno) if val_oxigeno else None,
            "frecuencia": float(val_frecuencia) if val_frecuencia else None,
            "presion": val_presion,
            "peso": float(val_peso) if val_peso else None,
            "talla": float(val_talla) if val_talla else None,
            "fiebre": fiebre_var.get(),
            "tos": tos_var.get(),
            "dolor": dolor_var.get(),
            "dolor_cabeza": dolorcab_var.get(),
            "agotamiento": agotamiento_var.get(),
            "diagnostico": ultima_evaluacion["diagnostico"],
            "servicio": ultima_evaluacion["servicio"],
            "cita": ultima_evaluacion["cita"],
            "fecha_registro": datetime.now()
        }

        resultado = coleccion.insert_one(documento)
        messagebox.showinfo(
            "Guardado exitoso",
            f"Paciente guardado correctamente.\n\nID de MongoDB:\n{resultado.inserted_id}"
        )
    except ValueError:
        messagebox.showerror("Error", "Verifica que los datos numéricos sean correctos.")
    except Exception as e:
        messagebox.showerror("Error de MongoDB", f"No se pudo guardar el paciente.\n\n{e}")

def generar_cita():
    """Genera una fecha aleatoria para la cita entre 1 y 7 días."""
    dias = random.randint(1, 7)
    fecha_cita = date.today() + timedelta(days=dias)
    return fecha_cita.strftime("%d/%m/%Y")

def evaluar_datos(datos):
    oxigeno = datos["oxigeno"]
    frecuencia = datos["frecuencia"]
    presion = datos["presion"]

    fiebre = datos["fiebre"]
    tos = datos["tos"]
    dolor = datos["dolor"]
    dolor_cabeza = datos["dolor_cabeza"]
    agotamiento = datos["agotamiento"]

    # Evaluar parámetros vitales
    oxigeno_bajo = oxigeno < 90
    oxigeno_reducido = 90 <= oxigeno < 95

    frecuencia_alta = frecuencia > 100
    frecuencia_baja = frecuencia < 60

    presion_alta = presion >= 140
    presion_baja = presion < 90

    # Sintomatología
    sintomas_respiratorios = fiebre and tos
    irritacion_respiratoria = tos and dolor
    hay_sintomas = fiebre or tos or dolor or dolor_cabeza or agotamiento

    alerta_medica = oxigeno_bajo or presion_alta or presion_baja
    frecuencia_anormal = frecuencia_alta or frecuencia_baja

    # Diagnóstico y servicio
    if alerta_medica or (presion_alta and frecuencia_alta):
        diagnostico = "Alerta medica: se detectaron signos que requieren atención."
        servicio = "Urgencias"
    elif sintomas_respiratorios and oxigeno_reducido:
        diagnostico = "Posible infección respiratoria con oxígeno reducido."
        servicio = "Urgencias"
    elif sintomas_respiratorios:
        diagnostico = "Posibles síntomas de infección respiratoria."
        servicio = "Estudios"
    elif irritacion_respiratoria:
        diagnostico = "Posible irritación respiratoria."
        servicio = "Farmacia"
    elif hay_sintomas:
        diagnostico = "Se presentan síntomas que requieren valoración."
        servicio = "Estudios" if fiebre else "Farmacia"
    elif frecuencia_anormal:
        diagnostico = "Se detectó una frecuencia cardiaca fuera del rango establecido."
        servicio = "Estudios"
    else:
        diagnostico = "Estas muy sano. No se detectaron alteraciones importantes."
        servicio = "Ninguno"

    return diagnostico, servicio

def validar_numero(valor, nombre):
    try:
        return float(valor)
    except ValueError:
        messagebox.showerror("Error", f"El campo {nombre} debe contener un número válido.")
        return None

def evaluar():
    global ultima_evaluacion

    nombre = nombre_var.get().strip()
    if not nombre:
        messagebox.showwarning("Dato faltante", "Ingresa el nombre del paciente.")
        return

    edad = validar_numero(edad_var.get(), "Edad")
    if edad is None: return

    oxigeno = validar_numero(oxigeno_var.get(), "Oxígeno")
    if oxigeno is None: return

    frecuencia = validar_numero(frecuencia_var.get(), "Frecuencia cardiaca")
    if frecuencia is None: return

    presion = validar_numero(presion_var.get(), "Presión arterial")
    if presion is None: return

    peso = validar_numero(peso_var.get(), "Peso")
    if peso is None: return

    talla = validar_numero(talla_var.get(), "Talla")
    if talla is None: return

    talla = talla / 100
    if talla <= 0:
        messagebox.showerror("Error", "La talla debe ser mayor que cero.")
        return

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
        "agotamiento": agotamiento_var.get()
    }

    diagnostico, servicio = evaluar_datos(datos)
    cita = generar_cita()

    ultima_evaluacion = {
        "diagnostico": diagnostico,
        "servicio": servicio,
        "cita": cita
    }

    menu_var.set(servicio)
    resultado_var.set(
        f"Paciente: {nombre}\n\n"
        f"Edad: {int(edad)} años\n\n"
        f"Cita: {cita}\n\n"
        f"Resultado:\n{diagnostico}\n\n"
        f"Servicio recomendado:\n{servicio}"
    )

def mostrar_servicio():
    servicio = menu_var.get()
    if not servicio:
        messagebox.showwarning("Servicio", "Selecciona un servicio.")
        return

    indicaciones = {
        "Urgencias": "Acude a urgencias para recibir atención inmediata.",
        "Estudios": "Se recomienda realizar estudios y valoración médica.",
        "Farmacia": "Consulta al personal de farmacia para recibir orientación.",
        "Ninguno": "No se requiere un servicio adicional en esta evaluación."
    }

    mensaje = indicaciones.get(servicio, "No hay una indicación disponible.")
    messagebox.showinfo(f"Indicación - {servicio}", mensaje)

def consultar_pacientes():
    try:
        ventana_consulta = tk.Toplevel(ventana)
        ventana_consulta.title("Pacientes registrados")
        ventana_consulta.geometry("1100x600")
        ventana_consulta.configure(bg="white")

        titulo = tk.Label(
            ventana_consulta,
            text="Pacientes registrados en MongoDB",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#1E3A5F"
        )
        titulo.pack(pady=15)

        frame_tabla = tk.Frame(ventana_consulta, bg="white")
        frame_tabla.pack(fill="both", expand=True, padx=15, pady=10)

        columnas = ("id", "nombre", "edad", "oxigeno", "frecuencia", "presion", "servicio", "cita", "fecha")
        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

        tabla.heading("id", text="ID")
        tabla.heading("nombre", text="Nombre")
        tabla.heading("edad", text="Edad")
        tabla.heading("oxigeno", text="Oxígeno")
        tabla.heading("frecuencia", text="Frecuencia")
        tabla.heading("presion", text="Presión")
        tabla.heading("servicio", text="Servicio")
        tabla.heading("cita", text="Cita")
        tabla.heading("fecha", text="Fecha registro")

        tabla.column("id", width=90)
        tabla.column("nombre", width=150)
        tabla.column("edad", width=60)
        tabla.column("oxigeno", width=80)
        tabla.column("frecuencia", width=100)
        tabla.column("presion", width=80)
        tabla.column("servicio", width=100)
        tabla.column("cita", width=90)
        tabla.column("fecha", width=160)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tabla.pack(side="left", fill="both", expand=True)

        pacientes = coleccion.find().sort("fecha_registro", -1)

        for paciente in pacientes:
            fecha_registro = paciente.get("fecha_registro", "")
            if isinstance(fecha_registro, datetime):
                fecha_registro = fecha_registro.strftime("%d/%m/%Y %H:%M")

            tabla.insert(
                "",
                "end",
                values=(
                    str(paciente.get("_id", ""))[:12],
                    paciente.get("nombre", ""),
                    paciente.get("edad", ""),
                    paciente.get("oxigeno", ""),
                    paciente.get("frecuencia", ""),
                    paciente.get("presion", ""),
                    paciente.get("servicio", ""),
                    paciente.get("cita", ""),
                    fecha_registro
                )
            )

    except Exception as e:
        messagebox.showerror("Error de MongoDB", f"No se pudieron consultar los pacientes.\n\n{e}")

# ==========================================================
# VENTANA PRINCIPAL Y GUI
# ==========================================================
ventana = tk.Tk()
ventana.title("Sistema experto de diagnóstico")
ventana.geometry("620x720")
ventana.configure(bg="white")

# Variables de la interfaz
nombre_var = tk.StringVar()
edad_var = tk.StringVar()
oxigeno_var = tk.StringVar()
frecuencia_var = tk.StringVar()
presion_var = tk.StringVar()
peso_var = tk.StringVar()
talla_var = tk.StringVar()

fiebre_var = tk.BooleanVar()
tos_var = tk.BooleanVar()
dolor_var = tk.BooleanVar()
dolorcab_var = tk.BooleanVar()
agotamiento_var = tk.BooleanVar()

resultado_var = tk.StringVar()
menu_var = tk.StringVar()

# Título
tk.Label(
    ventana,
    text="Sistema experto de diagnóstico",
    font=("Arial", 22, "bold"),
    bg="white",
    fg="#1E3A5F"
).pack(pady=15)

# Frame Datos del Paciente
frame_datos = tk.LabelFrame(
    ventana, text="Datos del paciente", font=("Arial", 11, "bold"),
    bg="white", fg="#1E3A5F", padx=10, pady=10
)
frame_datos.pack(fill="x", padx=20, pady=5)

fields = [
    ("Nombre:", nombre_var),
    ("Edad:", edad_var),
    ("Oxígeno:", oxigeno_var),
    ("Frecuencia cardiaca:", frecuencia_var),
    ("Presión arterial:", presion_var),
    ("Peso:", peso_var),
    ("Talla (cm):", talla_var)
]

for i, (label_text, var) in enumerate(fields):
    tk.Label(frame_datos, text=label_text, bg="white").grid(row=i, column=0, sticky="w", pady=3)
    tk.Entry(frame_datos, textvariable=var, width=35).grid(row=i, column=1, pady=3)

# Frame Síntomas
frame_sintomas = tk.LabelFrame(
    ventana, text="Síntomas", font=("Arial", 11, "bold"),
    bg="white", fg="#1E3A5F", padx=10, pady=10
)
frame_sintomas.pack(fill="x", padx=20, pady=5)

tk.Checkbutton(frame_sintomas, text="Fiebre", variable=fiebre_var, bg="white").grid(row=0, column=0, sticky="w")
tk.Checkbutton(frame_sintomas, text="Tos", variable=tos_var, bg="white").grid(row=0, column=1, sticky="w")
tk.Checkbutton(frame_sintomas, text="Dolor de garganta", variable=dolor_var, bg="white").grid(row=1, column=0, sticky="w")
tk.Checkbutton(frame_sintomas, text="Dolor de cabeza", variable=dolorcab_var, bg="white").grid(row=1, column=1, sticky="w")
tk.Checkbutton(frame_sintomas, text="Agotamiento", variable=agotamiento_var, bg="white").grid(row=2, column=0, sticky="w")

# Botón Evaluar
boton_evaluar = tk.Button(
    ventana, text="Evaluar y generar cita", command=evaluar,
    bg="#1E88E5", fg="white", font=("Arial", 11, "bold"), width=30, pady=8
)
boton_evaluar.pack(pady=10)

# Frame Resultado
frame_resultado = tk.LabelFrame(
    ventana, text="Resultado", font=("Arial", 11, "bold"),
    bg="white", fg="#1E3A5F", padx=10, pady=10
)
frame_resultado.pack(fill="x", padx=20, pady=5)

label_resultado = tk.Label(
    frame_resultado, textvariable=resultado_var, bg="white",
    justify="left", anchor="w", font=("Arial", 10)
)
label_resultado.pack(fill="x")

# Frame Servicio
frame_servicio = tk.Frame(ventana, bg="white")
frame_servicio.pack(pady=10)

tk.Label(frame_servicio, text="Servicio:", bg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)

menu = ttk.Combobox(
    frame_servicio, textvariable=menu_var,
    values=["Urgencias", "Estudios", "Farmacia", "Ninguno"],
    state="readonly", width=20
)
menu.grid(row=0, column=1, padx=5)

boton_indicacion = tk.Button(
    frame_servicio, text="Ver indicación", command=mostrar_servicio,
    bg="#43A047", fg="white", font=("Arial", 10, "bold")
)
boton_indicacion.grid(row=0, column=2, padx=5)

# Frame MongoDB
frame_mongodb = tk.LabelFrame(
    ventana, text="Base de datos MongoDB", font=("Arial", 11, "bold"),
    bg="white", fg="#1E3A5F", padx=10, pady=10
)
frame_mongodb.pack(fill="x", padx=20, pady=5)

boton_guardar = tk.Button(
    frame_mongodb, text="Guardar paciente en MongoDB", command=guardar_datos,
    bg="#1565C0", fg="white", font=("Arial", 10, "bold"), width=30, pady=6
)
boton_guardar.grid(row=0, column=0, padx=5, pady=5)

boton_consultar = tk.Button(
    frame_mongodb, text="Consultar pacientes", command=consultar_pacientes,
    bg="#00897B", fg="white", font=("Arial", 10, "bold"), width=30, pady=6
)
boton_consultar.grid(row=1, column=0, padx=5, pady=5)

# Iniciar aplicación
ventana.mainloop()