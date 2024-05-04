import pandas as pd
import requests
from PIL import Image
import io
import numpy as np

df = pd.read_csv('./HackUPC2024/inditextech_hackupc_challenge_images.csv')

  # Quantitat de images que et vols descarregar

for i in range(1100): 
    #per cada peça de roba hi ha 3 imatges
    #nosaltres triarem una d'elles que tingui el fons blanc (si cap en té, no es tria la peça de roba)

    for j in range(1, 4):  # Recorre cada versió de la imatge
        url = df[f'IMAGE_VERSION_{j}'][i]
        try:
            response = requests.get(url)  # Realitza la solicitud HTTP

            # Verifica que es pugui arribar al URL
            if response.status_code == 200:
                with io.BytesIO(response.content) as stream:
                    image = Image.open(stream)
                    image_rgb = image.convert('RGB')

                    # convertir la imatge a un array per poder calcular el percentatge de blanc que hi ha
                    pixels = np.array(image_rgb)
                    white_threshold = 230 #mira els 3 canals RGB si són >= que 230
                    white_pixels = (pixels >= white_threshold).all(axis=-1) #comproba quins píxels son blancs
                    total_pixels = pixels.shape[0] * pixels.shape[1] #mida de la imatge

                    num_white_pixels = np.sum(white_pixels) #quantitat de píxels blancs
                    percentage_white = (num_white_pixels / total_pixels) * 100 #percentatge píxels blancs

                    height, width, _ = pixels.shape

                    # Verifica bordes superior e inferior
                    top_edge = pixels[0:1, :, :]
                    bottom_edge = pixels[-1:, :, :]

                    # Verifica bordes izquierdo y derecho
                    left_edge = pixels[:, 0:1, :]
                    right_edge = pixels[:, -1:, :]

                    # Une todos los bordes y verifica si son blancos
                    all_borders = np.concatenate((top_edge, bottom_edge, left_edge, right_edge), axis=None)

                    borders_white = np.all(all_borders >= 220)

                    if percentage_white >= 20 and borders_white == True:
                        #guardar la imatge
                        image.save(f'./image/{i}.png', format='png')
                        break
        except Exception as e:
            pass