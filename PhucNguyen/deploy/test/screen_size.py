# import subprocess


# def get_screen_resolution():
#     output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',
#                               shell=True, stdout=subprocess.PIPE).communicate()[0]
#     resolution = output.split()[0].split(b'x')
#     return {'width': resolution[0], 'height': resolution[1]}


# print(get_screen_resolution())

from Xlib.display import Display
screen = Display(':0').screen()
print(screen.width_in_pixels, screen.height_in_pixels)
