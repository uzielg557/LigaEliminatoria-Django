from django.shortcuts import render, redirect, get_object_or_404
from .forms import EquipoForm
from .models import Equipo, Partido
from django.db.models import Sum, F
from django.http import Http404


# ============================================================
# 🔵 PANEL PRINCIPAL
# ============================================================

def panel_principal(request):
    """Muestra el menú principal del sistema."""
    return render(request, 'liga/panel_principal.html')



# ============================================================
# 🔵 CRUD EQUIPOS
# ============================================================

def listar_equipos(request):
    """Lista todos los equipos registrados."""
    equipos = Equipo.objects.all()
    return render(request, 'liga/listar_equipos.html', {'equipos': equipos})


def crear_equipo(request):
    """Crea un nuevo equipo mediante formulario."""
    if request.method == "POST":
        form = EquipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_equipos')
    else:
        form = EquipoForm()  # Formulario vacío

    return render(request, 'liga/crear_equipo.html', {'form': form})


def editar_equipo(request, id):
    """Edita la información de un equipo existente."""
    equipo = get_object_or_404(Equipo, id=id)

    if request.method == "POST":
        form = EquipoForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()
            return redirect('listar_equipos')
    else:
        form = EquipoForm(instance=equipo)

    return render(request, 'liga/editar_equipo.html', {'form': form})


def eliminar_equipo(request, id):
    """Permite eliminar un equipo tras confirmación."""
    equipo = get_object_or_404(Equipo, id=id)

    if request.method == "POST":
        equipo.delete()
        return redirect('listar_equipos')

    return render(request, 'liga/eliminar_equipo.html', {'equipo': equipo})



# ============================================================
# ⚽ GENERAR LIGA (ROUND ROBIN)
# ============================================================

