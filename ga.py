# IMPORTS
from flask import Flask,render_template,jsonify,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime
import sys
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:230204@localhost:5432/salvemos_bd"
db = SQLAlchemy(app)



# Usuario model
class Usuario(db.Model):
    __tablename__ = 'usuario'
    correo = db.Column(db.String(25), primary_key=True)
    nickname = db.Column(db.String(15), nullable=False)
    saldo = db.Column(db.Numeric(10, 2), nullable=False)

    def __init__(self,correo,nickname,saldo):
        self.correo = correo
        self.nickname = nickname
        self.saldo = saldo

    def serialize(self):
        return{
            'id': self.id,
            'correo': self.correo,
            'nickname' : self.nickname,
            'saldo' : self.saldo,
        }

# Comprador model
class Comprador(db.Model):
    __tablename__ = 'comprador'
    usuario_correo = db.Column(db.String(25), db.ForeignKey('usuario.correo'), primary_key=True)
    def __init__(self,usuario_correo):
        self.usuario_correo = usuario_correo
    
    def serialize(self):
        return{
            'usuario_correo' : self.usuario_correo,
        }    

# Vendedor model
class Vendedor(db.Model):
    __tablename__ = 'vendedor'
    usuario_correo = db.Column(db.String(25),db.ForeignKey('usuario.correo'),primary_key=True)
    nrocuenta = db.Column(db.String(25), primary_key=True)
    calificacion = db.Column(db.Integer, nullable=False)

    def __init__(self,usuario_correo,nrocuenta,calificacion):
        self.usuario_correo = usuario_correo
        self.nrocuenta = nrocuenta
        self.calificacion
    
    def serialize(self):
        return{
            'usuario_correo' : self.usuario_correo,
            'nrocuenta' : self.nrocuenta,
            'calificacion' : self.calificacion,
        }

# Compania model
class Compania(db.Model):
    __tablename__ = 'compania'
    nombre = db.Column(db.String(20), primary_key=True)
    ceo = db.Column(db.String(18), nullable=True)

    def __init__(self,nombre,ceo):
        self.nombre = nombre
        self.ceo = ceo
    def serialize(self):
        return{
            'nombre': self.nombre,
            'ceo' : self.ceo,
        }

# Cuenta model
class Cuenta(db.Model):
    __tablename__ = 'cuenta'
    correo = db.Column(db.String(25), primary_key=True)
    compania_nombre = db.Column(db.String(20), db.ForeignKey('compania.nombre'), primary_key=True)
    usuario_correo = db.Column(db.String(25), db.ForeignKey('usuario.correo'), nullable=False)
    contrasena = db.Column(db.String(12), nullable=False)

    def __init__(self,correo,compania_nombre,usuario_correo,contrasena):
        self.correo = correo
        self.compania_nombre = compania_nombre
        self.usuario_correo = usuario_correo
        self.contrasena = contrasena

    def serialize(self):
        return {
            'correo' : self.correo,
            'compania_nombre':self.compania_nombre,
            'usuario_correo' : self.usuario_correo,
            'constrasena' : self.constrasena
        }

# Juego model
class Juego(db.Model):
    __tablename__ = 'juego'
    nombre = db.Column(db.String(20), primary_key=True)
    categoria = db.Column(db.String(12), nullable=False)
    gama = db.Column(db.String(12), nullable=False)
    compania_nombre = db.Column(db.String(20), db.ForeignKey('compania.nombre'), nullable=False)

    def __init__(self,nombre,categoria,gama,compania_nombre):
        self.nombre = nombre
        self.categoria = categoria
        self.gama = gama
        self.compania_nombre = compania_nombre
    
    def serialize(self):
        return {
            'nombre':self.nombre,
            'categoria' :self.categoria,
            'gama' : self.gama,
            'compania_nombre' : self.compania_nombre,
        }

