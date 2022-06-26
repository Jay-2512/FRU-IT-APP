from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import cv2
import os

from img_proc import Proc



class MangoDetect:

    def detect_ripeness(image_path):
        # Disabling Tensorflow warning
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


        model = load_model('./Models/MANDET-v2.0.h5', compile=False)
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        file_path = image_path

        print("------------ filepath ------------")
        print(file_path)


        # For live detection of the fruit {NOT TESTED YET}

        # while True:
        #     cap = cv2.VideoCapture(0)
        #     ret, frame = cap.read()
        #     frame = cv2.resize(frame, (224, 224))
        #     cv2.imshow('frame', frame)
        #     image = Image.fromarray(frame)
        #     image = ImageOps.fit(image, (224, 224), Image.ANTIALIAS)
        #     image_array = np.asarray(image)
        #     normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        #     data[0] = normalized_image_array
        #     prediction = model.predict(data)
        #     print(prediction)

        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break

        #     pred_list = prediction.tolist()[0]

        #     grt_ind = pred_list.index(max(pred_list))

        #     os.system('cls')

        #     if grt_ind == 0:
        #         print("Prediction: Person")
        #     elif grt_ind == 1:
        #         print('Prediction: Phone')
        #     else:
        #         print('I Dont know wth is that')
        #     cap.release()
        #     cv2.destroyAllWindows()

        image = Image.open(file_path)
        # arg_image = cv2.imread(file_path)
        image = ImageOps.fit(image, (224, 224), Image.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
        prediction = model.predict(data)

        # clear screen
        # os.system('cls')

        # horizontal rule

        # print('❗ PREDICTING IMAGE ❗')
        # print(prediction)

        # print('Prediction List:')
        pred_list = prediction.tolist()[0]
        # os.system('cls')
        # print(pred_list)
        # print('Output index:')
        grt_ind = pred_list.index(max(pred_list))
        # print(grt_ind)

        # print('\n-------------------------\n')
        if grt_ind == 0:
            message = "💡Prediction: Overripe mango 🥭"
            output, opmsg = Proc.det_decay(file_path, unripe=False)
        elif grt_ind == 1:
            message = "💡Prediction: Ripe mango 🥭"
            output, opmsg = Proc.det_decay(file_path, unripe=False)
        elif grt_ind == 2:
            message = "💡Prediction: Unripe mango 🥭"
            output, opmsg = Proc.det_decay(file_path, unripe=True)
        else:
            message = '💡I Dont know wth is that'
            output = None, 'Hmmm...'
    
        return message, output, opmsg