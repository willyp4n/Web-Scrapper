import yaml


__config = None


def config():
    global __config #para que la variable global la podamos utilizar dentro de nuestra función.
    if not __config:
        with open("config.yaml", mode="r") as f: # para abrir el archivo en modo lectura
            __config = yaml.safe_load(f) 
    
    return __config