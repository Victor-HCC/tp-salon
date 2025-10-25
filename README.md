### Antes de iniciar por primera vez, crear manualmente una base de datos "salon_db" y ejecutar en la terminal desde la raíz

```bash
mysql -u root -p salon_db < scripts/tablas.sql 
```

### Creación de entorno virtual

```bash
python3 -m venv venv  # O 'python'
```

### Activación de entorno virtual 

```bash
source venv/bin/activate # Ubuntu

.\venv\Scripts\Activate.ps1 # Windows
```

### Desactivar entorno virtual

```bash
deactivate
```

### Instalar librerías

```bash
pip install -r requirements.txt
```

### Para crear al usuario admin
```bash
python3 scripts/crear_admin.py 
```