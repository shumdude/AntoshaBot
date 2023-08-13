"""https://github.com/Ruslanch0s/qrgenerator"""

import qrcode
from PIL import Image, ImageDraw
from pyzbar.pyzbar import decode
from path import Path
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask, ImageColorMask


# Путь до картинки с QR кодом
def read_qr_code(path_to_download: Path):
    try:
        img = Image.open(path_to_download)
        decoded = decode(img)
        wrote = decoded[0].data.decode("utf-8")
    except:
        wrote = None
    return wrote


def gen_qr_code(text: str, path_to_download: Path, path_to_save: Path = None) -> bool:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.get_matrix()

    coeff = 20  # height * width
    coeff_small = round(coeff / 3)
    length_qr = len(img) * coeff

    try:
        background = Image.open(path_to_download).resize((length_qr, length_qr)).convert("RGBA")
    except:
        return False

    back_im = Image.new('RGBA', (length_qr, length_qr), (0, 0, 0, 0))
    idraw = ImageDraw.Draw(back_im, "RGBA")

    # Colors
    black_1 = (0, 0, 0, 0)
    black_2 = (0, 0, 0, 230)
    white_1 = (255, 255, 255, 50)
    white_2 = (255, 255, 255, 230)
    yellow_1 = (255, 255, 0, 230)
    blue_1 = (0, 0, 255, 230)
    green_1 = (0, 255, 0, 230)
    sirenev_1 = (185, 255, 255, 230)
    white_3 = (0, 0, 0, 0)

    fill_1 = blue_1
    fill_0 = white_2

    x, y = 0, 0
    for string in qr.get_matrix():
        this_str = ''
        for i in string:
            if i:
                this_str += '1'
                # idraw.ellipse((x + coeff_small, y + coeff_small, x + coeff - coeff_small, y + coeff - coeff_small),
                #               fill=fill_1)

                # idraw.rectangle((x, y, x + coeff, y + coeff), fill=fill_1)

                idraw.rectangle((x + coeff_small, y + coeff_small, x + coeff - coeff_small, y + coeff - coeff_small),
                                fill=fill_1)
            else:
                this_str += '0'
                # idraw.ellipse((x + coeff_small, y + coeff_small, x + coeff - coeff_small, y + coeff - coeff_small),
                #               fill=fill_0)
                # idraw.rectangle((x, y, x + coeff, y + coeff), fill=fill_0)
                idraw.rectangle((x + coeff_small, y + coeff_small, x + coeff - coeff_small, y + coeff - coeff_small),
                                fill=fill_0)
            x += coeff
        x = 0
        y += coeff

    fill_back = white_1
    fill_rectangle = black_2

    # BACK
    idraw.rectangle((0, 0, coeff * 9, coeff * 9), fill=fill_back)
    idraw.rectangle((length_qr - coeff * 9, 0, length_qr, coeff * 9), fill=fill_back)
    idraw.rectangle((0, length_qr - coeff * 9, coeff * 9, length_qr), fill=fill_back)
    idraw.rectangle((length_qr - coeff * 10, length_qr - coeff * 9, length_qr - coeff * 6, length_qr - coeff * 6),
                    fill=fill_back)

    # LEFT UP
    idraw.rectangle((coeff, coeff, coeff * 8, coeff * 2), fill=fill_rectangle)
    idraw.rectangle((coeff * 3, coeff * 3, coeff * 6, coeff * 6), fill=fill_rectangle)
    idraw.rectangle((coeff, coeff, coeff * 2, coeff * 8), fill=fill_rectangle)
    idraw.rectangle((coeff * 7, coeff, coeff * 8, coeff * 8), fill=fill_rectangle)
    idraw.rectangle((coeff, coeff * 7, coeff * 8, coeff * 8), fill=fill_rectangle)

    # RIGHT UP
    idraw.rectangle((length_qr - coeff * 8, coeff, length_qr - coeff, coeff * 2), fill=fill_rectangle)
    idraw.rectangle((length_qr - coeff * 8, coeff * 7, length_qr - coeff, coeff * 8), fill=fill_rectangle)
    idraw.rectangle((length_qr - coeff * 6, coeff * 3, length_qr - coeff * 3, coeff * 6), fill=fill_rectangle)
    idraw.rectangle((length_qr - coeff * 2, coeff, length_qr - coeff, coeff * 8), fill=fill_rectangle)
    idraw.rectangle((length_qr - coeff * 8, coeff, length_qr - coeff * 7, coeff * 8), fill=fill_rectangle)

    # LEFT DOWN
    idraw.rectangle((coeff, length_qr - coeff * 8, coeff * 8, length_qr - coeff * 7), fill=fill_rectangle)
    idraw.rectangle((coeff, length_qr - coeff * 2, coeff * 8, length_qr - coeff), fill=fill_rectangle)
    idraw.rectangle((coeff, length_qr - coeff * 8, coeff * 2, length_qr - coeff), fill=fill_rectangle)
    idraw.rectangle((coeff * 7, length_qr - coeff * 8, coeff * 8, length_qr - coeff), fill=fill_rectangle)
    idraw.rectangle((coeff * 3, length_qr - coeff * 6, coeff * 6, length_qr - coeff * 3), fill=fill_rectangle)

    # RIGHT DOWN
    idraw.rectangle((length_qr - coeff * 10, length_qr - coeff * 10, length_qr - coeff * 9, length_qr - coeff * 5),
                    fill=fill_rectangle)
    idraw.rectangle((length_qr - coeff * 6, length_qr - coeff * 10, length_qr - coeff * 5, length_qr - coeff * 5),
                    fill=fill_rectangle)
    idraw.rectangle((length_qr - coeff * 8, length_qr - coeff * 8, length_qr - coeff * 7, length_qr - coeff * 7),
                    fill=fill_rectangle)
    idraw.rectangle((length_qr - coeff * 10, length_qr - coeff * 10, length_qr - coeff * 6, length_qr - coeff * 9),
                    fill=fill_rectangle)
    idraw.rectangle((length_qr - coeff * 10, length_qr - coeff * 6, length_qr - coeff * 6, length_qr - coeff * 5),
                    fill=fill_rectangle)

    background.paste(back_im, (0, 0), back_im)
    if path_to_save is not None:
        path_to_download = path_to_save
    background.save(path_to_download)
    return True


def generate_qr_code(text: str, path_to_download: Path, path_to_save: Path = None):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(text)
    img_6 = qr.make_image(image_factory=StyledPilImage,
                          color_mask=ImageColorMask(color_mask_path=path_to_download),
                          module_drawer=RoundedModuleDrawer())
    img_6.save(path_to_save)
