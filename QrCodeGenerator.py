import qrcode

def generate_qrcode(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=5,
    )

    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qrimg.png")


generate_qrcode("https://checkmk-gmbh.jobs.personio.de/job/1936120?language=en&display=en&utm_source=juniors.ro#apply")