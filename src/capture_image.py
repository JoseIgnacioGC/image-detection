import cv2
from cv2.typing import MatLike
from PIL import Image


def __convert_opencv_to_pil(cv_image: MatLike) -> Image.Image:
    return Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))


def capture_image_from_camera() -> Image.Image | None:
    cap = cv2.VideoCapture(0)
    pil_image = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("no hay camara")
            break

        cv2.imshow("espacio pa capturar la foto", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord(" "):
            pil_image = __convert_opencv_to_pil(frame)
            break
        elif key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return pil_image
