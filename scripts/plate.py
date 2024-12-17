#! /usr/bin/env python3

x=40
y=43
z=2

tool_diameter = 6
overlap_percentage = 0.75
v_feed = 200
h_feed = 700

y_pass_len = y + ( 1 * tool_diameter )

x_pass_len = tool_diameter * overlap_percentage

full_passes = int(x // x_pass_len)
last_pass  = x % x_pass_len

remainder = x
gcode = [
        '%',
        f"(Tool diameter: {tool_diameter}mm, step: {x_pass_len}mm)",
        f"(Z cut depth: {z}mm; Face dimension: {x}x{y})",
        '#<_start_x> = #<_x>',
        '#<_start_y> = #<_y>',
        '#<_start_z> = #<_z>',
        'G91',
        f"G1 F{v_feed} Z-{z}",
        f"F{h_feed}"
        ]

remains_passes = full_passes

#First cutter pass aways left and always exists
gcode.append(f"G1 X-{x_pass_len}")
gcode.append(f"G1 Y-{y_pass_len}")
left = False
remains_passes -= 1

while remains_passes:
    if left:
        sign = '-'
        left = False
    else:
        sign = ''
        left = True

    gcode.append(f"G1 X-{x_pass_len}")
    gcode.append(f"G1 Y{sign}{y_pass_len}")
    remains_passes -= 1

if last_pass > 0:
    if left:
        sign = '-'
        left = False
    else:
        sign = ''
        left = True

    gcode.append("(Last pass)")
    gcode.append(f"G1 X-{last_pass}")
    gcode.append(f"G1 Y{sign}{y_pass_len}")


gcode.append(f"G0 Z{z+2}")
gcode.append("G90")
gcode.append("G0 X#<_start_x> Y#<_start_y>")
gcode.append("G0 Z#<_start_z>")
gcode.append(f"G1 G91 F{v_feed} Z-{z}")
gcode.append("G90")
gcode.append("%")

for line in gcode:
    print(line)