# Skin model
class Skin(db.Model):
    __tablename__ = 'skin'
    hash = db.Column(db.String(40), primary_key=True)
    juego_nombre = db.Column(db.String(20), db.ForeignKey('juego.nombre'), primary_key=True)
    cuenta_correo = db.Column(db.String(25), db.ForeignKey('cuenta.correo'), nullable=False)
    cuenta_compania_nombre = db.Column(db.String(20), db.ForeignKey('cuenta.compania_nombre'), nullable=False)
    nombre = db.Column(db.String(20), nullable=False)

    def __init__(self,hash,juego_nombre,cuenta_correo,cuenta_compania_nombre,nombre):
        self.hash = hash
        self.juego_nombre = juego_nombre
        self.cuenta_correo = cuenta_correo
        self.cuenta_compania_nombre = cuenta_compania_nombre
        self.nombre = nombre
    
    def serialize(self):
        return{
            'hash' : self.hash,
            'juego_nombre' : self.juego_nombre,
            'cuenta_correo' : self.cuenta_correo,
            'cuenta_compania_nombre' : self.cuenta_compania_nombre,
            'nombre' : self.nombre,
        }
        

# Post model
class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.String(40), primary_key=True)
    vendedor_correo = db.Column(db.String(25), db.ForeignKey('vendedor.usuario_correo'), primary_key=True)
    vendedor_nrocuenta = db.Column(db.String(25), db.ForeignKey('vendedor.nrocuenta'), primary_key=True)
    skin_hash = db.Column(db.String(40), db.ForeignKey('skin.hash'), nullable=False)
    fecha_publicacion = db.Column(db.DateTime, nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    juego_nombre = db.Column(db.String(20), db.ForeignKey('juego.nombre'), nullable=False)

    def __init__(self,post_id,vendedor_correo,vendedor_nrocuenta,skin_hash,fecha_publicacion,precio,juego_nombre):
        self.post_id = post_id
        self.vendedor_correo = vendedor_correo
        self.vendedor_nrocuenta = vendedor_nrocuenta
        self.skin_hash = skin_hash
        self.fecha_publicacion = fecha_publicacion
        self.precio = precio
        self.juego_nombre = juego_nombre

    def serialize(self):
        return {
            'post_id' : self.post_id,
            'vendedor_correo' : self.vendedor_correo,
            'vendedor_nrocuenta': self.vendedor_nrocuenta,
            'skin_hash' : self.skin_hash,
            'fecha_publicacion' : self.fecha_publicacion,
            'precio' : self.precio,
            'juego_nombre' : self.juego_nombre,
        }

# Transaccion model
class Transaccion(db.Model):
    __tablename__ = 'transaccion'
    post_id = db.Column(db.String(40), db.ForeignKey('post.post_id'), primary_key=True)
    vendedor_correo = db.Column(db.String(25), db.ForeignKey('post.vendedor_correo'), primary_key=True)
    vendedor_nrocuenta = db.Column(db.String(25), db.ForeignKey('post.vendedor_nrocuenta'), primary_key=True)
    comprador_correo = db.Column(db.String(25), db.ForeignKey('comprador.usuario_correo'), nullable=False)
    fecha_compra = db.Column(db.DateTime, nullable=False)

    def __init__(self,post_id,vendedor_correo,vendedor_nrocuenta,comprador_correo,fecha_compra):
        self.post_id = post_id
        self.vendedor_correo = vendedor_correo
        self.vendedor_nrocuenta = vendedor_nrocuenta
        self.comprador_correo = comprador_correo
        self.fecha_compra = fecha_compra

    def serialize(self):
        return {
            'post_id' : self.post_id,
            'vendedor_correo': self.vendedor_correo,
            'vendedor_nrocuenta' : self.vendedor_nrocuenta,
            'comprador_correo' : self.comprador_correo,
            'fecha_compra' : self.fecha_compra,
        }


with app.app_context():db.create_all()


@app.route('/register-user',methods=['POST'])
def register_user():
    try:
        correo  = request.form.get('correo')
        nickname = request.form.get('nickname')
        saldo = request.form.get('saldo')

        user = User(correo,nickname,saldo)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        print(sys.exc_info())
        db.session.rollback()
        return jsonify({'success':False,'message':str(e)}) #redirect a la pagina que quieras 
    finally:
        db.session.close()

@app.route('/show-users',methods=['GET'])
def show_user():
    try:
        users = Usuario.query.all()
        users_serialized = [user.serialize() for user in users]
        return jsonify({'success':True,"users":users_serialized}),200
    except Exception as e:
        return jsonify({"success":False,"error":str(e)})


@app.route('/register-comprador',methods=['POST'])
def register_comprador():
    try:
        usuario_correo =  request.form.get('usuario_correo')
        comprador = Comprador(usuario_correo)
        db.session.add(comprador)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False,'message':str(e)})
    finally:
        db.session.close()

