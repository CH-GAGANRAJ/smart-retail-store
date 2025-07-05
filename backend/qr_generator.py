import qrcode
from io import BytesIO
import os

def generate_qr_code(data:str,save_path:str):
    qr=qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=5
    )
    qr.add_data(data)
    qr.make(fit=True)

    img=qr.make_image(fill_color='black',back_color='white')
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    img.save(save_path)
