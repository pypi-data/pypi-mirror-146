import qrcode
import time


class QRcode:
    def __init__(self, data, qr_version, box_size, border, color_fill, back_color, file_name):
        self.data = data
        self.qr_version = qr_version
        self.box_size = box_size
        self.border = border
        self.color_fill = color_fill
        self.back_color = back_color
        self.file_name = file_name

    def generate_qr(self):
        qr = qrcode.QRCode(
            version=self.qr_version,
            box_size=self.box_size,
            border=self.border)
        qr.add_data(self.data)
        qr.make(fit=True)
        img = qr.make_image(fill=self.color_fill, back_color=self.back_color)
        img.save(self.file_name)


if __name__ == '__main__':
    data = str(input("QR code: "))
    ver = int(input("QR code vsersion: "))
    boxsize = int(input("QR code box size: "))
    border = int(input("QR code border: "))
    color_fill = str(input("Color fill: "))
    back_color = str(input("Back Color: "))
    file_name = str(input("file name: "))

    qrgen = QRcode(data, ver, boxsize, border,
                   color_fill, back_color, file_name)
    start_time = time.time()
    qrgen.generate_qr()
    print("Done in ", "--- %s seconds ---" % (time.time() - start_time))
