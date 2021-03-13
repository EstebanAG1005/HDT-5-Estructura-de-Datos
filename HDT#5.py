import simpy
import random
import os 

# Codigo Creado por Esteban Aldana Guerra 20591 y Kenneth Galvez 20079

# Codigo Basado en ejemplo dado en (Clase de una gasolinera)

# Corre varias simulaciones para ver en cuento tiempo se realiza ese proceso dentro de la memoria
random.seed(10)

def simulacion(env, nombre, RAM, Procesadora, memoria, instruccion, Tprocesos, Tiempo,TiempoT):
    # Inicia la simulacion
    sim = True
    
    yield env.timeout(Tiempo)
    # Mientras que el programa este funcionando va a realizar la simulacion
    tiempoI = Tiempo
    yield env.timeout(Tiempo)
    while sim == True:
        yield env.timeout(tiempoI)
        # Simular que obtiene el espacio en memoria
        yield RAM.get(memoria)
        # Mientras que las instrucciones sean mayores a 0
        while instruccion > 0:
          pTiempo = env.now
          
            # Se dirige al lugar donde se va a realizar el proceso
            # pero si hay otro proceso, debe hacer cola
          with Procesadora.request() as cola:
                yield env.timeout(instruccion- Tprocesos/Tprocesos)
                # Ya comenzo el proceso
                yield cola
                # Realza el proceso en un tiempo determinado
                yield env.timeout(1)
                tiempoI = tiempoI + env.now-pTiempo +1
                #Calculo para determinar el timpo de la instrucción
                instruccion = instruccion - Tprocesos
                #Random para escoger si entrara en la cola de "waiting" o volvera a entrar en la cola de "ready"
                Cprocesos = random.randint(1, 2)
                #-------------Waiting---------------
                if (Cprocesos == 1):
                    print("Se envia el proceso %s a la cola durante %s segundos. Tiempo Actual: %s , Espacio en memoria utilizado por el proceso: %s" % (
                        nombre, Tiempo, env.now, memoria))
                    #Regreso a la cola ready al terminar la operación.    
                    yield env.timeout(Tiempo)
                    tiempoI = tiempoI + 1
                #-------------Ready----------------
                else:
                    #Se muestran los resultados obtenidos de la simulacion de cada proceso
                    print("Se envia el proceso %s a la memoria para obtener su tiempo en realiar el proceso, Tiempo %s, Tiempo Actual: %s , Espacio en memoria utilizado: %s" % (
                        nombre, Tprocesos, env.now, memoria))
                    #Se finaliza el proceso y vuelve a "ready".
                    print('Proceso %s finalizado, Tiempo en el que se finalizo: %s' % (nombre, env.now))
                    RAM.put(memoria)
                    sim = False
                    print("Le tomo %s segundos a %s terminar el proceso." %(tiempoI,nombre))
                    TiempoT.put(tiempoI)
                    

#--------:v--------#
#Ambiente de simulación
env = simpy.Environment()
# Se usa simpy.Container para simular la memoria y se hace cola para solicitar la memoria necesaria para la simulacion.
RAM = simpy.Container(env, init=100,capacity=100)
#Cantidad de Memoria RAM
#Capacidad para la procesadora
Procesadora = simpy.Resource(env, capacity=1)
TiempoT = simpy.Container(env,capacity=10000000000000000000000000)


for i in range(100):
  env.process(simulacion(env, i+1, RAM, Procesadora, random.randint(1, 10), random.randint(1,10), 6, round(random.expovariate(1/10)+ 1),TiempoT))

# Se corre la simulacion
env.run()
print("Tiempo promedio:",TiempoT.level/100)
#Funcion para limpiar la pantalla
def limpiar():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


        