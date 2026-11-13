"""Convierte el CSV ANI cp1252 a datos estáticos del tablero (sin dependencias)."""
import csv,json,sys
from pathlib import Path
p=Path(sys.argv[1])
rows=list(csv.DictReader(p.open(encoding='cp1252',newline=''),delimiter=';'))
keys={'Consecutivo':'id','Año':'year','Descripción Hallazgo':'description','Nombre Informe Auditoría':'audit','Vicepresidencia/Oficina Responsable':'office','Grupo Interno de Trabajo':'group','Fecha de Inicio':'start','Fecha de Terminación':'end','Avance':'progress','Estado':'status','Plan de Mejoramiento':'plan','No. de acciones':'actions','No. Prórroga en fecha terminación plan':'extensions','Categoria':'category','Auditor Actual':'auditor','Seguimiento Control Interno':'tracking'}
data=[{v:r.get(k,'').strip() for k,v in keys.items()} for r in rows]
Path('app/data.js').write_text('window.ANI_DATA = '+json.dumps(data,ensure_ascii=False)+';\n',encoding='utf-8')
print(f'{len(data)} registros exportados')
