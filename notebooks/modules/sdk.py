import requests, xlrd, xlwt

LANG = 'es'
APIKEY = 'GqUQ3m0uJiWPD'
APIURL = 'https://sentic.net/api/' + LANG + '/' + APIKEY + '.py?text='
FILENAME = 'data'

wb = xlrd.open_workbook(FILENAME + '.xls')
sheet = wb.sheet_by_index(0)
new_wb = xlwt.Workbook(style_compression=2)
new_sheet = new_wb.add_sheet('labeled')

# count = 0
# for row in range(sheet.nrows):
#     text = sheet.cell_value(row, 0)
#     for c in [';', '&', '#', '{', '}']: text = text.replace(c, ':')
#     label = str(requests.get(APIURL + text).content)[2:-3]
#     new_sheet.write(count, 0, text)
#     if label == 'NEGATIVE': 
#         new_sheet.write(count, 1, label, xlwt.easyxf('font: color red; align: horiz center'))
#         print(text + ': \033[91m' + label + '\033[0;0m')
#     elif label == 'POSITIVE':
#         new_sheet.write(count, 1, label, xlwt.easyxf('font: color green; align: horiz center'))
#         print(text + ': \033[92m' + label + '\033[0;0m')
#     else:
#         new_sheet.write(count, 1, label, xlwt.easyxf('align: horiz center'))
#         print(text + ': ' + label)
#     count += 1
    
# new_wb.save(FILENAME + '_labeled.xls')

text = "El día 4 de abril del año 2020 a las 5:00 a.m. ingresaron a la mina A 10 trabajadores a quienes les correspondía su turno de trabajo ese día. La mina A estaba comunicada con las minas B, C y D; en la mina B, explotación ilegal, se encontraban cinco empleados bajo tierra, en las minas C y D no se encontraban personas laborando. En la mina donde ocurrió la explosión, alrededor de las 12:10 p.m,, seis de los trabajadores se encontraban concentrados en la tornamesa y alistados para salir, los otros cuatro trabajadores se encontraban sobre el nivel principal, ese fue el momento en el que timbraron por última vez. A las 12.15 p.m. es la hora en la que se escuchó la explosión desde superficie y por las cuatro bocaminas de las cuatro minas implicadas, salió humo, polvo de carbón y fueron proyectados otros elementos. La explosión, inicio con una explosión primaria de metano y se enriqueció con polvo de carbón. Debido a que la mina era sub ventilada, con deficiente monitoreo de la atmosfera minera y registros regulares de CH4, se concentró metano en el rango de explosividad del (5 al 15% en volumen de aire), que junto con la fuente de calor dio lugar a una deflagración de gas metano. De las hipótesis sobre la fuente de ignición de la explosión, la que considero el equipo investigador más probable es una chispa eléctrica generada por alguno de los dos ventiladores o alguna de las dos electrobombas que estaban ubicados en los niveles seis y siete y que todavía estuvieran en operación, dado que el turno no había salido aun de la bocamina, los equipos no eran a prueba de explosión, ni contaban con un programa de mantenimiento, pudo haberse generado un corto eléctrico o un calentamiento que diera lugar a una chispa eléctrica que puede alcanzar temperaturas de 1100 *C. Se estimó que el foco de la explosión pudo haber sido en el nivel siete en el que se habían concentrado los trabajos en ese turno laboral. La explosión inicial de metano se expandió debido al calor y frente de llama y los gases no quemados empujaron la explosión hacia adelante lejos del extremo ciego, Esta ráfaga de aire levanto el polvo, la nube de carbón formada fue suficientemente rica para ser inflamable y continuar propagando la explosión por la totalidad de las labores de la mina y las minas que se comunicaban, existen evidencias de combustión en todo el recorrido de la mina A, alrededor de 1000 m de recorrido. La rápida expansión debido al calor desarrollo una onda de presión que de acuerdo con las afectaciones que sufrieron las minas tuvo valores comprendidos entre los 3 y 9 bares de presión. Los aumentos de presión pudieron deberse a la pulsación violenta con presión reducida causada por la condensación de la humedad. Evidencia de ello son los derrumbes sobre ambos inclinados de la mina A y en menor proporción sobre el nivel principal, en algunos sectores las presiones fueron más fuertes, colapsaron elementos del sostenimiento como puertas y sobre el nivel uno fue deformada una vagoneta y otros elementos proyectados. En las minas contiguas las consecuencias de la onda de presión se sintieron con menor poder, sin embargo, también hubo algunos derrumbes puntuales. Se estima que la explosión se propago a una velocidad promedio de 200 m/s, es decir que fue una explosión subsónica. Otra de las consecuencias de la explosión es que dio lugar a una atmosfera irrespirable, dado que en la explosión una alta participación del polvo de carbón como combustible se generaron altas concentraciones de monóxido de carbono que, de acuerdo a las evidencias, se estima estuvieron en el rango de 5 al 10% de volumen en aire. De acuerdo con los informes periciales de necropsia se determinó como como mecanismo fisiopatológico de la muerte de los trabajadores de la mina A una hipoxia aguda, secundaria a una insuficiencia respiratoria, la"
response = requests.get(APIURL + text)
print(response.content)