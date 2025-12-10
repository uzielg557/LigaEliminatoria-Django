# 🏆 Gestor de Torneos – Django

Aplicación web desarrollada en Django que permite gestionar torneos de fútbol de forma visual e intuitiva. Incluye registro de equipos, generación automática de ligas, registro de resultados, tabla de posiciones y modo eliminatoria.

## 🚀 Características principales

### ⚽ Gestión de equipos
- Crear equipos  
- Editar equipos  
- Eliminar equipos  
- Listar equipos  

### 📅 Generación automática de Liga
- Sistema Round Robin  
- Calendario generado automáticamente  
- Registro de resultados  

### 📊 Tabla de posiciones
Incluye cálculo automático de:
- PJ, PG, PE, PP  
- GF, GC, DG  
- Puntos  

### 🥇 Modo Eliminatoria
Disponible en:
- Final (2 equipos)  
- Semifinales (4 equipos)  
- Cuartos de final (8 equipos)  
- Octavos (16 equipos)

---

# 🖼️ Capturas de Pantalla

Panel Principal  
https://github.com/uzielg557/LigaEliminatoria-Django/blob/main/%7BD1854B54-E728-4ED9-A314-99FA9B2F3033%7D.png?raw=1  

Equipos Registrados  
https://github.com/uzielg557/LigaEliminatoria-Django/blob/main/%7B46D34C17-AAAD-491B-97B2-57F70EF3032C%7D.png?raw=1  

Crear Equipo  
https://github.com/uzielg557/LigaEliminatoria-Django/blob/main/%7BA4BBEBD0-22FB-478A-8D73-1DF6694D2763%7D.png?raw=1  

Editar Equipo  
https://github.com/uzielg557/LigaEliminatoria-Django/blob/main/%7BF65F510C-FE39-42FA-9D55-42F60122CA12%7D.png?raw=1  

Eliminar Equipo  
https://github.com/uzielg557/LigaEliminatoria-Django/blob/main/%7BBB477601-94FF-468F-84A7-F359580DAA3A%7D.png?raw=1  

Jornadas Generadas  
https://github.com/uzielg557/LigaEliminatoria-Django/blob/main/%7BF81D44DB-684A-4A4D-B838-A6679FECC5A9%7D.png?raw=1  

Registrar Resultados  
https://github.com/uzielg557/LigaEliminatoria-Django/blob/main/%7BD13FAC69-0BF5-4AA3-A506-E614BF4AA6C4%7D.png?raw=1  

Tabla de Posiciones  
https://github.com/uzielg557/LigaEliminatoria-Django/blob/main/%7B7C3F060D-21EF-4424-9ABD-F3AAC1F3DAB0%7D.png?raw=1  

Elegir Eliminatoria  
https://github.com/uzielg557/LigaEliminatoria-Django/blob/main/%7B61ED6211-5459-49BC-B533-1BA770883ECD%7D.png?raw=1  

Eliminatoria Generada  
https://github.com/uzielg557/LigaEliminatoria-Django/blob/main/%7B7848E2A6-26DC-4BA2-B30A-FCAFB3CB0D5E%7D.png?raw=1  

Registrar Eliminatoria  
https://github.com/uzielg557/LigaEliminatoria-Django/blob/main/%7B7B997B89-1E98-4E75-97CE-31E5B78DADF5%7D.png?raw=1  

Campeón del Torneo  
https://github.com/uzielg557/LigaEliminatoria-Django/blob/main/%7BD50BCA5D-EA60-4CCD-A1D2-392D37BC6709%7D.png?raw=1  

---

# 📦 Instalación

git clone https://github.com/uzielg557/LigaEliminatoria-Django.git  
cd LigaEliminatoria-Django  
python -m venv venv  
venv\Scripts\activate  
pip install -r requirements.txt  
python manage.py runserver  

---

# 📁 Estructura del Proyecto

TorneoDjango/  
│── gestor_torneos/  
│── liga/  
│── db.sqlite3  
│── manage.py  
│── requirements.txt  

---

# 👨‍💻 Autor

Víctor Uziel García Jácome  
Proyecto desarrollado con Django para la gestión de torneos deportivos.
