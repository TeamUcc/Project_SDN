# TALLER DE CIRCUITOS ELÉCTRICOS
## Análisis de Circuitos Serie, Paralelo y Mixtos

---

## EJERCICIO SERIE 1

### 1. Portada
- **Curso:** Circuitos Eléctricos
- **Ejercicio:** Serie 1 - Análisis de circuito con tres resistencias
- **Fecha:** [Completar con fecha actual]

### 2. Objetivo
Analizar un circuito en serie determinando Req, corriente total, caídas de tensión y potencias; validar con simulación y montaje.

### 3. Materiales
- Fuente DC o pila 9V
- Resistencias: R1=220Ω, R2=330Ω, R3=1kΩ
- Protoboard
- Cables de conexión
- Multímetro

### 4. Esquema del Circuito
```
V = 9V ---|---R1(220Ω)---|---R2(330Ω)---|---R3(1kΩ)---|--- GND
```

### 5. Cálculos Teóricos Detallados

**Resistencia Equivalente (Req):**
En un circuito en serie: Req = R1 + R2 + R3
Req = 220Ω + 330Ω + 1000Ω = 1550Ω

**Corriente Total (I):**
Aplicando Ley de Ohm: I = V/Req
I = 9V / 1550Ω = 0.00581 A = 5.81 mA

**Caídas de Tensión:**
- V1 = I × R1 = 0.00581 A × 220Ω = 1.278 V
- V2 = I × R2 = 0.00581 A × 330Ω = 1.917 V  
- V3 = I × R3 = 0.00581 A × 1000Ω = 5.810 V

**Verificación:** V1 + V2 + V3 = 1.278 + 1.917 + 5.810 = 9.005 V ≈ 9V ✓

**Potencias:**
- P1 = V1 × I = 1.278 V × 0.00581 A = 0.00742 W = 7.42 mW
- P2 = V2 × I = 1.917 V × 0.00581 A = 0.01113 W = 11.13 mW
- P3 = V3 × I = 5.810 V × 0.00581 A = 0.03375 W = 33.75 mW
- PT = P1 + P2 + P3 = 52.30 mW

**Verificación:** PT = V × I = 9V × 0.00581A = 52.29 mW ✓

---

## EJERCICIO SERIE 2

### 1. Datos del Circuito
- V = 9V DC
- R1 = 470Ω, R2 = 680Ω, R3 = 2.2kΩ

### 2. Cálculos Teóricos

**Resistencia Equivalente:**
Req = R1 + R2 + R3 = 470Ω + 680Ω + 2200Ω = 3350Ω

**Corriente Total:**
I = V/Req = 9V / 3350Ω = 0.002687 A = 2.687 mA

**Caídas de Tensión:**
- V1 = I × R1 = 0.002687 A × 470Ω = 1.263 V
- V2 = I × R2 = 0.002687 A × 680Ω = 1.827 V
- V3 = I × R3 = 0.002687 A × 2200Ω = 5.911 V

**Potencias:**
- P1 = V1 × I = 1.263 V × 0.002687 A = 3.394 mW
- P2 = V2 × I = 1.827 V × 0.002687 A = 4.910 mW
- P3 = V3 × I = 5.911 V × 0.002687 A = 15.884 mW
- PT = 24.188 mW

---

## EJERCICIO PARALELO 1

### 1. Datos del Circuito
- V = 9V DC
- R1 = 1kΩ, R2 = 2.2kΩ, R3 = 4.7kΩ

### 2. Cálculos Teóricos

**Resistencia Equivalente:**
Para resistencias en paralelo: 1/Req = 1/R1 + 1/R2 + 1/R3
1/Req = 1/1000 + 1/2200 + 1/4700
1/Req = 0.001 + 0.000454 + 0.000213 = 0.001667
Req = 1/0.001667 = 600Ω

**Tensiones en cada rama:**
En paralelo, todas las resistencias tienen la misma tensión:
V1 = V2 = V3 = V = 9V

