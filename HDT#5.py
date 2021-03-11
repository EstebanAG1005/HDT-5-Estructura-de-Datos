import simpy
import random
# Codigo Creado por Esteban Aldana Guerra 20591 y Kenneth Galvez 20079

# Codigo Basado en ejemplo dado en (Clase de una gasolinera)

# Corre varias simulaciones para ver en cuento tiempo se realiza ese proceso dentro de la memoria


def simulacion(env, nombre, RAM, Procesadora, memoria, instruccion, Tprocesos, Tiempo,):
    # Inicia la simulacion
    sim = True
    # Mientras que el programa este funcionando va a realizar la simulacion
    while sim == True:
        # Simular que obtiene el espacio en memoria
        yield RAM.get(memoria)
        # Mientras que las instrucciones sean mayores a 0
        while instruccion > 0:
            # Se dirige al lugar donde se va a realizar el proceso
            # pero si hay otro proceso, debe hacer cola
            with Procesadora.request() as cola:
                # Ya comenzo el proceso
                yield cola
                # Realza el proceso en un tiempo determinado
                yield env.timeout(1)

                instruccion = instruccion - Tprocesos

                Cprocesos = random.randint(1, 2)

                if (Cprocesos == 1):
                    print("Se envia proceso %s a cola por %s segundos. Tiempo Actual: %s , Espacio en memoria: %s" % (
                        nombre, Tiempo, env.now, memoria))
                    yield env.timeout(Tiempo)
                else:
                    print("Se envia el proceso %s a la memoria para ver su tiempo, Tiempo %s, Tiempo Actual: %s , Espacio en memoria: %s" % (
                        nombre, Tprocesos, env.now, memoria))
                    print('Proceso %s exitoso, finalizando en tiempo: %s' % (nombre, env.now))
                    RAM.put(memoria)
                    sim = False


env = simpy.Environment()
RAM = simpy.Container(env, capacity=100)
RAM.put(100)
Procesadora = simpy.Resource(env, capacity=2)


for i in range(6):
    env.process(simulacion(env, i+1, RAM, Procesadora,random.randint(30, 60), random.randint(8, 12), 3, 3))


# Se corre la simulacion
env.run()

        
        
        