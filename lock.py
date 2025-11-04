import os

# Trigger macOS lock screen
os.system('osascript -e \'tell application "System Events" to keystroke "q" using {control down, command down}\'')