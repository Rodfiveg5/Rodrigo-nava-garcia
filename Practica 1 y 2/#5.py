print("================================================")
print("      Hola huesped tiene algun problema         ")
print("================================================")

print("Que problema se le presenta a continuación?")
electricidad = input("¿Tiene electricidad (s/n)").strip().lower() == "s"

if not electricidad:
    print("============Informe de diagnostico==============")
    print("Diagnostico: revisar alimentación.")
    
    Revision = input("¿Regreso la electricidad (s/n)").strip().lower() == "s"
    
    if not Revision:
        print("============Informe de diagnostico==============")
        print("Por favor llame a un tecnico para que revise la alimentación a este numero: 123-456-7890.") 
        
        tecnico = input("¿Tuvo atencion del tecnico (s/n)").strip().lower() == "s"
        if not tecnico:
            print("===========================================================")
            print("Un tecnico se presentara en su domicilio para revisar la alimentación el dia de mañana")
        else: 
            print("Perfecto, el tecnico se presentara para solucionar el problema.")      
        
else:
    print("Muy bien, el equipo esta funcionando correctamente.")
    
enciende = input("¿Enciende (s/n)").strip().lower() == "s"
if not enciende:
    print("============Informe de diagnostico==============")
    print("Diagnostico: revisar fuente de poder.")
    revision = input("¿Al revisarlo encendio (s/n)").strip().lower() == "s"
    if not revision:
        print("============Informe de diagnostico==============")
        print("Por favor llame a un tecnico para que revise la fuente de poder a este numero: 123-456-7890.") 
        
        tecnico = input("¿Tuvo atencion del tecnico (s/n)").strip().lower() == "s"
        if not tecnico:
            print("===========================================================")
            print("Un tecnico se presentara en su domicilio para revisar la fuente de poder el dia de mañana")
        else: 
            print("Perfecto, el tecnico se presentara para solucionar el problema.")
else:
    print("Muy bien, el equipo esta funcionando correctamente.")
    
    
imagen = input("¿Muestra imagen (s/n)").strip().lower() == "s"
if not imagen:
    print("============Informe de diagnostico==============")
    print("Diagnostico: revisar monitoreo o memoria .")
    
    muestra= input("¿Al revisarlo muestra imagen (s/n)").strip().lower() == "s"
    if not muestra:
        print("============Informe de diagnostico==============")
        print("Por favor llame a un tecnico para que revise el monitoreo o memoria a este numero: 123-456-7890.") 
        
        tecnico = input("¿Tuvo atencion del tecnico (s/n)").strip().lower() == "s"
        if not tecnico:
            print("===========================================================")
            print("Un tecnico se presentara en su domicilio para revisar el monitoreo o memoria el dia de mañana")
        else: 
            print("Perfecto, el tecnico se presentara para solucionar el problema.")
    else:
        print("Muy bien, el equipo esta funcionando correctamente.")
else:
    print("Muy bien, el equipo esta funcionando correctamente.")
