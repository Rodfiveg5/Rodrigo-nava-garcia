while True:

    Cantidad = int(input("Cuantas preposiciones quieres"))

    if Cantidad == 2:
        valores = [True, False]
        #Cuantas proporciciones quieres evaluar 
        print("P \t Q \t P ^ Q")
        print("-" * 80)
        for P in valores: 
            for Q in valores:
                resultado = P and Q 

                print(P, "\t", Q, "\t", resultado,"\t", )
    elif Cantidad == 3:
        valores = [True, False]
        print("P \t Q \t P ^ Q \t P ∨ Q ")
        print("-" * 80)
        for P in valores: 
            for Q in valores:
                for R in valores:
                    resultado = P and Q 
                    resultadoo = P or Q 

                    print(P, "\t", Q, "\t", R, "\t", resultado,"\t", resultadoo, "\t" )

    elif Cantidad == 4:
        valores = [True, False]
        print("P \t Q \t P ^ Q \t P ∨ Q \t  ¬P")
        print("-" * 80)
        for P in valores: 
            for Q in valores:
                for R in valores:
                    for S in valores:
                        resultado = P and Q 
                        resultadoo = P or Q 
                        Negativo = not P

                        print(P, "\t", Q, "\t", resultado,"\t", resultadoo, "\t", Negativo,  )

    elif Cantidad == 5:
        valores = [True, False]
        print("P \t Q \t P ^ Q \t P ∨ Q  \t ¬ P \t (NOT P) OR Q")
        print("-" * 80)
        for P in valores: 
            for Q in valores:
                for R in valores:
                    for S in valores:
                        for T in valores:
                            resultado = P and Q 
                            resultadoo = P or Q 
                            Negativo = not P
                            Condicional = (not P) or Q

                            print(P, "\t", Q, "\t", resultado,"\t", resultadoo, Negativo, "\t", Condicional, "\t" )
    elif Cantidad == 6:
        valores = [True, False]
        print("P \t Q \t P ^ Q \t P ∨ Q \t  ¬P \t P → Q \t P ↔ Q")
        print("-" * 80)
        for P in valores: 
            for Q in valores:
                for R in valores:
                    for S in valores:
                        for T in valores:
                            for U in valores:
                                resultado = P and Q 
                                resultadoo = P or Q 
                                Negativo = not P
                                Condicional = (not P) or Q
                                Bicondicional = P == Q

                                print(P, "\t", Q, "\t", resultado,"\t", resultadoo, Negativo, "\t", Condicional, "\t", Bicondicional )

    else: 
        print("==========================================================")
        print("Cantidad de preposiciones no soportadas, solo se soportan de 2 a 6")
        print("==========================================================")
        break
    #agregar OR, NOT, CONDICIONAL Y BICONDICIONAL    