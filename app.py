import os, sqlite3, random
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "eduplay.db")
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cambia-esta-clave-local")

LESSONS = {
 "lengua": {
  "title":"Lengua", "icon":"📚", "description":"Lee, comprende, escribe y comunica tus ideas.",
  "topics":[
   {"slug":"comprension-lectora","title":"Comprensión lectora","icon":"📖","level":"Básico",
    "intro":"Comprender un texto significa identificar lo que dice, reconocer sus ideas y explicar su significado con tus propias palabras.",
    "explanation":["Lee el texto completo una primera vez para conocer el tema.","En una segunda lectura identifica la idea principal y las ideas secundarias.","Relaciona la información con el título, el contexto y tus conocimientos."],
    "example":"Texto: “Las abejas visitan las flores y transportan polen. Gracias a este proceso muchas plantas pueden reproducirse.” Idea principal: las abejas ayudan a la reproducción de las plantas.",
    "question":"¿Qué idea expresa mejor el texto del ejemplo?","answers":["Las abejas ayudan a las plantas mediante la polinización.","Todas las flores son iguales.","Las abejas viven solamente en árboles."],"correct":0,
    "video":"https://www.youtube.com/results?search_query=comprension+lectora+explicacion+para+secundaria"},
   {"slug":"acentuacion","title":"Acentuación","icon":"✍️","level":"Básico",
    "intro":"La acentuación permite reconocer dónde recae la fuerza de voz de una palabra y cuándo debe escribirse tilde.",
    "explanation":["Agudas: la sílaba tónica es la última; llevan tilde si terminan en n, s o vocal.","Graves o llanas: la sílaba tónica es la penúltima; llevan tilde si NO terminan en n, s o vocal.","Esdrújulas: la sílaba tónica es la antepenúltima; siempre llevan tilde."],
    "example":"canción (aguda, termina en n); lápiz (grave, termina en z); música (esdrújula).",
    "question":"¿Cuál palabra es esdrújula?","answers":["reloj","música","papel"],"correct":1,
    "video":"https://www.youtube.com/results?search_query=reglas+de+acentuacion+agudas+graves+esdrujulas"},
   {"slug":"sujeto-y-predicado","title":"Sujeto y predicado","icon":"🧩","level":"Intermedio",
    "intro":"En una oración, el sujeto indica de quién o de qué se habla y el predicado expresa lo que hace o lo que se dice del sujeto.",
    "explanation":["Localiza el verbo conjugado de la oración.","Pregunta quién realiza la acción para encontrar el sujeto.","El predicado contiene el verbo y la información que se dice del sujeto."],
    "example":"“Los estudiantes preparan su proyecto”. Sujeto: “Los estudiantes”. Predicado: “preparan su proyecto”.",
    "question":"En “Mi hermana lee un libro”, ¿cuál es el sujeto?","answers":["lee un libro","Mi hermana","un libro"],"correct":1,
    "video":"https://www.youtube.com/results?search_query=sujeto+y+predicado+explicacion+ejemplos"},
   {"slug":"sinonimos-y-antonimos","title":"Sinónimos y antónimos","icon":"🔄","level":"Básico",
    "intro":"Los sinónimos tienen significados iguales o parecidos; los antónimos expresan significados opuestos.",
    "explanation":["Usa sinónimos para evitar repetir palabras y enriquecer tus textos.","Usa antónimos para expresar contraste.","El contexto ayuda a elegir la palabra adecuada."],
    "example":"Sinónimos: alegre / feliz. Antónimos: frío / caliente.",
    "question":"¿Cuál es un antónimo de “amplio”?","answers":["extenso","espacioso","estrecho"],"correct":2,
    "video":"https://www.youtube.com/results?search_query=sinonimos+y+antonimos+para+secundaria"}
  ]
 },
 "matematicas": {
  "title":"Matemáticas", "icon":"🔢", "description":"Comprende procedimientos y resuelve problemas paso a paso.",
  "topics":[
   {"slug":"operaciones-basicas","title":"Operaciones básicas","icon":"➕","level":"Básico",
    "intro":"Las operaciones básicas son suma, resta, multiplicación y división. Permiten resolver cálculos cotidianos.",
    "explanation":["Suma: reúne cantidades. Ejemplo: 8 + 5 = 13.","Resta: calcula la diferencia. Ejemplo: 12 − 7 = 5.","Multiplicación: suma repetida. Ejemplo: 4 × 3 = 12.","División: reparte en partes iguales. Ejemplo: 20 ÷ 4 = 5."],
    "example":"Si tienes 3 bolsas con 4 canicas cada una, calculas 3 × 4 = 12 canicas.",
    "question":"¿Cuánto es 9 × 6?","answers":["45","54","63"],"correct":1,
    "video":"https://www.youtube.com/results?search_query=operaciones+basicas+matematicas+explicacion"},
   {"slug":"fracciones","title":"Fracciones","icon":"🍕","level":"Básico",
    "intro":"Una fracción representa partes iguales de un todo. El numerador indica cuántas partes tomamos y el denominador en cuántas partes se dividió el todo.",
    "explanation":["El numerador se escribe arriba de la línea.","El denominador se escribe abajo y no puede ser cero.","Para sumar fracciones con el mismo denominador, suma numeradores y conserva el denominador."],
    "example":"2/5 + 1/5 = 3/5. Se suman 2 + 1 y se conserva el 5.",
    "question":"¿Cuánto es 1/4 + 2/4?","answers":["3/4","3/8","2/4"],"correct":0,
    "video":"https://www.youtube.com/results?search_query=fracciones+explicacion+ejercicios+secundaria"},
   {"slug":"porcentajes","title":"Porcentajes","icon":"％","level":"Intermedio",
    "intro":"Un porcentaje expresa una cantidad como parte de cien. El símbolo % significa “de cada 100”.",
    "explanation":["Convierte el porcentaje a decimal dividiéndolo entre 100.","Multiplica el decimal por la cantidad total.","También puedes calcular 10% dividiendo entre 10 y usarlo como referencia."],
    "example":"20% de 150 = 0.20 × 150 = 30.",
    "question":"¿Cuánto es el 10% de 80?","answers":["8","10","18"],"correct":0,
    "video":"https://www.youtube.com/results?search_query=porcentajes+como+calcular+ejemplos"},
   {"slug":"ecuaciones-lineales","title":"Ecuaciones lineales","icon":"📐","level":"Intermedio",
    "intro":"Una ecuación lineal es una igualdad que contiene una incógnita elevada a la primera potencia. Resolverla consiste en encontrar el valor que hace verdadera la igualdad.",
    "explanation":["Simplifica ambos lados si es necesario.","Agrupa los términos con x en un lado y los números en el otro.","Realiza la operación inversa para despejar x.","Comprueba sustituyendo el resultado en la ecuación original."],
    "example":"x + 5 = 12. Restamos 5 en ambos lados: x = 12 − 5, por lo tanto x = 7.",
    "question":"Si x − 4 = 9, ¿cuánto vale x?","answers":["5","13","36"],"correct":1,
    "video":"https://www.youtube.com/results?search_query=ecuaciones+lineales+paso+a+paso"},
   {"slug":"ecuaciones-cuadraticas","title":"Ecuaciones cuadráticas","icon":"📈","level":"Avanzado",
    "intro":"Una ecuación cuadrática tiene la forma ax² + bx + c = 0, con a distinto de cero. Puede resolverse por factorización o fórmula general.",
    "explanation":["Identifica los coeficientes a, b y c.","Sustituye en x = (−b ± √(b² − 4ac)) / 2a.","Calcula el discriminante b² − 4ac para conocer el tipo de soluciones.","Resuelve las dos posibilidades: una con + y otra con −."],
    "example":"x² − 5x + 6 = 0. Factorizamos: (x − 2)(x − 3) = 0. Las soluciones son x = 2 y x = 3.",
    "question":"En x² + 3x + 2 = 0, ¿cuál es el valor de a?","answers":["1","3","2"],"correct":0,
    "video":"https://www.youtube.com/results?search_query=ecuaciones+cuadraticas+formula+general+explicacion"},
   {"slug":"geometria","title":"Geometría: áreas","icon":"🔺","level":"Intermedio",
    "intro":"La geometría estudia las figuras y sus propiedades. El área mide la superficie que ocupa una figura plana.",
    "explanation":["Rectángulo: área = base × altura.","Triángulo: área = (base × altura) ÷ 2.","Cuadrado: área = lado × lado.","Escribe siempre las unidades cuadradas, por ejemplo cm²."],
    "example":"Triángulo con base 8 cm y altura 5 cm: (8 × 5) ÷ 2 = 20 cm².",
    "question":"¿Cuál es el área de un rectángulo de 6 cm por 4 cm?","answers":["10 cm²","20 cm²","24 cm²"],"correct":2,
    "video":"https://www.youtube.com/results?search_query=areas+figuras+geometricas+explicacion"}
  ]
 }
}

