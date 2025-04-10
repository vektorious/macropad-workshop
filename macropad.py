# macropad.py
# Dieses Script steuert das Macropad mit OLED-Anzeige und verschiedenen Modi
# Es wird automatisch ausgeführt, wenn es als "code.py" oder "main.py" auf dem CIRCUITPY-Laufwerk liegt

import board                      # Zugriff auf die GPIO-Pins
import busio                      # Für I2C-Kommunikation
import time                       # Für Pausen und Zeitsteuerung
import usb_hid                    # Um HID-Geräte (z.B. Tastatur) zu emulieren
import digitalio                  # Für digitale Ein- und Ausgänge
import adafruit_ssd1306          # OLED-Display-Bibliothek

from adafruit_hid.keyboard import Keyboard

# Standard US-Layout:
#from adafruit_hid.keycode import Keycode
#from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout

# Wenn du ein deutsches Layout verwendest, importiere diese:
from keyboard_layout_win_de import KeyboardLayout
from keycode_win_de import Keycode

# Tastenbelegung: welche GPIOs mit Buttons verbunden sind
BTN1_PIN = board.GP6
BTN2_PIN = board.GP8
BTN3_PIN = board.GP11
BTN4_PIN = board.GP7
BTN5_PIN = board.GP10
BTN6_PIN = board.GP12

# Buttons initialisieren
buttons = []
for pin in [BTN1_PIN, BTN2_PIN, BTN3_PIN, BTN4_PIN, BTN5_PIN, BTN6_PIN]:
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.DOWN
    buttons.append(btn)

# OLED-Anzeige initialisieren (128x32 Pixel)
WIDTH = 128
HEIGHT = 32
i2c = busio.I2C(scl=board.GP5, sda=board.GP4)
display = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Zustände für Taster
BTN_DOWN = 1
BTN_UP = 0
lastState = BTN_UP

# Hier kannst du deine Modi und Tastenbelegungen ändern
modes = [
    ['Teams', 'Search', 'Goto', 'Toggle mute', 'Toggle camera', 'Hangup'],
    ['VS Code', 'Explorer', 'Problems', 'Search', 'Debug', 'Output'],
    ['Git', 'Branch..', 'Checkout main', 'Status', 'Push', 'Pull origin main']
]

# Konstanten für Modus-Zuweisung
MODE_TEAMS = 0
MODE_VSCODE = 1
MODE_GIT = 2
COUNT_OF_MODES = 3
currentMode = MODE_GIT  # Startmodus

# Tastatur initialisieren
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayout(keyboard)


# Funktion zur Anzeige auf dem Display
def draw_screen(text, x, y):
    display.fill(0)
    display.text(text, x, y, 1)
    display.text("Modus: " + modes[currentMode][0], 24, 12, 1)
    display.text("Pad v1.0", 24, 24, 1)
    display.show()


# Hier legst du die Tastenkombinationen für jede Taste in jedem Modus fest
def handle_mode_press(mode, key):
    if mode == MODE_TEAMS:
        if key == 1:
            keyboard.send(Keycode.LEFT_CONTROL, Keycode.E)
        elif key == 2:
            keyboard.send(Keycode.LEFT_CONTROL, Keycode.G)
        elif key == 3:
            keyboard.send(Keycode.LEFT_CONTROL, Keycode.SHIFT, Keycode.M)
        elif key == 4:
            keyboard.send(Keycode.LEFT_CONTROL, Keycode.SHIFT, Keycode.O)
        elif key == 5:
            keyboard.send(Keycode.LEFT_CONTROL, Keycode.SHIFT, Keycode.B)

    elif mode == MODE_VSCODE:
        if key == 1:
            keyboard.send(Keycode.LEFT_CONTROL, Keycode.SHIFT, Keycode.E)
        elif key == 2:
            keyboard.send(Keycode.LEFT_CONTROL, Keycode.SHIFT, Keycode.M)
        elif key == 3:
            keyboard.send(Keycode.LEFT_CONTROL, Keycode.SHIFT, Keycode.F)
        elif key == 4:
            keyboard.send(Keycode.F5)
        elif key == 5:
            keyboard.send(Keycode.LEFT_CONTROL, Keycode.SHIFT, Keycode.U)

    elif mode == MODE_GIT:
        if key == 1:
            layout.write('git branch -b ')
        elif key == 2:
            layout.write('git checkout main\n')
        elif key == 3:
            layout.write('git status\n')
        elif key == 4:
            layout.write('git push\n')
        elif key == 5:
            layout.write('git pull origin main\n')


# Funktion, die Tasten prüft und entsprechend reagiert
def buttonPress(last):
    global currentMode
    tempLast = last
    nextState = last
    text = ""

    # Taste 1 = Modus wechseln
    if tempLast == BTN_UP and buttons[0].value:
        nextState = BTN_DOWN
        currentMode = (currentMode + 1) % COUNT_OF_MODES
        draw_screen("", 1, 1)

    # Tasten 2–6 = Funktion ausführen
    for i in range(1, 6):
        if tempLast == BTN_UP and buttons[i].value:
            nextState = BTN_DOWN
            text = modes[currentMode][i]
            draw_screen(text, 1, 1)
            handle_mode_press(currentMode, i)
            time.sleep(0.25)

    # Wenn keine Taste gedrückt ist, Status zurücksetzen
    if tempLast == BTN_DOWN and not any(btn.value for btn in buttons):
        nextState = BTN_UP
        draw_screen("", 1, 1)

    return nextState


# Initiale Anzeige
draw_screen("", 1, 1)


# Hauptschleife
while True:
    lastState = buttonPress(lastState)
