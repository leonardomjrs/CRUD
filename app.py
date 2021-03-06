from turtle import update
from flask import Flask
from flask import render_template , request , redirect
from flaskext.mysql import MySQL
from datetime import datetime
import os

app= Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema22072'
mysql.init_app(app)

CARPETA = os.path.join('uploads')
app.config['CARPETA']=CARPETA

@app.route('/')
def func():
    sql="SELECT * FROM `EMPLEADOS`;"
    conn=mysql.connect() #abrir conexion con objeto sql
    cursor=conn.cursor() #llevar la sentencia sql (line 17) y llevarla a la DB
    cursor.execute(sql) #ejecutar la consulta line17
    empleados = cursor.fetchall()
    print(empleados)
    conn.commit() #mandar la consulta
    return render_template('empleados/index.html' , empleados = empleados)

@app.route("/destroy/<int:id>")
def destroy(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    
    cursor.execute("SELECT foto from empleados WHERE id = %s", id)   
    fila = cursor.fetchall() 
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0])) 
        
    cursor.execute("DELETE FROM empleados WHERE id=%s", id)
    conn.commit()
    return redirect('/')
    
@app.route("/edit/<int:id>")
def edit(id):
    conn=mysql.connect() 
    cursor=conn.cursor() 
    cursor.execute("SELECT * FROM empleados WHERE id=%s", id) 
    empleados = cursor.fetchall()
    print(empleados)
    conn.commit() 
    return render_template('empleados/edit.html' , empleados = empleados)
    
@app.route("/update" , methods=['POST'])
def update():
    _id = request.form['txtId']
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    sql= "UPDATE empleados SET nombre = %s , correo = %s WHERE id = %s;"
    datos = (_nombre, _correo, _id)
    conn=mysql.connect() 
    cursor=conn.cursor() 
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    
    if _foto.filename != '':
        nuevoNombreFoto= tiempo + _foto.filename
        _foto.save("uploads/"+nuevoNombreFoto) 
        
        cursor.execute("SELECT foto from empleados WHERE id = %s", _id)   
        fila = cursor.fetchall() 
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0])) 
        cursor.execute("UPDATE empleados SET foto = %s WHERE id = %s", (nuevoNombreFoto, _id))
    
    cursor.execute(sql,datos)
    conn.commit() 
    return redirect('/')
    
    
@app.route('/create') #enrutar al html
def create():
    return render_template('empleados/create.html')


@app.route("/store", methods=['POST']) #traer datos de create.html
def storage():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    
    if _foto.filename != '':
        nuevoNombreFoto= tiempo + _foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
    else:
        nuevoNombreFoto=''
    
    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    
    datos = (_nombre, _correo, nuevoNombreFoto)
    conn=mysql.connect() #abrir conexion con objeto sql
    cursor=conn.cursor() #llevar la sentencia sql (line 17) y llevarla a la DB
    cursor.execute(sql,datos) #ejecutar la consulta line17
    conn.commit() #mandar la consulta
    return redirect('/')














if __name__=='__main__':
    app.run(debug=True)