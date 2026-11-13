# Seguimientos PMP — ANI

Fuente: https://www.ani.gov.co/planes/plan-mejoramiento-procesos-pmp-21720

Enlaces consultados el 13 de noviembre de 2026. La página lista tres documentos:

| Corte | Enlace original |
| --- | --- |
| 30 de junio de 2026 | [Documento](https://www.ani.gov.co/documents/20117/0/Estado%20del%20PMP%20a%2030%20de%20junio%20de%202026%20(1).pdf/1df013ee-45b7-423e-71f8-faca39490fb9) |
| 31 de julio de 2026 | [Documento](https://www.ani.gov.co/documents/20117/0/estado%20del%20pmp%20con%20corte%20a%2031%20de%20Julio%20de2026/1596aaff-4728-c629-7e0f-5399479ea271) |
| 30 de septiembre de 2026 | [Documento](https://www.ani.gov.co/documents/20117/0/Estado_del_pmp_con_corte_a_30_de_Septiembre_de_2026/490f5a83-f85f-5143-1694-28f6b9795139) |

## Descargar originales

Desde una red con acceso a `www.ani.gov.co`, ejecutar con Python 3.8 o superior:

```sh
python3 scripts/descargar_pmp.py
```

Los archivos se guardan en `datos/originales/`, excluido de Git. El script identifica PDF y Excel por su cabecera, rechaza respuestas no reconocidas y devuelve un código de error si alguna descarga falla. Los enlaces están disponibles también en `datos/fuentes.json`.

**Estado:** los originales no se han descargado en este entorno porque la conexión directa al dominio de ANI está restringida. La consulta de la página sí permitió recuperar los enlaces. No se han convertido ni reconstruido los datos, ni se ha verificado el contenido completo de los archivos.

## Aplicación interactiva de hallazgos

Abrir `app/index.html` directamente en el navegador o ejecutar:

```sh
python3 -m http.server 8000 --bind 0.0.0.0 --directory app
```

La aplicación funciona sin dependencias ni servicios externos. Incluye filtros por
vencimiento, grupo y texto, ficha de cada hallazgo, exportación CSV y reporte
imprimible/guardable como PDF de la selección completa.

Datos: CSV aportado por la usuaria, corte 30/09/2026, 268 filas. El archivo
`app/data.js` preserva los campos utilizados sin reconstruir cifras del texto.
Para regenerarlo: `python3 scripts/preparar_tablero.py RUTA_AL_CSV` (cp1252, `;`).

El modelo estima conteos anuales, **no cierre ni probabilidad de incumplimiento**.
Entrena con Defensa Judicial 2019–2024 y prueba con 2025–2026; el último año es
parcial. Se muestran MAE, RMSE y una referencia constante (conteo 2024). La agenda
operativa se limita a VJ; el entrenamiento incluye también grupos compartidos.

## Publicar en GitHub Pages

La aplicación es completamente estática: no necesita Python, Node ni un servidor
backend en producción. El flujo `.github/workflows/pages.yml` publica **solo
`app/`** como raíz del sitio, por lo que no hay que añadir `/app/` a la URL.
Los recursos usan rutas relativas compatibles con sitios de proyecto de GitHub.

1. Incorporar estos cambios a `main` mediante un pull request.
2. En el repositorio, abrir **Settings → Pages → Build and deployment → Source**
   y seleccionar **GitHub Actions**.
3. Un push a `main` publica el sitio automáticamente. También se puede ejecutar
   **Actions → Deploy GitHub Pages → Run workflow** seleccionando `main`.
4. Consultar la URL publicada en el entorno `github-pages` o en **Settings → Pages**.
   Con el nombre actual del repositorio, la URL predeterminada será:
   <https://carolinabarrerov-lang.github.io/Seguimientos-PMP/>.

Los pull requests hacia `main` solo validan; no publican cambios. Si se ejecuta
manualmente el flujo desde otra rama, esa rama se desplegará (sujeto a las reglas
del entorno `github-pages`). No se requiere ningún secreto personalizado.

Antes de publicar, confirmar que los datos institucionales incluidos en
`app/data.js` pueden estar disponibles públicamente: Pages sirve todos los
archivos del directorio publicado.

### Validación local

```sh
python3 scripts/check_pages.py
node --check app/app.js
node --check app/data.js
```

Para probar el mismo directorio que se publica:

```sh
python3 -m http.server 8000 --bind 0.0.0.0 --directory app
```

Si GitHub indica que Pages no está habilitado, revisar primero **Settings → Pages**.
Si rechaza un despliegue por la rama, revisar las reglas del entorno **github-pages**.
