# Scripts de Demostración

## Scripts MQTT

Scripts de demostración para ilustrar el funcionamiento del protocolo MQTT.

### 📥 mqtt_demo_listener.py

Escucha mensajes de un broker MQTT y los muestra en pantalla en tiempo real.

**Uso:**
```bash
python scripts/mqtt_demo_listener.py
```

**Configuración (hardcodeada en el script):**
- Broker: `test.mosquitto.org` (broker público de prueba)
- Puerto: `1883`
- Tópicos: `ops-beacon/demo/#`

Para cambiar la configuración, edita las constantes al inicio del archivo.

---

### 📤 mqtt_demo_publisher.py

Publica mensajes de prueba al broker MQTT para demostrar el envío de datos.

**Uso:**
```bash
python scripts/mqtt_demo_publisher.py
```

El script ofrece dos modos:
1. **Publicar mensajes de prueba (una vez)**: Envía varios mensajes de ejemplo y termina
2. **Publicar mensajes continuamente**: Envía mensajes cada 3 segundos (útil para demostraciones)

**Configuración (hardcodeada en el script):**
- Broker: `test.mosquitto.org`
- Puerto: `1883`
- Tópico base: `ops-beacon/demo`

---

### 🎯 Demostración completa

Para ver el protocolo MQTT en acción:

1. En una terminal, inicia el listener:
   ```bash
   python scripts/mqtt_demo_listener.py
   ```

2. En otra terminal, inicia el publisher:
   ```bash
   python scripts/mqtt_demo_publisher.py
   ```

3. Observa cómo los mensajes publicados aparecen en tiempo real en el listener.

---

### 📝 Notas

- Los scripts usan el broker público `test.mosquitto.org` para facilitar la demostración
- No requieren configuración adicional ni credenciales
- Puedes modificar los brokers, tópicos y mensajes editando las constantes al inicio de cada script
- Ambos scripts manejan Ctrl+C para salir limpiamente
