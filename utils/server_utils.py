import random


def create_variables_to_test(myobj, idx):
    G1BG1 = myobj.add_variable(idx, "G1BG1", False)
    G1BG2 = myobj.add_variable(idx, "G1BG2", False)
    G1BG3 = myobj.add_variable(idx, "G1BG3", False)
    C2GB1 = myobj.add_variable(idx, "C2GB1", False)
    C2GB2 = myobj.add_variable(idx, "C2GB2", False)
    C2GB3 = myobj.add_variable(idx, "C2GB3", False)
    B_START = myobj.add_variable(idx, "B_START", False)
    B_STOP = myobj.add_variable(idx, "B_STOP", False)
    CHAVE_AM = myobj.add_variable(idx, "CHAVE_AM", False)
    B_RESET = myobj.add_variable(idx, "B_RESET", False)
    B_I4 = myobj.add_variable(idx, "B_I4", False)
    B_I5 = myobj.add_variable(idx, "B_I5", False)
    B_I6 = myobj.add_variable(idx, "B_I6", False)
    B_I7 = myobj.add_variable(idx, "B_I7", False)
    G1 = myobj.add_variable(idx, "G1", False)
    G2 = myobj.add_variable(idx, "G2", False)
    G3 = myobj.add_variable(idx, "G3", False)
    C1 = myobj.add_variable(idx, "C1", False)
    LED_START = myobj.add_variable(idx, "LED_START", False)
    LED_RESET = myobj.add_variable(idx, "LED_RESET", False)
    LUZ_Q1 = myobj.add_variable(idx, "LUZ_Q1", False)
    LUZ_Q2 = myobj.add_variable(idx, "LUZ_Q2", False)
    M_START = myobj.add_variable(idx, "M_START", False)
    M_STOP = myobj.add_variable(idx, "M_STOP", False)
    M_RESET = myobj.add_variable(idx, "M_RESET", False)
    M_STATUS = myobj.add_variable(idx, "M_STATUS", False)

    G1BG1.set_writable()
    G1BG2.set_writable()
    G1BG3.set_writable()
    C2GB1.set_writable()
    C2GB2.set_writable()
    C2GB3.set_writable()
    B_START.set_writable()
    B_STOP.set_writable()
    CHAVE_AM.set_writable()
    B_RESET.set_writable()
    B_I4.set_writable()
    B_I5.set_writable()
    B_I6.set_writable()
    B_I7.set_writable()
    G1.set_writable()
    G2.set_writable()
    G3.set_writable()
    C1.set_writable()
    LED_START.set_writable()
    LED_RESET.set_writable()
    LUZ_Q1.set_writable()
    LUZ_Q2.set_writable()
    M_START.set_writable()
    M_STOP.set_writable()
    M_RESET.set_writable()
    M_STATUS.set_writable()

    return [
        M_STOP,
        G1BG1,
        G1BG2,
        G1BG3,
        C2GB1,
        C2GB2,
        C2GB3,
        B_START,
        B_STOP,
        CHAVE_AM,
        B_RESET,
        B_I4,
        B_I5,
        B_I6,
        B_I7,
        G1,
        G2,
        G3,
        C1,
        LED_START,
        LED_RESET,
        LUZ_Q1,
        LUZ_Q2,
        M_START,
        M_RESET,
        M_STATUS]

def update_values(lista):
    lista2 = []
    dict1 = {}
    
    for i in lista:
        x = i.get_browse_name().Name
        x = x + "_value"
        lista2.append(x)
    
    for i in lista2:
        dict1[i] = random.randint(0 ,1)

    for key, value in dict1.items():
        for item in lista:
            if item.get_browse_name().Name in key:
                item.set_value(value)
                if item.get_browse_name().Name == "M_STOP":
                    item.set_value(False)