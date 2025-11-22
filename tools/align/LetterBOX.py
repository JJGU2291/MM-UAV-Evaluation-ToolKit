import cv2
import numpy as np


class LetterBox:
    """
    Resize image and padding for detection, instance segmentation, pose.

    This class resizes and pads images to a specified shape while preserving aspect ratio. It also updates corresponding labels and bounding boxes.

    Attributes:
        new_shape (tuple): Target shape (height, width) for resizing.
        auto (bool): Whether to use minimum rectangle.
        scale_fill (bool): Whether to stretch the image to new_shape.
        scaleup (bool): Whether to allow scaling up. If False, only scale down.
        stride (int): Stride for rounding padding.
        center (bool): Whether to center the image or align to top-left.

    Methods:
        __call__: Resize and pad image, update labels and bounding boxes.

    Examples:
        >>> transform = LetterBox(new_shape=(640, 640))
        >>> result = transform(labels)
        >>> resized_img = result["img"]
        >>> updated_instances = result["instances"]
    """

    def __init__(self, new_shape=(640, 640), auto=False, scale_fill=False, scaleup=True, center=True, stride=32):
        """
        Initialize LetterBox object for resizing and padding images.

        This class is designed to resize and pad images for object detection, instance segmentation, and pose estimation tasks. It supports various resizing modes including auto-sizing, scale-fill, and letterboxing.

        Args:
            new_shape (Tuple[int, int]): Target size (height, width) for the resized image.
            auto (bool): If True, use minimum rectangle to resize. If False, use new_shape directly.
            scale_fill (bool): If True, stretch the image to new_shape without padding.
            scaleup (bool): If True, allow scaling up. If False, only scale down.
            center (bool): If True, center the placed image. If False, place image in top-left corner.
            stride (int): Stride of the model (e.g., 32 for YOLOv5).

        Attributes:
            new_shape (Tuple[int, int]): Target size for the resized image.
            auto (bool): Flag for using minimum rectangle resizing.
            scale_fill (bool): Flag for stretching image without padding.
            scaleup (bool): Flag for allowing upscaling.
            stride (int): Stride value for ensuring image size is divisible by stride.

        Examples:
            >>> letterbox = LetterBox(new_shape=(640, 640), auto=False, scale_fill=False, scaleup=True, stride=32)
            >>> resized_img = letterbox(original_img)
        """
        self.new_shape = new_shape
        self.auto = auto
        self.scale_fill = scale_fill
        self.scaleup = scaleup
        self.stride = stride
        self.center = center  # Put the image in the middle or top-left

    def __call__(self, labels=None, image=None, image2=None):
        """
        Resizes and pads an image for object detection, instance segmentation, or pose estimation tasks.

        This method applies letterboxing to the input image, which involves resizing the image while maintaining its aspect ratio and adding padding to fit the new shape. It also updates any associated labels accordingly.

        Args:
            labels (Dict | None): A dictionary containing image data and associated labels, or empty dict if None.
            image (np.ndarray | None): The input image as a numpy array. If None, the image is taken from 'labels'.

        Returns:
            (Dict | Tuple): If 'labels' is provided, returns an updated dictionary with the resized and padded image, updated labels, and additional metadata. If 'labels' is empty, returns a tuple containing the resized and padded image, and a tuple of (ratio, (left_pad, top_pad)).

        Examples:
            >>> letterbox = LetterBox(new_shape=(640, 640))
            >>> result = letterbox(labels={"img": np.zeros((480, 640, 3)), "instances": Instances(...)} )
            >>> resized_img = result["img"]
            >>> updated_instances = result["instances"]
        """
        if labels is None:
            labels = {}

        # 获取图像
        img = labels.get('img') if image is None else image
        img2 = labels.get('img2') if image2 is None else image2

        # 获取目标尺寸
        new_shape = self.new_shape
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        # 核心修改点：分别处理两图的函数
        def process_image(image, new_shape):
            shape = image.shape[:2]  # 当前图像的 [height, width]

            # 计算缩放比例
            r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
            if not self.scaleup:  # 只缩小不放大
                r = min(r, 1.0)
            # print("r: ",r)
            # print("image: ", image.shape)
            # 计算填充
            ratio = (r, r)
            new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
            dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]

            if self.auto:  # 自动计算最小矩形填充
                # print("auto")
                dw, dh = np.mod(dw, self.stride), np.mod(dh, self.stride)
            elif self.scale_fill:  # 拉伸模式
                dw, dh = 0.0, 0.0
                new_unpad = (new_shape[1], new_shape[0])
                ratio = (new_shape[1] / shape[1], new_shape[0] / shape[0])

            dw, dh = dw / 2, dh / 2  # 两侧均分填充

            # 调整图像尺寸
            if shape[::-1] != new_unpad:
                image = cv2.resize(image, new_unpad, interpolation=cv2.INTER_LINEAR)
            # print("image: ", image.shape)
            # 添加边框
            top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
            left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
            image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))
            # print("image: ", image.shape)
            # 返回处理后的图像和参数
            return image, ratio, (dw, dh)

        img, ratio1, pad1 = process_image(img, new_shape)
        img2, ratio2, pad2 = process_image(img2, new_shape)

        # 更新标签信息
        if len(labels):
            labels = self._update_labels(labels, ratio1, *pad1, ratio2, *pad2)

            labels['img'] = img
            labels['img2'] = img2
            labels['resized_shape'] = new_shape
            labels['resized_shape2'] = new_shape
            return labels
        else:
            # print(img.shape)
            # print(img2.shape)
            return img, img2

    def _update_labels(self, labels, ratio1, dw1, dh1, ratio2, dw2, dh2):
        # 在实际使用时，这里会包含对标签（如边界框）的更新逻辑
        # 例如：更新边界框的位置、尺寸等
        # 这里为了简单，只是返回原始标签
        return labels


# 使用示例
if __name__ == "__main__":
    # 创建 LetterBox 对象
    letterbox = LetterBox(new_shape=(640, 640))

    # 读取两张图片
    image1 = cv2.imread('rgb.png')  # 替换为你的第一张图片路径
    image2 = cv2.imread('ir.png')  # 替换为你的第二张图片路径

    # 检查图片是否成功加载
    if image1 is None or image2 is None:
        print("Error: Unable to load one or both images.")
    else:
        # 调用 LetterBox 的 __call__ 方法处理图片
        transformed_img1, transformed_img2 = letterbox(image=image1, image2=image2)

        # 保存处理后的图片
        cv2.imwrite('transformed_image1.jpg', transformed_img1)
        cv2.imwrite('transformed_image2.jpg', transformed_img2)

        print("Images processed and saved successfully.")