@app.route('/show-compradores')
def show_compradores():
    try:
        compradores = Comprador.query.all()
        comprador_serialize = [comprador.serialize() for comprador in compradores]
        return jsonify({'success':True,"comprador":comprador_serialize}),200
    except Exception as e:
        return jsonify({"success":False,"error":str(e)})


@app.route('/register-vendedor',methods=['POST'])
def register_vendedor():
    try:
        usuario_correo  = request.form.get('usuario_correo')
        nrocuenta = request.form.get('nrocuenta')
        calificacion = request.form.get('calificacion')

        vendedor = Vendedor(usuario_correo,nrocuenta,calificacion)
        db.session.add(vendedor)
        db.session.commit()
    except Exception as e:
        print(e)
        print(sys.exc_info())
        db.session.rollback()
        return jsonify({'success':False,'message':str(e)}) #redirect a la pagina que quieras 
    finally:
        db.session.close()

@app.route('/show-vendedores',methods=['GET'])
def show_vendedor():
    try:
        vendedores = Vendedor.query.all()
        vendedores_serialized = [vendedor.serialize() for vendedor in vendedores]
        return jsonify({'success':True,"vendedores":vendedores_serialized}),200
    except Exception as e:
        return jsonify({"success":False,"error":str(e)})


@app.route('/register-compania',methods=['POST'])
def register_compania():
    try:
        nombre  = request.form.get('nombre')
        ceo = request.form.get('ceo')

        compania = Compania(nombre,ceo)
        db.session.add(compania)
        db.session.commit()
    except Exception as e:
        print(e)
        print(sys.exc_info())
        db.session.rollback()
        return jsonify({'success':False,'message':str(e)}) #redirect a la pagina que quieras 
    finally:
        db.session.close()

@app.route('/show-companias',methods=['GET'])
def show_compania():
    try:
        companiaes = Compania.query.all()
        companiaes_serialized = [compania.serialize() for compania in companiaes]
        return jsonify({'success':True,"companiaes":vendedores_serialized}),200
    except Exception as e:
        return jsonify({"success":False,"error":str(e)})


@app.route('/register-cuenta',methods=['POST'])
def register_cuenta():
    try:
        correo  = request.form.get('correo')
        compania_nombre = request.form.get('compania_nombre')
        usuario_correo = request.form.get('usuario_correo')
        contrasena = request.form.get('contrasena')
    

        cuenta = Cuenta(correo,compania_nombre,contrasena,contrasena)
        db.session.add(cuenta)
        db.session.commit()
    except Exception as e:
        print(e)
        print(sys.exc_info())
        db.session.rollback()
        return jsonify({'success':False,'message':str(e)}) #redirect a la pagina que quieras 
    finally:
        db.session.close()

@app.route('/show-cuentas',methods=['GET'])
def show_cuenta():
    try:
        cuentas = Cuenta.query.all()
        cuentas_serialized = [cuenta.serialize() for cuenta in cuentas]
        return jsonify({'success':True,"cuentas":cuentas_serialized}),200
    except Exception as e:
        return jsonify({"success":False,"error":str(e)})


@app.route('/register-juego',methods=['POST'])
def register_juego():
    try:
        nombre  = request.form.get('nombre')
        categoria = request.form.get('categoria')
        gama = request.form.get('gama')
        compania_nombre = request.form.get('compania_nombre')

        juego = Juego(nombre,categoria,gama,compania_nombre)
        db.session.add(juego)
        db.session.commit()
    except Exception as e:
        print(e)
        print(sys.exc_info())
        db.session.rollback()
        return jsonify({'success':False,'message':str(e)}) #redirect a la pagina que quieras 
    finally:
        db.session.close()