**Corrientes de rama:**
- I1 = V/R1 = 9V / 1000Ω = 9.00 mA
- I2 = V/R2 = 9V / 2200Ω = 4.09 mA
- I3 = V/R3 = 9V / 4700Ω = 1.91 mA

**Corriente Total:**
IT = I1 + I2 + I3 = 9.00 + 4.09 + 1.91 = 15.00 mA

**Verificación:** IT = V/Req = 9V / 600Ω = 15.00 mA ✓

**Potencias:**
- P1 = V1 × I1 = 9V × 0.009A = 81.0 mW
- P2 = V2 × I2 = 9V × 0.00409A = 36.8 mW
- P3 = V3 × I3 = 9V × 0.00191A = 17.2 mW
- PT = P1 + P2 + P3 = 135.0 mW

---

## EJERCICIO PARALELO 2

### 1. Datos del Circuito
- V = 9V DC
- R1 = 680Ω, R2 = 1kΩ, R3 = 1.5kΩ

### 2. Cálculos Teóricos

**Resistencia Equivalente:**
1/Req = 1/680 + 1/1000 + 1/1500
1/Req = 0.001471 + 0.001 + 0.000667 = 0.003138
Req = 318.7Ω

**Corrientes de rama:**
- I1 = 9V / 680Ω = 13.24 mA
- I2 = 9V / 1000Ω = 9.00 mA  
- I3 = 9V / 1500Ω = 6.00 mA
- IT = 28.24 mA

**Potencias:**
- P1 = 9V × 13.24mA = 119.2 mW
- P2 = 9V × 9.00mA = 81.0 mW
- P3 = 9V × 6.00mA = 54.0 mW
- PT = 254.2 mW

---

## EJERCICIOS MIXTOS

### Análisis General para Circuitos Mixtos

Para los circuitos mixtos mostrados en las imágenes, el procedimiento es:

1. **Identificar las conexiones serie y paralelo**
2. **Simplificar paso a paso:**
   - Calcular resistencias equivalentes de secciones paralelas
   - Combinar con resistencias en serie
   - Reducir hasta obtener Req total

3. **Calcular corriente total:** IT = V/Req

4. **Trabajar hacia atrás:**
   - Calcular tensiones en cada nodo
   - Determinar corrientes en cada rama
   - Calcular potencias individuales

### Ejemplo de Metodología:

**Para un circuito con R1 en serie con (R2 || R3):**

1. Req_paralelo = (R2 × R3)/(R2 + R3)
2. Req_total = R1 + Req_paralelo  
3. IT = V/Req_total
4. V1 = IT × R1
5. V_paralelo = V - V1
6. I2 = V_paralelo/R2
7. I3 = V_paralelo/R3

---

## 8. Análisis de Error y Conclusiones

### Fuentes de Error Típicas:
- **Tolerancia de resistencias:** ±5% en valores comerciales
- **Resistencia interna de la batería:** Reduce tensión bajo carga
- **Resistencia de contactos:** Protoboard y cables
- **Precisión del multímetro:** Error instrumental
- **Temperatura:** Afecta valor de resistencias

### Conclusiones:
1. Los valores medidos deben estar dentro del ±10% de los calculados
2. La Ley de Ohm se cumple satisfactoriamente en los circuitos resistivos
3. Las leyes de Kirchhoff (tensiones y corrientes) se verifican experimentalmente
4. La simulación proporciona valores ideales muy cercanos a los teóricos

---

## 9. Instrucciones para Montaje y Medición

### Pasos para el Montaje:
1. **Verificar valores de resistencias** con multímetro antes del montaje
2. **Armar circuito en protoboard** siguiendo el diagrama
3. **Verificar continuidad** antes de conectar la fuente
4. **Medir tensión de la fuente** sin carga
5. **Conectar fuente y medir:**
   - Corriente total (serie con amperímetro)
   - Tensiones individuales (voltímetro en paralelo)
6. **Documentar con fotografías** claras y nítidas

### Notas Importantes:
- Usar cables de colores para facilitar identificación
- Mantener conexiones firmes y limpias  
- Verificar polaridad de la fuente DC
- Tomar múltiples mediciones para mayor precisión