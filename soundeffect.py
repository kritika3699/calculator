
import tkinter as tk
import re
import winsound

# =========================
# WINDOW
# =========================

root = tk.Tk()
root.title("Neon Calculator")
root.geometry("380x650")
root.resizable(False, False)
root.configure(bg="#0b0b12")

# =========================
# COLORS
# =========================

BG_COLORS = [
    "#0b0b12",
    "#0c0b18",
    "#100b1c",
    "#0b101c",
    "#0b1418"
]

NEON_COLORS = [
    "#8A2BE2",
    "#00BFFF",
    "#FF1493",
    "#00FA9A",
    "#7C4DFF"
]

accent_index = 0
bg_index = 0

# =========================
# BUTTON CLICK SOUND
# =========================

def click_sound():
    try:
        winsound.Beep(850, 35)
    except:
        pass


# =========================
# DISPLAY
# =========================

display_var = tk.StringVar()

display = tk.Entry(
    root,
    textvariable=display_var,
    font=("Arial", 36, "bold"),
    bg="#0b0b12",
    fg="white",
    insertbackground="white",
    bd=0,
    justify="right"
)

display.pack(
    fill="x",
    padx=25,
    pady=(45, 20),
    ipady=20
)

# =========================
# BUTTON FRAME
# =========================

button_frame = tk.Frame(
    root,
    bg="#0b0b12"
)

button_frame.pack(
    expand=True,
    fill="both",
    padx=15,
    pady=10
)

# =========================
# CALCULATOR FUNCTIONS
# =========================

def press(value):

    click_sound()

    current = display_var.get()

    if value == ".":

        parts = re.split(
            r'[+\-×÷]',
            current
        )

        if "." in parts[-1]:
            return

    if value in "+-×÷":

        if not current:
            return

        if current[-1] in "+-×÷":
            current = current[:-1]

    display_var.set(
        current + value
    )


def clear():

    click_sound()
    display_var.set("")


def backspace():

    click_sound()

    current = display_var.get()
    display_var.set(
        current[:-1]
    )


def plus_minus():

    click_sound()

    current = display_var.get()

    if not current:
        return

    match = re.search(
        r'(-?\d*\.?\d+)$',
        current
    )

    if match:

        number = match.group(0)
        start = match.start()

        if number.startswith("-"):
            new_number = number[1:]
        else:
            new_number = "-" + number

        display_var.set(
            current[:start] + new_number
        )


def percentage():

    click_sound()

    current = display_var.get()

    match = re.search(
        r'(-?\d*\.?\d+)$',
        current
    )

    if match:

        number = match.group(0)
        start = match.start()

        try:

            result = float(number) / 100

            if result.is_integer():
                result = int(result)

            display_var.set(
                current[:start] + str(result)
            )

        except:
            pass


def calculate():

    click_sound()

    expression = display_var.get()

    if not expression:
        return

    try:

        expression = expression.replace(
            "×", "*"
        )

        expression = expression.replace(
            "÷", "/"
        )

        if not re.fullmatch(
            r'[0-9+\-*/(). ]+',
            expression
        ):
            raise ValueError

        result = eval(
            expression,
            {"__builtins__": None},
            {}
        )

        if (
            isinstance(result, float)
            and result.is_integer()
        ):
            result = int(result)

        display_var.set(
            str(result)
        )

        animate_result()

    except ZeroDivisionError:

        display_var.set(
            "Cannot divide by 0"
        )

    except:

        display_var.set(
            "Error"
        )


# =========================
# RESULT ANIMATION
# =========================

def animate_result():

    sizes = [40, 44, 40, 36]

    def animation(i=0):

        if i < len(sizes):

            display.config(
                font=(
                    "Arial",
                    sizes[i],
                    "bold"
                )
            )

            root.after(
                60,
                lambda: animation(i + 1)
            )

    animation()


# =========================
# BUTTON EFFECTS
# =========================

def hover_enter(button):

    button.config(
        relief="sunken"
    )


def hover_leave(button):

    button.config(
        relief="flat"
    )


def click_animation(
    button,
    original_color
):

    button.config(
        bg="white",
        fg=original_color
    )

    root.after(
        100,
        lambda: button.config(
            bg=original_color,
            fg="white"
        )
    )


# =========================
# CREATE BUTTON
# =========================

buttons = []


