import jwt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from GranProyecto.auth_backend import AuthBackend
from GranProyecto.validador import validador_contraseñas, validador_usuarios

app = FastAPI() # se encarga de escuchar las peticiones de internet
objeto_auth = AuthBackend()

SECRET_KEY = "Claude2026$%_proyecto_web"

class DatosUsuario(BaseModel):
    usuario: str
    password: str
    
def crear_token(usuario):
    payload = {"usuario": usuario}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

@app.get("/")
def inicio():
    return {"mensaje": "Mi backend está vivo 🚀"}

@app.post("/register")
def registro(datos: DatosUsuario):
    retorno_user = validador_usuarios(datos.usuario, objeto_auth.base_datos)
    retorno_passw = validador_contraseñas(datos.password)
    if retorno_user == True and retorno_passw == True:
        objeto_auth.registrar_usuario(datos.usuario, datos.password)
        objeto_auth.guardar_archivo()
        return {"mensaje": "Registrado con exito"}
    elif retorno_user != True and retorno_passw == True:
            raise HTTPException(status_code=400, detail=retorno_user)
    elif retorno_user == True and retorno_passw != True:
        raise HTTPException(status_code=400, detail=retorno_passw)
    else:
        raise HTTPException(status_code=400, detail=retorno_user + " y " + retorno_passw)

@app.post("/login")
def login(datos: DatosUsuario):
    retorno = objeto_auth.login_usuario(datos.usuario, datos.password)
    if retorno == True:
        token_generado = crear_token(datos.usuario)
        return {
            "mensaje": "Inicio exitoso",
            "token": token_generado,
            "token_type": "bearer"
        }
    else:
        raise HTTPException(status_code=400, detail=retorno)
    