import cv2


class BaseImageLoader:
    @classmethod
    def read(cls, path: str) -> cv2.Mat:
        img = cv2.imread(path)
        return img


if __name__ == "__main__":
    import fire
    fire.Fire(BaseImageLoader)
