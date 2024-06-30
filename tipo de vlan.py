def verificacionvlan(vlan_id):
    if 1 <= vlan_id <= 1005:
        return "VLAN Rango Normal"
    elif 1006 <= vlan_id <= 4094:
        return "VLAN Rango Extendido"
    else:
        return "El número de VLAN no es válido"

try:
    vlan_id = int(input("Introduce el número de VLAN: "))
    print(verificar_vlan(vlan_id))
except ValueError:
    print("Por favor, introduce un número válido.")