def db():
    con=sqlite3.connect(DB); con.row_factory=sqlite3.Row; return con
def init_db():
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS users(
          id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
          username TEXT UNIQUE NOT NULL, password TEXT NOT NULL,
          points INTEGER DEFAULT 0, completed INTEGER DEFAULT 0)""")
def logged(fn):
    @wraps(fn)
    def inner(*a,**k):
        if "uid" not in session:
            flash("Inicia sesión para entrar a esta sección.","warning")
            return redirect(url_for("login"))
        return fn(*a,**k)
    return inner

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/registro",methods=["GET","POST"])
def register():
    if request.method=="POST":
        name=request.form.get("name","").strip(); username=request.form.get("username","").strip()
        password=request.form.get("password","")
        if not name or not username or len(password)<6:
            flash("Completa los datos. La contraseña debe tener al menos 6 caracteres.","error")
        else:
            try:
                with db() as con:
                    con.execute("INSERT INTO users(name,username,password) VALUES(?,?,?)",(name,username,generate_password_hash(password)))
                flash("Cuenta creada. Ahora inicia sesión.","success"); return redirect(url_for("login"))
            except sqlite3.IntegrityError: flash("Ese usuario ya está registrado.","error")
    return render_template("register.html")
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        with db() as con: user=con.execute("SELECT * FROM users WHERE username=?",(request.form.get("username","").strip(),)).fetchone()
        if user and check_password_hash(user["password"],request.form.get("password","")):
            session.clear(); session["uid"]=user["id"]; session["name"]=user["name"]
            return redirect(url_for("dashboard"))
        flash("Usuario o contraseña incorrectos.","error")
    return render_template("login.html")
@app.route("/salir")
def logout():
    session.clear(); return redirect(url_for("home"))
@app.route("/inicio")
@logged
def dashboard():
    with db() as con: user=con.execute("SELECT * FROM users WHERE id=?",(session["uid"],)).fetchone()
    return render_template("dashboard.html",user=user,subjects=LESSONS)
@app.route("/materia/<subject>")
@logged
def subject(subject):
    data=LESSONS.get(subject)
    if not data: return redirect(url_for("dashboard"))
    return render_template("subject.html",key=subject,data=data)
@app.route("/tema/<subject>/<slug>",methods=["GET","POST"])
@logged
def topic(subject,slug):
    data=LESSONS.get(subject)
    if not data: return redirect(url_for("dashboard"))
    lesson=next((x for x in data["topics"] if x["slug"]==slug),None)
    if not lesson: return redirect(url_for("subject",subject=subject))
    result=None
    if request.method=="POST":
        try: selected=int(request.form.get("answer","-1"))
        except ValueError: selected=-1
        result=(selected==lesson["correct"])
        if result:
            with db() as con: con.execute("UPDATE users SET points=points+10, completed=completed+1 WHERE id=?",(session["uid"],))
    return render_template("topic.html",key=subject,data=data,lesson=lesson)
@app.route("/juegos")
@logged
def games(): return render_template("games.html")
@app.route("/juego/memorama")
@logged
def memory(): return render_template("memory.html")
@app.route("/juego/calculo")
@logged
def math_game(): return render_template("math_game.html")
@app.route("/progreso")
@logged
def progress():
    with db() as con: user=con.execute("SELECT * FROM users WHERE id=?",(session["uid"],)).fetchone()
    return render_template("progress.html",user=user)


@app.route("/actividad/<subject>/<slug>", methods=["GET","POST"])
@logged
def activity(subject, slug):
    data=LESSONS.get(subject)
    if not data: return redirect(url_for("dashboard"))
    lesson=next((x for x in data["topics"] if x["slug"]==slug),None)
    if not lesson: return redirect(url_for("subject",subject=subject))
    result=None
    if request.method=="POST":
        try: selected=int(request.form.get("answer","-1"))
        except ValueError: selected=-1
        result=(selected==lesson["correct"])
        if result:
            with db() as con:
                con.execute("UPDATE users SET points=points+10, completed=completed+1 WHERE id=?",(session["uid"],))
    return render_template("activity.html",key=subject,data=data,lesson=lesson,result=result)

@app.route("/juegos/<subject>")
@logged
def subject_games(subject):
    if subject not in LESSONS: return redirect(url_for("games"))
    return render_template("subject_games.html",key=subject,data=LESSONS[subject])

@app.route("/juego/<subject>/<game>")
@logged
def subject_game(subject,game):
    if subject not in LESSONS or game not in ("memorama","reto"): return redirect(url_for("games"))
    return render_template("subject_game.html",key=subject,data=LESSONS[subject],game=game)

@app.route("/examen/<subject>",methods=["GET","POST"])
@logged
def exam(subject):
    data=LESSONS.get(subject)
    if not data: return redirect(url_for("dashboard"))
    questions=[]
    for t in data["topics"]:
        questions.append({"topic":t["title"],"question":t["question"],"answers":t["answers"],"correct":t["correct"]})
    questions=questions[:5]
    score=None
    if request.method=="POST":
        correct=0
        for i,q in enumerate(questions):
            try: chosen=int(request.form.get(f"q{i}","-1"))
            except ValueError: chosen=-1
            if chosen==q["correct"]: correct+=1
        score=correct
        if correct:
            with db() as con:
                con.execute("UPDATE users SET points=points+?, completed=completed+? WHERE id=?",(correct*5,correct,session["uid"]))
    return render_template("exam.html",key=subject,data=data,questions=questions,score=score)


if __name__=="__main__":
    init_db()
    app.run(debug=True)
