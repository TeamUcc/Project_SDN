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


# Ejercicio Mixto 1

**R1 = 1 kΩ** en serie con el **paralelo** de **R2 = 470 Ω** y **R3 = 680 Ω**. **V = 9 V**.

**1) Equivalentes**

* $R_{23}=\left(\frac{1}{470}+\frac{1}{680}\right)^{-1}= \mathbf{278\ \Omega}$
* $R_{eq}=R_1+R_{23}=1000+277.913=\mathbf{1.28\ k\Omega}$

**2) Corriente total**

* $I_T=\dfrac{9}{1277.913}=\mathbf{7.04\ mA}$

**3) Tensiones**

* $V_{R1}=I_T\,R_1= \mathbf{7.04\ V}$
* $V_{R23}=I_T\,R_{23}= \mathbf{1.96\ V}$  (igual en R2 y R3 por estar en paralelo)

**4) Corrientes de rama**

* $I_2=\dfrac{1.957}{470}= \mathbf{4.16\ mA}$
* $I_3=\dfrac{1.957}{680}= \mathbf{2.88\ mA}$
  (Chequeo: $I_2+I_3 \approx I_T$)

**5) Potencias**

* $P_1=\dfrac{V_{R1}^2}{R_1}= \mathbf{49.6\ mW}$
* $P_2=\dfrac{1.957^2}{470}= \mathbf{8.15\ mW}$
* $P_3=\dfrac{1.957^2}{680}= \mathbf{5.63\ mW}$
* $P_T=V\,I_T= \mathbf{63.4\ mW}$ (≈ $P_1+P_2+P_3$)

> Todas las resistencias trabajan holgadas con ¼ W.

---

# Ejercicio Mixto 2

**R1 = 220 Ω** en **paralelo** con **R2 = 330 Ω**; ese bloque en **serie** con el **paralelo** de **R3 = 1 kΩ** y **R4 = 2.2 kΩ**. **V = 9 V**.

**1) Equivalentes de bloques**

* $R_{12}=\left(\frac{1}{220}+\frac{1}{330}\right)^{-1}= \mathbf{132\ \Omega}$
* $R_{34}=\left(\frac{1}{1000}+\frac{1}{2200}\right)^{-1}= \mathbf{687.5\ \Omega}$
* $R_{eq}=R_{12}+R_{34}= \mathbf{819.5\ \Omega}$

**2) Corriente total**

* $I_T=\dfrac{9}{819.5}= \mathbf{10.98\ mA}$

**3) Tensiones de bloque**

* $V_{12}=I_T\,R_{12}= \mathbf{1.45\ V}$ (misma en R1 y R2)
* $V_{34}=I_T\,R_{34}= \mathbf{7.55\ V}$ (misma en R3 y R4)

**4) Corrientes de cada resistor**

* $I_1=\dfrac{1.45}{220}= \mathbf{6.59\ mA}$
* $I_2=\dfrac{1.45}{330}= \mathbf{4.39\ mA}$
* $I_3=\dfrac{7.55}{1000}= \mathbf{7.55\ mA}$
* $I_4=\dfrac{7.55}{2200}= \mathbf{3.43\ mA}$
  (Chequeos: $I_1+I_2=I_T$ y $I_3+I_4=I_T$)

**5) Potencias**

* $P_1=\dfrac{1.45^2}{220}= \mathbf{9.55\ mW}$
* $P_2=\dfrac{1.45^2}{330}= \mathbf{6.37\ mW}$
* $P_3=\dfrac{7.55^2}{1000}= \mathbf{57.0\ mW}$
* $P_4=\dfrac{7.55^2}{2200}= \mathbf{25.9\ mW}$
* $P_T=V\,I_T= \mathbf{98.8\ mW}$ (≈ suma de potencias)

> Máxima disipación ≈ **57 mW** en R3 → ¼ W sigue siendo seguro.




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
