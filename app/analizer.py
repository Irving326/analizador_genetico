from fastapi import APIRouter, FastAPI, File, UploadFile, HTTPException
import requests

# Crear el router para organizar las rutas 
router = APIRouter()

#Conectar a API medica para obtener informacion adicional sobre las variantes geneticas
def obtener_informacion(variantes):
    url = "https://myvariant.info/v1/variant/"
    variantes_anotadas = []


    for variante in variantes:
        chrom_clean = str(variante['chrom']).replace('chr', '')
        id_variante = f"chr{chrom_clean}:g.{variante['pos']}{variante['ref']}>{variante['alt']}"

        try:
            response = requests.get(url + id_variante)
            if response.status_code == 200:
                datos = response.json()
                
                # Valores por defecto si no se encuentra info específica
                relevancia = "Variante detectada sin información clínica"
                enfermedad = "Sin información de enfermedad asociada"

                if '_id' in datos:
                    if 'clinvar' in datos:
                        clinvar_data = datos['clinvar']
                        try:
                            # 1. Normalizar rcv a lista (puede venir como dict o list)
                            rcv_data = clinvar_data.get('rcv', [])
                            rcv_list = rcv_data if isinstance(rcv_data, list) else [rcv_data]

                            if rcv_list:
                                relevancia = rcv_list[0].get('clinical_significance', 'No especificada')
                                
                                # 2. Extraer enfermedad de 'conditions'
                                condiciones = rcv_list[0].get('conditions', {})
                                if isinstance(condiciones, list):
                                    enfermedad = condiciones[0].get('name', 'Enfermedad no especificada')
                                else:
                                    enfermedad = condiciones.get('name', 'Enfermedad no especificada')
                        except (KeyError, IndexError, TypeError):
                            relevancia = "Info clínica incompleta"
                    else:
                        relevancia = "Sin registros en ClinVar"

            
                    variante['relevancia'] = relevancia
                    variante['enfermedad'] = enfermedad
                    variantes_anotadas.append(variante) # Agregamos a la lista de éxito
                    
                else:
                    print(f"Variante {id_variante} no encontrada en myvariant.info.")
            else:

                print(f"Error {response.status_code} para {id_variante}")
        
        except Exception as e:
            print(f"Error crítico en consulta: {e}")
            
    return variantes_anotadas
            

#Endpoint usando @router.post para subir el archivo VCF

@router.post("/upload-vcf")

#Sube el archivo VCF al servidor y lo procesa
#Verifica que el archivo tenga la extensión .vcf, si no es así, devuelve un error 400
async def upload_vcf(file: UploadFile = File(...)):
    if not file.filename.endswith('.vcf'):
        raise HTTPException(status_code=400 , detail="Archivo no valido. Por favor sube un archivo VCF.")

#Lee el contenido del archivo VCF y lo procesa línea por línea
    contenido = await file.read()
    vcf_datos = contenido.decode('utf-8').splitlines()
    resultados_preliminares = []

    for linea in vcf_datos:
        if linea.startswith('#'):
            continue
        campos = linea.split('\t')
        if len(campos) < 5:
            continue
        if campos[4] == '.':
            continue

#Guardar la informacion del archivo VCF en un diccionario
        resultados_preliminares.append({
            'chrom': campos[0],
            'pos': campos[1],
            'id': campos[2],
            'ref': campos[3],
            'alt': campos[4]
        })


    #llamar a funcion de obtener informacion pasando resultados del VCF
    variantes_con_info = obtener_informacion(resultados_preliminares)
    
    return {"variantes": variantes_con_info}