@app.route('/show-juegos',methods=['GET'])
def show_juego():
    try:
        juegos = Juego.query.all()
        juegos_serialized = [juego.serialize() for juego in juegos]
        return jsonify({'success':True,"juegos":juegos_serialized}),200
    except Exception as e:
        return jsonify({"success":False,"error":str(e)})


@app.route('/register-skin',methods=['POST'])
def register_skin():
    try:
        hash  = request.form.get('hash')
        juego_nombre = request.form.get('juego_nombre')
        cuenta_correo = request.form.get('cuenta_correo')
        cuenta_compania_nombre = request.form.get('cuenta_compania_nombre')
        nombre = request.form.get('nombre')

        skin = Skin(hash,juego_nombre,cuenta_correo,cuenta_compania_nombre,nombre)
        db.session.add(skin)
        db.session.commit()
    except Exception as e:
        print(e)
        print(sys.exc_info())
        db.session.rollback()
        return jsonify({'success':False,'message':str(e)}) #redirect a la pagina que quieras 
    finally:
        db.session.close()

@app.route('/show-skins',methods=['GET'])
def show_skin():
    try:
        skins = Skin.query.all()
        skins_serialized = [skin.serialize() for skin in skins]
        return jsonify({'success':True,"skins":skins_serialized}),200
    except Exception as e:
        return jsonify({"success":False,"error":str(e)})

@app.route('/register-post',methods=['POST'])
def register_post():
    try:
        post_id  = request.form.get('post_id')
        vendedor_correo = request.form.get('vendedor_correo')
        vendedor_nrocuenta = request.form.get('vendedor_nrocuenta')
        skin_hash = request.form.get('skin_hash')
        fecha_publicacion = request.form.get('fecha_publicacion')
        precio = request.form.get('precio')        
        juego_nombre = request.form.get('juego_nombre')        


        post = Post(post_id,vendedor_correo,vendedor_nrocuenta,skin_hash,fecha_publicacion,precio,juego_nombre)
        db.session.add(post)
        db.session.commit()
    except Exception as e:
        print(e)
        print(sys.exc_info())
        db.session.rollback()
        return jsonify({'success':False,'message':str(e)}) #redirect a la pagina que quieras 
    finally:
        db.session.close()

@app.route('/show-posts',methods=['GET'])
def show_post():
    try:
        posts = Post.query.all()
        posts_serialized = [post.serialize() for post in posts]
        return jsonify({'success':True,"posts":posts_serialized}),200
    except Exception as e:
        return jsonify({"success":False,"error":str(e)})


@app.route('/register-transaccion',methods=['POST'])
def register_transaccion():
    try:
        post_id  = request.form.get('post_id')
        vendedor_correo = request.form.get('vendedor_correo')
        vendedor_nrocuenta = request.form.get('vendedor_nrocuenta')
        comprador_correo = request.form.get('comprador_correo')
        fecha_compra = request.form.get('fecha_compra')

        transaccion = Transaccion(post_id,vendedor_correo,vendedor_nrocuenta,comprador_correo,fecha_compra)
        db.session.add(transaccion)
        db.session.commit()
    except Exception as e:
        print(e)
        print(sys.exc_info())
        db.session.rollback()
        return jsonify({'success':False,'message':str(e)}) #redirect a la pagina que quieras 
    finally:
        db.session.close()

@app.route('/show-transaccions',methods=['GET'])
def show_transaccion():
    try:
        transaccions = Transaccion.query.all()
        transaccions_serialized = [transaccion.serialize() for transaccion in transaccions]
        return jsonify({'success':True,"transaccions":transaccions_serialized}),200
    except Exception as e:
        return jsonify({"success":False,"error":str(e)})


# CORRER LA APP
if __name__ == '__main__':
    app.run(debug=True)
else:
    print('Importing {}'.format(__name__))

