#!/usr/bin/env python3
"""
Script de demostración para escuchar mensajes de un broker MQTT.
Este script se conecta a un broker y muestra en pantalla todos los mensajes que llegan.
"""
import asyncio
from aiomqtt import Client
from datetime import datetime


# ============================================================
# CONFIGURACIÓN HARDCODEADA
# ============================================================
MQTT_BROKER = "test.mosquitto.org"  # Broker público de prueba
MQTT_PORT = 1883
MQTT_USERNAME = None  # Cambiar si el broker requiere autenticación
MQTT_PASSWORD = None  # Cambiar si el broker requiere autenticación

# Tópicos a los que se va a suscribir (puedes usar wildcards como #, +)
TOPICS_TO_SUBSCRIBE = [
    "ops-beacon/demo/#",  # Escucha todos los subtópicos de ops-beacon/demo
    # "sensors/temperature",  # Ejemplo de tópico específico
    # "test/+/data",  # Ejemplo con wildcard
]


# ============================================================
# FUNCIONES
# ============================================================
def print_message_header():
    """Imprime el encabezado de la tabla de mensajes."""
    print("\n" + "=" * 100)
    print(f"{'TIMESTAMP':<25} | {'TOPIC':<40} | {'MESSAGE':<30}")
    print("=" * 100)


def print_message(topic: str, payload: str, timestamp: str):
    """Imprime un mensaje recibido de forma formateada."""
    # Truncar el payload si es muy largo
    if len(payload) > 30:
        payload_display = payload[:27] + "..."
    else:
        payload_display = payload

    print(f"{timestamp:<25} | {topic:<40} | {payload_display:<30}")


async def listen_mqtt():
    """
    Función principal que se conecta al broker MQTT y escucha mensajes.
    """
    print(f"\n🔌 Conectando al broker MQTT: {MQTT_BROKER}:{MQTT_PORT}")

    try:
        async with Client(
            hostname=MQTT_BROKER,
            port=MQTT_PORT,
            username=MQTT_USERNAME,
            password=MQTT_PASSWORD,
        ) as client:

            print(f"✅ Conectado exitosamente al broker!")
            print(f"\n📡 Suscribiéndose a los tópicos:")

            # Suscribirse a todos los tópicos configurados
            for topic in TOPICS_TO_SUBSCRIBE:
                await client.subscribe(topic)
                print(f"   - {topic}")

            print_message_header()
            print("\n🎧 Escuchando mensajes... (Presiona Ctrl+C para salir)\n")

            # Escuchar mensajes indefinidamente
            message_count = 0
            async for message in client.messages:
                message_count += 1
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                topic = str(message.topic)
                payload = message.payload.decode('utf-8', errors='replace')

                print_message(topic, payload, timestamp)

                # Cada 20 mensajes, reimprimir el encabezado
                if message_count % 20 == 0:
                    print_message_header()

    except KeyboardInterrupt:
        print("\n\n⏹️  Deteniendo el listener...")
        print(f"📊 Total de mensajes recibidos: {message_count}")
        print("\n👋 ¡Hasta luego!\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise


# ============================================================
# PUNTO DE ENTRADA
# ============================================================
if __name__ == "__main__":
    print("\n" + "=" * 100)
    print("  MQTT DEMO LISTENER - Script de demostración del protocolo MQTT")
    print("=" * 100)

    asyncio.run(listen_mqtt())