def generar_jornadas(request):
    """
    Genera jornadas automáticas usando el algoritmo Round Robin.
    Empareja todos contra todos sin repetición.
    """
    equipos = list(Equipo.objects.all())

    if len(equipos) < 2:
        return render(request, 'liga/error.html', {
            'mensaje': 'Debes registrar al menos 2 equipos.'
        })

    lista = equipos.copy()

    # Si el número de equipos es impar -> agregamos un "descanso"
    if len(lista) % 2 != 0:
        lista.append(None)

    total = len(lista)
    jornadas = []

    # Generar jornadas con rotación circular (Round Robin)
    for _ in range(total - 1):
        jornada = []

        # Emparejamientos de la jornada
        for i in range(total // 2):
            local = lista[i]
            visitante = lista[-(i + 1)]
            jornada.append((local, visitante))

        jornadas.append(jornada)

        # Rotación de equipos (excepto el primero)
        lista = [lista[0]] + [lista[-1]] + lista[1:-1]

    # Borrar partidos anteriores
    Partido.objects.all().delete()

    # Guardar jornadas en la base de datos
    for num_jornada, jornada in enumerate(jornadas, start=1):
        for local, visitante in jornada:
            if local is None or visitante is None:
                continue  # "descansa"

            Partido.objects.create(
                equipo_local=local,
                equipo_visitante=visitante,
                jornada=num_jornada,
                goles_local=0,
                goles_visitante=0,
                jugado=False
            )

    return render(request, 'liga/jornadas_generadas.html', {
        'jornadas': jornadas
    })



# ============================================================
# 📝 REGISTRAR RESULTADOS DE LIGA
# ============================================================

def registrar_resultados(request):
    """Permite ingresar los resultados de cada partido de liga."""
    
    # Obtener todos los partidos ordenados por jornada
    partidos = Partido.objects.all().order_by("jornada", "id")

    guardado_id = None  # Para identificar qué partido se acaba de guardar

    if request.method == "POST":
        partido_id = request.POST.get("partido_id")
        goles_local = request.POST.get("goles_local")
        goles_visitante = request.POST.get("goles_visitante")

        partido = get_object_or_404(Partido, id=partido_id)

        # Guardar los resultados
        partido.goles_local = int(goles_local)
        partido.goles_visitante = int(goles_visitante)
        partido.jugado = True
        partido.save()

        # Guardamos el ID del partido recién actualizado
        guardado_id = partido.id

    return render(request, "liga/registrar_resultados.html", {
        "partidos": partidos,
        "guardado_id": guardado_id
    })



# ============================================================
# 📊 TABLA DE POSICIONES
# ============================================================

def calcular_tabla():
    """
    Calcula estadísticas de cada equipo:
    PJ, PG, PE, PP, GF, GC, DG, Puntos.
    Devuelve una tabla ordenada por:
        - Puntos
        - Diferencia de goles
        - Goles a favor
    """
    equipos = Equipo.objects.all()
    tabla = []

    for equipo in equipos:
        # Partidos donde fue local
        local = Partido.objects.filter(equipo_local=equipo, jugado=True)
        # Partidos donde fue visitante
        visitante = Partido.objects.filter(equipo_visitante=equipo, jugado=True)

        pj = local.count() + visitante.count()  # Partidos jugados

        # Goles a favor (GF)
        gf = (local.aggregate(total=Sum('goles_local'))['total'] or 0) + \
             (visitante.aggregate(total=Sum('goles_visitante'))['total'] or 0)

        # Goles en contra (GC)
        gc = (local.aggregate(total=Sum('goles_visitante'))['total'] or 0) + \
             (visitante.aggregate(total=Sum('goles_local'))['total'] or 0)

        dg = gf - gc  # Diferencia de goles

        # Victorias
        gan_local = local.filter(goles_local__gt=F('goles_visitante')).count()
        gan_visit = visitante.filter(goles_visitante__gt=F('goles_local')).count()

        # Empates
        emp_local = local.filter(goles_local=F('goles_visitante')).count()
        emp_visit = visitante.filter(goles_visitante=F('goles_local')).count()

        pg = gan_local + gan_visit
        pe = emp_local + emp_visit

        # Puntos: victoria=3, empate=1
        puntos = pg * 3 + pe

        tabla.append({
            'equipo': equipo,
            'pj': pj,
            'pg': pg,
            'pe': pe,
            'pp': pj - pg - pe,
            'gf': gf,
            'gc': gc,
            'dg': dg,
            'puntos': puntos
        })

    # Ordenar tabla
    return sorted(tabla, key=lambda x: (-x['puntos'], -x['dg'], -x['gf']))


def tabla_posiciones(request):
    """Renderiza la tabla de posiciones."""
    return render(request, "liga/tabla_posiciones.html", {
        "tabla": calcular_tabla()
    })



# ============================================================
# 🏆 MODO ELIMINATORIA
# ============================================================

def elegir_eliminatoria(request):
    """Pantalla donde se elige si será TOP 2, TOP 4, TOP 8 o TOP 16."""
    return render(request, "liga/elegir_eliminatoria.html")


def generar_eliminatoria(request, cantidad):
    cantidad = int(cantidad)

    if cantidad not in [2, 4, 8, 16]:
        raise Http404("Cantidad inválida")

    tabla = calcular_tabla()

    if len(tabla) < cantidad:
        return render(request, "liga/error.html", {
            "mensaje": f"Necesitas al menos {cantidad} equipos para este modo."
        })

    # Tomar TOP N
    top = tabla[:cantidad]
    seleccionados = [fila['equipo'] for fila in top]

    # 🔥 BORRAR TODO PARA QUE SOLO EXISTAN PARTIDOS DE LA ELIMINATORIA
    Partido.objects.all().delete()

    # Generar llaves
    llaves = []
    i = 0
    j = len(seleccionados) - 1

    while i < j:
        llaves.append((seleccionados[i], seleccionados[j]))
        i += 1
        j -= 1

    # Crear partidos
    for A, B in llaves:
        Partido.objects.create(
            equipo_local=A,
            equipo_visitante=B,
            jornada=1,
            jugado=False
        )

    return render(request, "liga/eliminatoria_generada.html", {
        "llaves": llaves,
        "cantidad": cantidad
    })



# ============================================================
# 🏆 REGISTRO Y AVANCE AUTOMÁTICO EN ELIMINATORIA
# ============================================================

def registrar_eliminatoria(request):

    partidos = Partido.objects.filter(jugado=False).order_by("id")

    # Si NO hay partidos pendientes → terminar ronda
    if not partidos.exists():

        ronda = Partido.objects.filter(jugado=True).order_by("id")
        ganadores = []

        # Determinar ganadores de la ronda
        for p in ronda:
            if p.goles_local > p.goles_visitante:
                ganadores.append(p.equipo_local)
            else:
                ganadores.append(p.equipo_visitante)

        # Si queda solo 1 → fin del torneo
        if len(ganadores) == 1:
            return render(request, "liga/campeon.html", {
                "campeon": ganadores[0]
            })

        # Crear nueva ronda
        Partido.objects.all().delete()

        i, j = 0, len(ganadores) - 1
        while i < j:
            Partido.objects.create(
                equipo_local=ganadores[i],
                equipo_visitante=ganadores[j],
                jornada=1,
                jugado=False
            )
            i += 1
            j -= 1

        return redirect("registrar_eliminatoria")

    # Si se envió un resultado
    if request.method == "POST":
        partido_id = request.POST.get("partido_id")
        gl = int(request.POST.get("goles_local"))
        gv = int(request.POST.get("goles_visitante"))

        p = get_object_or_404(Partido, id=partido_id)
        p.goles_local = gl
        p.goles_visitante = gv
        p.jugado = True
        p.save()

        print(">>> PARTIDOS EN BD:", list(Partido.objects.all()))
        print(">>> PARTIDOS JUGADOS:", list(Partido.objects.filter(jugado=True)))
        print(">>> PARTIDOS NO JUGADOS:", list(Partido.objects.filter(jugado=False)))

        return redirect("registrar_eliminatoria")

    return render(request, "liga/registrar_eliminatoria.html", {
        "partidos": partidos
    })


# Debug
print(">>> VIEWS CARGADO CORRECTAMENTE <<<")