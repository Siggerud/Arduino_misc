from pynput.keyboard import Key, Listener

def on_press(key):
    print('\nHolding {0}'.format( key))
    if key == Key.delete:
        return False
    
def on_release(key):
    print('\nReleasing {0}'.format( key))
		
with Listener(on_press = on_press, on_release=on_release) as listener:
    listener.join()