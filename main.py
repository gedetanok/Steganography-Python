from PIL import Image

def encode_image_bmp(input_image_path, output_image_path, secret_message):
    # Buka gambar
    image = Image.open(input_image_path)
    encoded_image = image.copy()
    
    width, height = image.size
    index = 0
    
    # Ubah pesan rahasia menjadi biner
    binary_secret_message = ''.join(format(ord(char), '08b') for char in secret_message)
    binary_secret_message += '111111111111111'  # penanda akhir pesan
    
    for row in range(height):
        for col in range(width):
            if index < len(binary_secret_message):
                r, g, b = image.getpixel((col, row))
                
                # Ubah bit terakhir dari setiap komponen warna dengan bit dari pesan
                if index < len(binary_secret_message):
                    new_r = int(format(r, '08b')[:-1] + binary_secret_message[index], 2)
                    index += 1
                else:
                    new_r = r
                
                if index < len(binary_secret_message):
                    new_g = int(format(g, '08b')[:-1] + binary_secret_message[index], 2)
                    index += 1
                else:
                    new_g = g
                
                if index < len(binary_secret_message):
                    new_b = int(format(b, '08b')[:-1] + binary_secret_message[index], 2)
                    index += 1
                else:
                    new_b = b
                
                encoded_image.putpixel((col, row), (new_r, new_g, new_b))
            else:
                break

    # Simpan gambar yang telah dienkripsi
    encoded_image.save(output_image_path, 'BMP')


def decode_image_bmp(image_path):
    # Buka gambar
    image = Image.open(image_path)
    
    width, height = image.size
    binary_message = ''
    
    for row in range(height):
        for col in range(width):
            r, g, b = image.getpixel((col, row))
            binary_message += format(r, '08b')[-1]
            binary_message += format(g, '08b')[-1]
            binary_message += format(b, '08b')[-1]
    
    # Pisahkan biner menjadi byte (8 bit)
    binary_message = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    
    # Konversi dari biner ke string
    decoded_message = ''
    for byte in binary_message:
        if byte == '11111111':  # penanda akhir pesan
            break
        decoded_message += chr(int(byte, 2))
    
    return decoded_message


# Contoh penggunaan:
image_path = 'Orang Ganteng.bmp'
output_image_path = 'output_image.bmp'
encode_image_bmp(image_path, output_image_path, 'sembilan maret')
print(decode_image_bmp(output_image_path))
