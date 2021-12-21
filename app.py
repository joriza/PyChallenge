from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

from config import config

app = Flask(__name__)

conexion = MySQL(app)


@app.route("/detalle")
def lista_datos():
    """Lista los datos cargados"""
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM datos"
        cursor.execute(sql)
        datos = cursor.fetchall()
        registros = []
        for fila in datos:
            row = {"id_emp": fila[0], "id_usu": fila[1], "cnt_ha": fila[2]}
            registros.append(row)
        return jsonify({"datos_registrados: ": registros})
    except Exception as ex:
        return jsonify({"Mensaje: ": "Error en lista_datos"})


@app.route("/registrar", methods=["POST"])
def registra_datos():
    """Agrega datos a la tablas datos"""
    try:
        req = request.json
        print("reg_dat: ", req)
        valUsuEmp = valida_usuario_empresa(req)
        print("Valor UsuEmp", valUsuEmp)
        if valUsuEmp:
            verifica_alta_empresa(req["id_emp"])
            verifica_alta_usuario(req)
            cursor = conexion.connection.cursor()
            sql = """INSERT INTO datos (id_emp, id_usu, cnt_ha)
                        VALUES ({0}, {1}, {2})""".format(
                request.json["id_emp"], request.json["id_usu"], request.json["cnt_ha"]
            )
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({"Mensaje: ": "Dato registrado"})
        else:
            return jsonify(
                {
                    "Mensaje: ": "Registro Inválido. Cada usuario debe pertenecer a una única Empresa"
                }
            )
    except:
        return jsonify({"Mensaje: ": "Error en registra_datos"})


@app.route("/balance1")
def balance1():
    """Emite Balance agrupado por Empresa"""
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id_emp, Sum(cnt_ha) AS cnt_ha FROM datos GROUP BY id_emp"
        cursor.execute(sql)
        datos = cursor.fetchall()
        registros = []
        for fila in datos:
            row = {"id_emp": fila[0], "cnt_ha": fila[1]}
            registros.append(row)
        return jsonify({"Balance_por_Empresa: ": registros})
    except Exception as ex:
        return jsonify({"Mensaje: ": "Error en balance2"})


@app.route("/balance2")
def balance2():
    """Emite Balance agrupado por Empresa y Usuario"""
    try:
        cursor = conexion.connection.cursor()
        sql = """SELECT id_emp, id_usu, Sum(cnt_ha) AS cnt_ha FROM datos
                    GROUP BY id_emp, id_usu"""
        cursor.execute(sql)
        datos = cursor.fetchall()
        registros = []
        for fila in datos:
            row = {"id_emp": fila[0], "id_usu": fila[1], "cnt_ha": fila[2]}
            registros.append(row)
        return jsonify({"Balance_por_Empresa_Usuario:": registros})
    except Exception as ex:
        return jsonify({"Mensaje: ": "Error en balance2"})


def pag_not_found(error):
    """Emite una respuesta cuando una URL solicitada no es válida"""
    return jsonify({"Mensaje: ": "URL no encontrada"}), 404


def verifica_alta_empresa(registro):
    """Verifica si la empresa de la consulta existe,
        sino, invoca a la funcion que da el alta a la tabla empresa
    """
    try:
        cursor = conexion.connection.cursor()
        print("id_empresa: ", registro)
        sql = "SELECT * FROM empresas WHERE id_emp = {0}".format(registro)
        print("sql:", sql)
        cursor.execute(sql)
        datos = cursor.fetchall()
        if len(datos) < 1:
            print("La empresa NO existe")
            realiza_alta_empresa(registro)
            return True
        else:
            print("datos:", len(datos))
            print("La empresa existe")
            return False
    except Exception as ex:
        return jsonify({"Mensaje: ": "Error en verifica_alta_empresa"})


def realiza_alta_empresa(registro):
    """Agrega Empresa de la consulta a la tabla empresas"""
    try:
        print("func: realiza_alta_empresa")
        cursor = conexion.connection.cursor()
        print("id_empresa: ", registro)
        sql = "INSERT INTO empresas ( id_emp) VALUES ( {0} )".format(registro)
        print("sql:", sql)
        cursor.execute(sql)
        conexion.connection.commit()
    except Exception as ex:
        return jsonify({"Mensaje: ": "Error en realiza_alta_empresa"})


def verifica_alta_usuario(registro):
    """Verifica si el usuario de la consulta existe,
        sino, invoca a la funcion que da el alta a la tabla usuarios
    """
    try:
        print("func: verifica_alta_usuario")
        cursor = conexion.connection.cursor()
        print("id_usuario: ", registro["id_usu"], type(registro["id_usu"]))
        sql = "SELECT * FROM usuarios WHERE id_usu = {0} and id_emp = {1}".format(
            registro["id_usu"], registro["id_emp"]
        )
        print("sql:", sql)
        cursor.execute(sql)
        datos = cursor.fetchall()
        if len(datos) < 1:
            print("el usuario NO existe")
            realiza_alta_usuario(registro)
            return True
        else:
            print("cnt_usu:", len(datos))
            print("El usuario existe")
            return False
    except Exception as ex:
        return jsonify({"Mensaje: ": "Error en verifica_alta_usuario"})


def realiza_alta_usuario(registro):
    """Agrega Usuario de la consulta a la tabla usuarios"""
    try:
        print("func: realiza_alta_usuario")
        cursor = conexion.connection.cursor()
        print("id_usuario: ", registro["id_usu"], type(registro["id_usu"]))
        sql = "INSERT INTO usuarios ( id_usu, id_emp) VALUES ( {0}, {1} )".format(
            registro["id_usu"], registro["id_emp"]
        )
        print("sql:", sql)
        cursor.execute(sql)
        conexion.connection.commit()
    except Exception as ex:
        return jsonify({"Mensaje: ": "Error en realiza_alta_usuario"})


def valida_usuario_empresa(registro):
    try:
        print("func: valida_usuario_empresa")
        print("Reg: usuEmp: ", registro["id_usu"], registro["id_emp"])
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM usuarios WHERE id_usu = {0} AND id_emp NOT IN ( {1} )".format(
            registro["id_usu"], registro["id_emp"]
        )
        print("sql:", sql)
        cursor.execute(sql)
        datos = cursor.fetchall()
        if len(datos) > 0:
            print("cant. UsuEmp:", len(datos))
            print("El usuario Pertenece a otra Empresa")
            return False
        else:
            print("el usuarioEmpresa es VALIDO")
            return True
    except Exception as ex:
        return jsonify({"Mensaje: ": "Error en valida_usuario_empresa"})


if __name__ == "__main__":
    app.config.from_object(config["development"])
    app.register_error_handler(404, pag_not_found)
    app.run()
