import requests
import json

def consultar_api():
    url = "https://myvariant.info/v1/variant/"
    
    # Definimos la variante: (cromosoma, posición, referencia, alteración)
    # Ejemplo real: Variante en el gen BRCA1
    variante_info = ("13", "32337213", "T", "A ")

    # Construcción correcta del ID HGVS: chr17:g.43045712G>A
    id_variante = f"chr{variante_info[0]}:g.{variante_info[1]}{variante_info[2]}>{variante_info[3]}"
    
    print(f"--- Consultando MyVariant.info para: {id_variante} ---\n")
    
    try:
        response = requests.get(url + id_variante)
        
        if response.status_code == 200:
            datos = response.json()
            response = requests.get(url + id_variante)
            # Imprimimos TODO el JSON de forma bonita (indentado)
            print("DATOS COMPLETOS RECIBIDOS:")
            print(json.dumps(datos, indent=4))
            
            print("\n" + "="*50 + "\n")
            
            # Ejemplo: Extraer específicamente los datos RCV de ClinVar
            if "clinvar" in datos and "rcv" in datos["clinvar"]:
                print("INFORMACIÓN CLÍNICA (RCV):")
                rcv_list = datos["clinvar"]["rcv"]
                
                # A veces RCV es un diccionario único o una lista
                if isinstance(rcv_list, dict): rcv_list = [rcv_list]
                
                for registro in rcv_list:
                    acc = registro.get("accession", "N/A")
                    sig = registro.get("clinical_significance", "N/A")
                    print(f"- Acceso: {acc} | Significancia: {sig}")
            else:
                print("No se encontró información de ClinVar/RCV para esta variante.")
                
        else:
            print(f"Error de API: Código {response.status_code}")
            print("Asegúrate de que el ID sea válido y la variante exista.")
            
    except Exception as e:
        print(f"Error crítico en la conexión: {e}")

if __name__ == "__main__":
    consultar_api()
