# Seguimientos PMP — ANI

Bases de datos del **Plan de Mejoramiento por Procesos (PMP)** de la Agencia Nacional
de Infraestructura (ANI), tomadas de la página oficial:

<https://www.ani.gov.co/planes/plan-mejoramiento-procesos-pmp-21720>

## Qué se descargó

La página publica tres cortes del estado del PMP (informes de la Oficina de Control
Interno + base de datos en formato Excel publicada dentro de cada archivo):

| Corte | Archivo publicado (URL oficial) | Contenido |
|---|---|---|
| 30-jun-2026 | `Estado del PMP a 30 de junio de 2026 (1).pdf` → `1df013ee-45b7-423e-71f8-faca39490fb9` | Memorando 20261020160743 + informe de balance trimestral abr–jun 2026 |
| 31-jul-2026 | `estado del pmp con corte a 31 de Julio de2026` → `1596aaff-4728-c629-7e0f-5399479ea271` | Base PMP completa: hoja *Resumen*, hoja *Vigentes* (consecutivo por hallazgo/plan) y demás hojas |
| 30-sep-2026 | `Estado_del_pmp_con_corte_a_30_de_Septiembre_de_2026` → `490f5a83-f85f-5143-1694-28f6b9795139` | Base PMP completa con corte a septiembre |

## Contenido de `datos/`

Archivos tabulares (`UTF-8`, separados por coma) construidos a partir de los
documentos oficiales, más una consolidación en Excel:

| Archivo | Descripción |
|---|---|
| `PMP_ANI_bases_consolidadas.xlsx` | **Consolidado**: una hoja por tabla |
| `resumen_cortes.csv` | Indicadores por corte (jun / jul / sep 2026) |
| `planes_vigentes_2026-06-30.csv` | Planes por estado (implementado, en término, vencido, sin plan) |
| `implementados_efectividad_2026-06-30.csv` | Revisión de efectividad de los 130 planes implementados |
| `planes_por_anio_origen_2026-06-30.csv` | Planes por año de origen del hallazgo y estado |
| `planes_por_dependencia_2026-06-30.csv` | Planes vigentes por vicepresidencia/oficina |
| `planes_por_proyecto_top10_2026-06-30.csv` | Top 10 proyectos por número de planes |
| `distribucion_avance_2026-06-30.csv` | Intervalos de avance (en término y vencidos) |
| `planes_vencidos_2026-06-30.csv` | Los 28 planes vencidos con área, GIT y fecha de terminación |
| `planes_reformulacion_2026-06-30.csv` | Planes con concepto de no efectividad que requieren reformulación |
| `hallazgos_sin_plan_2026-06-30.csv` | Los 35 planes requeridos para 20 hallazgos sin formular |
| `planes_mayor_numero_prorrogas_2026-06-30.csv` | Planes con más prórrogas solicitadas |
| `vencimientos_S2_2026.csv` | Vencimientos del segundo semestre de 2026 por vicepresidencia y avance |
| `planes_cerrados_no_vigentes_abr_jun_2026.csv` | Cierres y planes no vigentes del trimestre |
| `variacion_hallazgos_trimestre_2026.csv` | Ingresos/salidas de hallazgos ene–mar vs abr–jun |

Cada tabla replica las cifras publicadas y citadas en el informe de la OCI
(corte 30-jun-2026); la tabla `resumen_cortes.csv` añade los cortes de julio y
septiembre tomados de las hojas *Resumen* de esas bases.

## Descarga automática de los archivos originales (PDF/Excel)

El sitio de la ANI bloquea las conexiones salientes de este entorno de trabajo, por
eso la descarga de los originales se hace desde un runner de GitHub Actions del
propio repositorio, que corre el workflow:

```
.github/workflows/descargar-pmp.yml
```

Pasos para obtener los archivos originales:

1. En GitHub: **Actions → Descargar bases PMP ANI → Run workflow** (o se ejecuta
   automáticamente al abrir/actualizar un pull request a `main`).
2. El job `descargar` guarda los archivos en `datos/raw/` y los publica como
   artefacto **`pmp-ani-crudos`** de la ejecución.
3. Descargue el artefacto (desde la UI de la ejecución o con
   `gh run download <run-id> -n pmp-ani-crudos`).
4. Si el token del workflow tiene permiso de escritura, además se hace commit de
   `datos/raw/` en la rama.

> Nota: el `GITHUB_TOKEN` de este repositorio está configurado como **solo lectura**
> para Actions, por lo que el paso de commit puede omitirse (`continue-on-error`);
> en ese caso los archivos quedan únicamente en el artefacto.

Para correrlo localmente en un equipo con acceso a internet:

```bash
mkdir -p datos/raw
curl -L -o datos/raw/PMP_estado_2026-06-30.pdf \
  "https://www.ani.gov.co/documents/20117/0/Estado%20del%20PMP%20a%2030%20de%20junio%20de%202026%20(1).pdf/1df013ee-45b7-423e-71f8-faca39490fb9"
curl -L -o datos/raw/PMP_estado_2026-07-31.xlsx \
  "https://www.ani.gov.co/documents/20117/0/estado%20del%20pmp%20con%20corte%20a%2031%20de%20Julio%20de2026/1596aaff-4728-c629-7e0f-5399479ea271"
curl -L -o datos/raw/PMP_estado_2026-09-30.xlsx \
  "https://www.ani.gov.co/documents/20117/0/Estado_del_pmp_con_corte_a_30_de_Septiembre_de_2026/490f5a83-f85f-5143-1694-28f6b9795139"
```

## Fuente

Agencia Nacional de Infraestructura — Oficina de Control Interno.
Informe de balance del Plan de Mejoramiento por Procesos, cortes 30-jun-2026,
31-jul-2026 y 30-sep-2026. Datos públicos.
