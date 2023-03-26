import QuinceQr as QR

from PIL import Image

qr = QR.QrCode("HELLO WORLD", QR.ErrorCorrectionLevel.M)

img = qr.make_image()
img.show()