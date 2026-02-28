#!/usr/bin/env python3
"""
Script de demostración para publicar mensajes a un broker MQTT.
Este script publica mensajes de prueba que pueden ser escuchados por mqtt_demo_listener.py
"""
import asyncio
from aiomqtt import Client
from datetime import datetime
import json


# ============================================================
# CONFIGURACIÓN HARDCODEADA
# ============================================================
MQTT_BROKER = "test.mosquitto.org"  # Broker público de prueba
MQTT_PORT = 1883
MQTT_USERNAME = None  # Cambiar si el broker requiere autenticación
MQTT_PASSWORD = None  # Cambiar si el broker requiere autenticación

# Tópico base para publicar mensajes
BASE_TOPIC = "ops-beacon/demo"


# ============================================================
# FUNCIONES
# ============================================================
async def publish_demo_messages():
    """
    Publica mensajes de demostración al broker MQTT.
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
            print(f"\n📤 Publicando mensajes de prueba...\n")

            # Publicar diferentes tipos de mensajes
            messages = [
                (f"{BASE_TOPIC}/text", "Hola desde ops-beacon!"),
                (f"{BASE_TOPIC}/sensor/temperature", "23.5°C"),
                (f"{BASE_TOPIC}/sensor/humidity", "65%"),
                (f"{BASE_TOPIC}/status", "Sistema operativo"),
                (f"{BASE_TOPIC}/json", json.dumps({
                    "timestamp": datetime.now().isoformat(),
                    "sensor": "temperature",
                    "value": 23.5,
                    "unit": "celsius"
                })),
                (f"{BASE_TOPIC}/alert", "⚠️ Alerta de prueba"),
            ]

            for i, (topic, message) in enumerate(messages, 1):
                await client.publish(topic, message)
                print(f"   [{i}/{len(messages)}] 📨 {topic}")
                print(f"        └─ {message}")
                await asyncio.sleep(1)  # Pausa de 1 segundo entre mensajes

            print(f"\n✅ Se publicaron {len(messages)} mensajes exitosamente!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise


async def continuous_publish():
    """
    Publica mensajes continuamente cada pocos segundos.
    Útil para demostrar un flujo constante de datos.
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
            print(f"\n📤 Publicando mensajes continuamente... (Presiona Ctrl+C para salir)\n")

            counter = 0
            while True:
                counter += 1
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Mensaje simple con contador
                topic = f"{BASE_TOPIC}/heartbeat"
                message = f"Mensaje #{counter} - {timestamp}"

                await client.publish(topic, message)
                print(f"   [{counter}] 📨 {topic}: {message}")

                await asyncio.sleep(3)  # Publicar cada 3 segundos

    except KeyboardInterrupt:
        print("\n\n⏹️  Deteniendo el publisher...")
        print(f"📊 Total de mensajes publicados: {counter}")
        print("\n👋 ¡Hasta luego!\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise


# ============================================================
# PUNTO DE ENTRADA
# ============================================================
if __name__ == "__main__":
    print("\n" + "=" * 100)
    print("  MQTT DEMO PUBLISHER - Script de demostración del protocolo MQTT")
    print("=" * 100)

    # Menú de opciones
    print("\nOpciones:")
    print("  1. Publicar mensajes de prueba (una vez)")
    print("  2. Publicar mensajes continuamente")
    print()

    choice = input("Selecciona una opción (1 o 2): ").strip()

    if choice == "1":
        asyncio.run(publish_demo_messages())
    elif choice == "2":
        asyncio.run(continuous_publish())
    else:
        print("❌ Opción inválida")
