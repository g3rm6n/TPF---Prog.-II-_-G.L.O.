import time
import random


class DispositivoIOT:
    def operar(self):
        pass


class SensorTemperaturaCongelados(DispositivoIOT):
    def __init__(self):
        self.temperatura = range(-30, -18)

    def obtener_lectura(self):
        self.temperatura = round(random.uniform(-35, -15), 2)
        return self.temperatura

    def operar(self):
        temperatura = self.obtener_lectura()
        if temperatura < -30 or temperatura > -18:
            return f"\nCámara Frigorífica CONGELADOS: Temperatura detectada: {temperatura} °C. - Temperatura fuera de rango."
        else:
            return f"\nCámara Frigorífica CONGELADOS: Temperatura detectada: {temperatura} °C."


class SensorHumedadCongelados(DispositivoIOT):
    def __init__(self):
        self.humedad = range(85, 95)

    def obtener_lectura(self):
        self.humedad = round(random.uniform(80, 99), 0)
        return self.humedad
    
    def operar(self, humedad):
        if humedad < 85 or humedad > 95:
            return f"\nCámara Frigorífica CONGELADOS: Humedad detectada: {humedad} %. - Humedad fuera de rango."
        else:
            return f"\nCámara Frigorífica CONGELADOS: Humedad detectada: {humedad} %."


class SensorTemperaturaConserva(DispositivoIOT):
    def __init__(self):
        self.temperatura = range(-3, 7)

    def obtener_lectura(self):
        self.temperatura = round(random.uniform(-10, 10), 2)
        return self.temperatura
    
    def operar(self):
        temperatura = self.obtener_lectura()
        if temperatura < -3 or temperatura > 7:
            return f"Cámara Frigorífica CONSERVAS: Temperatura detectada: {temperatura} °C. - Temperatura fuera de rango."
        else:
            return f"Cámara Frigorífica CONSERVAS: Temperatura detectada: {temperatura} °C."


class SensorHumedadConserva(DispositivoIOT):
    def __init__(self):
        self.humedad = range(65, 85)

    def obtener_lectura(self):
        self.humedad = round(random.uniform(60, 90), 0)
        return self.humedad
    
    def operar(self, humedad):
        if humedad < 65 or humedad > 85:
            return f"Cámara Frigorífica CONSERVAS: Humedad detectada: {humedad} %. - Humedad fuera de rango."
        else:
            return f"Cámara Frigorífica CONSERVAS: Humedad detectada: {humedad} %."


class Activar_Deshumidificador_Congelados(DispositivoIOT):
    def __init__(self):
        self.activo = False

    def operar(self, humedad):
        if humedad > 95:
            if not self.activo:
                self.activo = True
                return "\nDeshumidificador CONGELADOS ACTIVADO."
        elif humedad <= 95 and self.activo:
            self.activo = False
            return "\nDeshumidificador CONGELADOS DESACTIVADO."
        return None


class Activar_Deshumidificador_Conservas(DispositivoIOT):
    def __init__(self):
        self.activo = False

    def operar(self, humedad):
        if humedad > 85:
            if not self.activo:
                self.activo = True
                return "\nDeshumidificador CONSERVAS ACTIVADO."
        elif humedad <= 85 and self.activo:
            self.activo = False
            return "\nDeshumidificador CONSERVAS DESACTIVADO."
        return None


class Activar_Generador(DispositivoIOT):
    def __init__(self):
        self.activo = False

    def operar(self):
        if not self.activo:
            self.activo = True
            return "\nGenerador ACTIVADO."
        return None


class Control_Electricidad(DispositivoIOT):
    def __init__(self, generador):
        self.generador = generador
        self.luz_activa = True

    def detectar_corte_luz(self):
        return random.choice([True, False])

    def operar(self):
        if self.detectar_corte_luz():
            if self.luz_activa:
                self.luz_activa = False
                print(f"\nCORTE en el Suministro de Electricidad.")
                return self.generador.operar()
        else:
            if not self.luz_activa:
                self.luz_activa = True
                if self.generador.activo:
                    self.generador.activo = False
                    print(f"\nSuministro de Electricidad RESTABLECIDO.")
                    return "\nGenerador DESACTIVADO."
        return None


class AdministradordeDispositivos:
    def __init__(self):
        self.dispositivos = []

    def agregar_dispositivos(self, dispositivo):
        self.dispositivos.append(dispositivo)

    def operar(self):
        resultados = []
        for dispositivo in self.dispositivos:
            resultado = dispositivo.operar()
            if resultado:
                resultados.append(resultado)
        return resultados


administrador = AdministradordeDispositivos()

sensor_temp_congelados = SensorTemperaturaCongelados()
sensor_hum_congelados = SensorHumedadCongelados()
sensor_temp_conserva = SensorTemperaturaConserva()
sensor_hum_conserva = SensorHumedadConserva()
deshumidificador_congelados = Activar_Deshumidificador_Congelados()
deshumidificador_conserva = Activar_Deshumidificador_Conservas()
generador = Activar_Generador()
control_electricidad = Control_Electricidad(generador)

administrador.agregar_dispositivos(sensor_temp_congelados)
administrador.agregar_dispositivos(sensor_temp_conserva)
administrador.agregar_dispositivos(control_electricidad)

try:
    while True:
        resultados = administrador.operar()
        
        humedad_congelados = sensor_hum_congelados.obtener_lectura()
        humedad_conserva = sensor_hum_conserva.obtener_lectura()

        resultado_humedad_congelados = sensor_hum_congelados.operar(humedad_congelados)
        resultado_humedad_conserva = sensor_hum_conserva.operar(humedad_conserva)

        resultados.append(resultado_humedad_congelados)
        resultados.append(resultado_humedad_conserva)

        resultado_deshumidificador_congelados = deshumidificador_congelados.operar(humedad_congelados)
        resultado_deshumidificador_conserva = deshumidificador_conserva.operar(humedad_conserva)

        if resultado_deshumidificador_congelados:
            resultados.append(resultado_deshumidificador_congelados)
        if resultado_deshumidificador_conserva:
            resultados.append(resultado_deshumidificador_conserva)

        for resultado in resultados:
            print(resultado)
            
        time.sleep(30)
        print("\n--------------------------------------------------------------------------------")
except KeyboardInterrupt:
    print("Interrumpido.")
