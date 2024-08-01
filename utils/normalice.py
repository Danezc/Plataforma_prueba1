import re 

def normalize_module_name(module_name):
    # Convertir a minúsculas
    module_name = module_name.lower()
    # Eliminar tildes y caracteres especiales
    module_name = re.sub(r'[^\w\s]', '', module_name)
    # Reemplazar espacios por guiones bajos
    module_name = module_name.replace(' ', '_')
    return module_name