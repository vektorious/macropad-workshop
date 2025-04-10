# Macropad Workshop

Dieses Projekt zeigt dir, wie du mit einem Raspberry Pi Pico und CircuitPython ein Macropad mit OLED-Anzeige
und mehreren Modi baust. Der Workshop ist so aufgebaut, dass du jeden Schritt selbst nachvollziehen und eigene 
Anpassungen vornehmen kannst.

---

## Schritt-für-Schritt-Anleitung

Diese Anleitung führt dich durch den Aufbau eines eigenen Macropads mit einem Raspberry Pi Pico. 
Ziel ist es, nicht nur ein fertiges Gerät zu bauen, sondern auch die einzelnen Elemente kennenzulernen und später 
selbst weiterzuentwickeln.

---

### Schritt 1: Vorbereitungen

**Thonny installieren**  
Thonny ist eine einfache Python-IDE, ideal für Einsteiger und Bildungszwecke.  
Download: [https://thonny.org](https://thonny.org)

**CircuitPython auf dem Pico installieren**  
1. Lade die passende Firmware (UF2-Datei) von [https://circuitpython.org/downloads](https://circuitpython.org/downloads):
   - [Pico W](https://circuitpython.org/board/raspberry_pi_pico_w/)
   - [Pico2 W](https://circuitpython.org/board/raspberry_pi_pico2_w/)
2. Falls bereits Firmware installiert ist, halte beim Einstecken des Pico die **BOOTSEL-Taste** gedrückt (sonst nicht nötig).
3. Ziehe die UF2-Datei auf das Laufwerk das erscheint (z.B. RPI-RP2).
4. Nach einer Weile erschein das Laufwerk `CIRCUITPY` – damit ist jetzt Circuitpython installiert.

---

### Schritt 2: Erste Tests in Thonny

1. Öffne Thonny, wähle unter "Interpreter" den Raspberry Pi Pico (CircuitPython).
2. Test in der "Shell"
    ```python
    print("Hello World!")
    ```
3. Lass die interne LED blinken:
Kopiere den folgenden Code in die Datei "code.py" auf deinem RPi Pico in Thonny und führe sie aus
    ```python
    import time
    import board
    import digitalio

    led = digitalio.DigitalInOut(board.LED)
    led.direction = digitalio.Direction.OUTPUT

    while True:
        led.value = True
        time.sleep(0.5)
        led.value = False
        time.sleep(0.5)
    ```
---

### Schritt 3: Buttons anschließen und testen

**GPIOs für Buttons (in diesem Projekt):** GP6, GP8, GP11, GP7, GP10, GP12

**Testcode:**
```python
import board
import digitalio
import time

pins = [board.GP6, board.GP8, board.GP11, board.GP7, board.GP10, board.GP12]
buttons = []

for pin in pins:
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    buttons.append(btn)

while True:
    for i, btn in enumerate(buttons):
        if btn.value == False:
            print(f"Button {i+1} pressed")
    time.sleep(0.1)
```

---

### Schritt 4: Tastatur-Signale über USB senden

1. Lade die `adafruit-circuitpython-hid` library:  
   [HID auf GitHub](https://github.com/adafruit/Adafruit_CircuitPython_HID/releases)

2. Entpacke das ZIP, kopiere den Inhalt des `lib/`-Ordners in den `lib/`-Ordner auf dem CIRCUITPY-Laufwerk.

3. Testcode:
    ```python
    import usb_hid
    from adafruit_hid.keyboard import Keyboard
    from adafruit_hid.keycode import Keycode

    keyboard = Keyboard(usb_hid.devices)
    keyboard.send(Keycode.A)
    ```

---

### Optional: Deutsches Tastaturlayout verwenden

Standardmäßig nutzt CircuitPython das US-Tastaturlayout. Wenn du aber auf einem deutschen Windows-System arbeitest, kannst du ein passendes Layout nachrüsten. Dafür gibt es eine Erweiterung von [Neradoc](https://github.com/Neradoc/Circuitpython_Keyboard_Layouts), die alternative Layouts bereitstellt.

#### Installation des deutschen Windows-Layouts

1. Lade die aktuelle Version der Layout-library von hier herunter:  
   [https://github.com/Neradoc/Circuitpython_Keyboard_Layouts/releases](https://github.com/Neradoc/Circuitpython_Keyboard_Layouts/releases)

2. Entpacke die ZIP-Datei.

3. Kopiere **nur** diese beiden Dateien in den `lib/`-Ordner auf deinem CIRCUITPY-Laufwerk:
   - `keycode_win_de.py`
   - `keyboard_layout_win_de.py`

#### Verwendung im Code

Ersetze den Import des US-Layouts durch:

```python
from keyboard_layout_win_de import KeyboardLayout
from keycode_win_de import Keycode
```

Hier ist ein Beispiel script das nach einem 10 Sekunden Delay einen Text schreibt.

```python
import usb_hid
import time
from adafruit_hid.keyboard import Keyboard
from keyboard_layout_win_de import KeyboardLayout
from keycode_win_de import Keycode

keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayout(keyboard)

time.sleep(10)
layout.write("Viele Grüße und bis bald")
```

### Schritt 5: OLED-Display anschließen und testen

**I2C-Anschluss:**
- SDA = GP4
- SCL = GP5

1. Lade die libraries 
   - [adafruit_ssd1306](https://github.com/adafruit/Adafruit_CircuitPython_SSD1306/releases) (adafruit-circuitpython-ssd1306-py-x.x.x.zip)
   - [adafruit_framebuf](https://github.com/adafruit/Adafruit_CircuitPython_framebuf/releases) (adafruit-circuitpython-framebuf-py-x.x.x.zip)
   - Schriftart Binaries: [font5x8.bin](https://github.com/adafruit/Adafruit_CircuitPython_framebuf/blob/main/examples/font5x8.bin)
2. Entpacke die libaries und transferiere sie in den lib Ordner wie zuvor. Die Schrift kann ins toplevel.
3. Beispielcode:
    ```python
    import board
    import busio
    import adafruit_ssd1306

    i2c = busio.I2C(scl=board.GP5, sda=board.GP4)
    display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

    display.fill(0)
    display.text("Hallo OLED!", 0, 0, 1)
    display.show()
    ```

---

### Schritt 6: Modus-Wechsel und Funktionstasten

Jetzt kombinieren wir alles:

- Taste 1: Modi wechseln (z.B. Git, VS Code, Teams)
- Tasten 2–6: Aktionen je nach Modus ausführen
- OLED zeigt den Modus und die Funktion der Taste

---

### Schritt 7: Finales Script (anpassbar)

Das vollständige Script findest du in der Datei `code/macropad.py`.

Hier einige Hinweise, wo du es leicht anpassen kannst:

```python
# Tastenzuordnung (GPIOs ändern)
BTN1_PIN = board.GP6
...

# Modi und Tastenfunktionen anpassen
modes = [
    ['Teams', 'Search', 'Goto', 'Mute', 'Camera', 'Hangup'],
    ['VS Code', 'Explorer', 'Problems', 'Search', 'Debug', 'Output'],
    ['Git', 'Branch..', 'Checkout main', 'Status', 'Push', 'Pull']
]

# Hier definierst du, was bei jedem Tastendruck passiert
def handle_mode_press(mode, key):
    if mode == MODE_GIT:
        if key == 1:
            layout.write('git branch -b ')
        elif key == 2:
            layout.write('git checkout main\n')
        ...
```

**Was lässt sich leicht anpassen:**
- Eigene Tastenkombinationen
- Neue Modi hinzufügen oder bestehende löschen
- Displayausgabe personalisieren
- Buttonbelegung ändern, z.B. bei anderer Hardware

---

## Lizenz

Dieser Workshop basiert auf der Idee von 
[codeof.me/pikku](https://www.codeof.me/pikku-raspberry-pi-pico-powered-macropad/) 
([GitHub Repository](https://github.com/tlaukkanen/pikku-macropad)) und wurde entsprechend aufbereitet.

Der Inhalt dieses Repositories ist unter der GPL-3.0 lizenziert (siehe LICENSE.md) 
****


# Setup in English

## Install Thonny
Thonny is a Python IDE for beginners that's especially nice for educational purposes.
Download it from the [Thonny webpage](https://thonny.org/).

## Install Circuit Python
1. Download the latest firmware (UF2 file) from Adafruit.
   - [Pico W](https://circuitpython.org/board/raspberry_pi_pico_w/)
   - [Pico2 W](https://circuitpython.org/board/raspberry_pi_pico2_w/)
   - or search the [circuit python website](https://circuitpython.org/downloads)
2. Plug-in the Pico board. If there is already a firmware on the board, you have to press (and keep pressing) the BOOTSEL button while you plug it in.
3. A folder called RPxxx should appear. Drag and drop the firmware (UF2) file into this folder and wait.
4. After a while the RPxxx folder disappears and a CIRCUITPY folder appears.

## Get the necessary libraries
1. Download the latest version of [Adafruit CircuitPython](https://github.com/adafruit/Adafruit_CircuitPython_HID/releases)
   - get the adafruit-circuitpython-hid-py-x.x.x.zip file and unpack it
2. Download the latest version of [Adafruit SSD1306](https://github.com/adafruit/Adafruit_CircuitPython_SSD1306/releases)
   - get the adafruit-circuitpython-ssd1306-py-x.x.x.zip file and unpack it#
3. Download the latest version of [Adafruit CircuitPython Framebuffer](https://github.com/adafruit/Adafruit_CircuitPython_framebuf/releases)
   - get the adafruit-circuitpython-framebuf-py-x.x.x.zip file and unpack it#
4. "Install" the libraries by uploading the content of the lib folder to the board lib folder through the Thonny IDE
5. Check if everything is working by entering and executing these command in the interactive shell:
    ```{python}
   from adafruit_hid.keyboard import Keyboard
   import adafruit_ssd1306
   ```


