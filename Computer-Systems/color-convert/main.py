import re


def hex_to_rgb(hexString):
    hexString = hexString.lstrip('#')
    colorsArray = hexString_to_rgbList(hexString)
    rgbString = " ".join(str(x) for x in colorsArray[0:3])

    if (len(colorsArray) > 3):
        rgbString += f" / {colorsArray[3]}"
        return f'rgba({rgbString})'
    return f'rgb({rgbString})'


def hexString_to_rgbList(hexString):
    if (len(hexString) <= 4):
        hexString = "".join([f'{s}{s}' for s in hexString])

    result = [int(hexString[i:i+2], 16) for i in (0, 2, 4)]
    if (len(hexString) == 8):
        alpha = int(hexString[6:], 16) / 255
        alpha = round(alpha, 5)
        result.append(alpha)
    return result


def converted_css(original_css):
    return re.sub(r'#[a-fA-F0-9]{3,}', lambda match: hex_to_rgb(match.group()),
                  original_css)


filename = 'advanced'
with open(f'{filename}.css') as file:
    contents = file.read()
    with open(f'{filename}_result.css', 'w') as f:
        f.write(converted_css(contents))
