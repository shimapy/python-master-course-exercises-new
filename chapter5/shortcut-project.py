from pynput import keyboard
    
with open ( "./sample.txt", "a+") as file:
    file.write("WOOOW! a new file created !")

def on_activate_D():
    print('<ctrl>+<alt>+D pressed')
    with open("sample.txt", "r") as file:    
        print(file.read())
        file.close()

def on_activate_H():
    print('<ctrl>+<alt>+H pressed')
    with open("sample.txt", "w") as file:
        file.write("content edited!")
        file.close()


with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+D': on_activate_D,
        '<ctrl>+<alt>+H': on_activate_H}) as h:
    h.join()    
    