def create_button(
    text,
    row,
    column,
    command,
    bg,
    colspan=1
):

    button = tk.Button(
        button_frame,
        text=text,
        command=lambda: button_click(
            button,
            command,
            bg
        ),
        font=(
            "Arial",
            19,
            "bold"
        ),
        bg=bg,
        fg="white",
        activeforeground="white",
        activebackground=bg,
        bd=0,
        relief="flat",
        cursor="hand2"
    )

    button.grid(
        row=row,
        column=column,
        columnspan=colspan,
        sticky="nsew",
        padx=6,
        pady=6
    )

    button.bind(
        "<Enter>",
        lambda e: hover_enter(button)
    )

    button.bind(
        "<Leave>",
        lambda e: hover_leave(button)
    )

    buttons.append(
        (button, bg)
    )

    return button


def button_click(
    button,
    command,
    color
):

    # Visual click
    click_animation(
        button,
        color
    )

    # Run button command
    command()


# =========================
# BUTTON COLORS
# =========================

NUMBER = "#252532"
FUNCTION = "#5A5A68"
OPERATOR = "#8A2BE2"

# =========================
# BUTTONS
# =========================

create_button(
    "AC", 0, 0,
    clear,
    FUNCTION
)

create_button(
    "⌫", 0, 1,
    backspace,
    FUNCTION
)

create_button(
    "%", 0, 2,
    percentage,
    FUNCTION
)

create_button(
    "÷", 0, 3,
    lambda: press("÷"),
    OPERATOR
)


create_button(
    "7", 1, 0,
    lambda: press("7"),
    NUMBER
)

create_button(
    "8", 1, 1,
    lambda: press("8"),
    NUMBER
)

create_button(
    "9", 1, 2,
    lambda: press("9"),
    NUMBER
)

create_button(
    "×", 1, 3,
    lambda: press("×"),
    OPERATOR
)


create_button(
    "4", 2, 0,
    lambda: press("4"),
    NUMBER
)

create_button(
    "5", 2, 1,
    lambda: press("5"),
    NUMBER
)

create_button(
    "6", 2, 2,
    lambda: press("6"),
    NUMBER
)

create_button(
    "−", 2, 3,
    lambda: press("-"),
    OPERATOR
)


create_button(
    "1", 3, 0,
    lambda: press("1"),
    NUMBER
)

create_button(
    "2", 3, 1,
    lambda: press("2"),
    NUMBER
)

create_button(
    "3", 3, 2,
    lambda: press("3"),
    NUMBER
)

create_button(
    "+", 3, 3,
    lambda: press("+"),
    OPERATOR
)


create_button(
    "+/−", 4, 0,
    plus_minus,
    FUNCTION
)

create_button(
    "0", 4, 1,
    lambda: press("0"),
    NUMBER
)

create_button(
    ".", 4, 2,
    lambda: press("."),
    NUMBER
)

create_button(
    "=", 4, 3,
    calculate,
    OPERATOR
)

# =========================
# GRID
# =========================

for row in range(5):

    button_frame.rowconfigure(
        row,
        weight=1
    )

for column in range(4):

    button_frame.columnconfigure(
        column,
        weight=1
    )

# =========================
# BACKGROUND ANIMATION
# =========================

def animate_background():

    global bg_index

    color = BG_COLORS[bg_index]

    root.configure(
        bg=color
    )

    button_frame.configure(
        bg=color
    )

    display.configure(
        bg=color
    )

    bg_index = (
        bg_index + 1
    ) % len(BG_COLORS)

    root.after(
        1000,
        animate_background
    )


# =========================
# NEON COLOR ANIMATION
# =========================

def animate_neon():

    global accent_index

    color = NEON_COLORS[
        accent_index
    ]

    for button, original in buttons:

        if original == OPERATOR:

            button.config(
                bg=color,
                activebackground=color
            )

    accent_index = (
        accent_index + 1
    ) % len(NEON_COLORS)

    root.after(
        700,
        animate_neon
    )


# =========================
# KEYBOARD SUPPORT
# =========================

def keyboard_input(event):

    key = event.keysym
    char = event.char

    if char in "0123456789":
        press(char)

    elif char == ".":
        press(".")

    elif char == "+":
        press("+")

    elif char == "-":
        press("-")

    elif char == "*":
        press("×")

    elif char == "/":
        press("÷")

    elif key in ("Return", "equal"):
        calculate()

    elif key == "BackSpace":
        backspace()

    elif key == "Escape":
        clear()


root.bind(
    "<Key>",
    keyboard_input
)

# =========================
# START
# =========================

animate_background()
animate_neon()

root.focus_set()

root.mainloop()
