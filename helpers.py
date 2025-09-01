import numpy as np
import cv2
import io

from PIL import Image, ImageEnhance, ImageFilter
from typing import Optional, Union, Tuple

def enhanceImage(image: Union[Image.Image, str], method: str = "opencv") -> Image.Image:
    """
    Enhanced version of your original function with multiple AI-powered options
    
    Args:
        image: PIL Image object or path to image file
        method: Enhancement method ('opencv', 'realesrgan', 'super-image', 'pil', 'combined')
    
    Returns:
        Enhanced PIL Image object
    """
    if method == "realesrgan":
        return enhanceWithRealESRGAN(image)
    elif method == "super-image":
        return enhanceWithSuperImage(image)
    elif method == "opencv":
        return enhanceWithOpenCV(image)
    elif method == "combined":
        return enhanceImageCombined(image)
    else:
        return enhanceWithPIL(image)

def enhanceWithSuperImage(image: Union[Image.Image, str]) -> Image.Image:
    """
    Enhance image using super-image library (HuggingFace based)
    Install: pip install super-image
    """
    try:
        from super_image import EdsrModel, ImageLoader
        
        # Load the image
        if isinstance(image, str):
            pil_image = Image.open(image)
        else:
            pil_image = image
        
        # Initialize model
        model = EdsrModel.from_pretrained('eugenesiow/edsr-base', scale=4)
        
        # Enhance the image
        inputs = ImageLoader.load_image(pil_image)
        preds = model(inputs)
        
        # Convert back to PIL
        enhanced = ImageLoader.get_image(preds, 0)
        return enhanced
        
    except ImportError:
        print("super-image not installed. Install with: pip install super-image")
        return enhanceWithOpenCV(image)
    except Exception as e:
        print(f"super-image enhancement failed: {e}")
        return enhanceWithOpenCV(image)
    
def enhanceImageCombined(image: Union[Image.Image, str]) -> Image.Image:
    """
    Combined enhancement using multiple techniques
    """
    # Start with AI enhancement if available
    try:
        enhanced = enhanceWithRealESRGAN(image)
    except:
        try:
            enhanced = enhanceWithSuperImage(image)
        except:
            enhanced = enhanceWithOpenCV(image)
    
    # Apply additional PIL enhancements
    final = enhanceWithPIL(enhanced)
    return final

def enhanceWithPIL(image: Union[Image.Image, str]) -> Image.Image:
    """
    Enhance image using PIL only (fallback method)
    """
    if isinstance(image, str):
        img = Image.open(image)
    else:
        img = image.copy()
    
    # Multiple enhancement steps
    enhanced = img
    
    # Apply filters
    enhanced = enhanced.filter(ImageFilter.DETAIL)
    enhanced = enhanced.filter(ImageFilter.SHARPEN)
    enhanced = enhanced.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    
    # Enhance attributes
    # Sharpness
    sharpness_enhancer = ImageEnhance.Sharpness(enhanced)
    enhanced = sharpness_enhancer.enhance(1.3)
    
    # Contrast
    contrast_enhancer = ImageEnhance.Contrast(enhanced)
    enhanced = contrast_enhancer.enhance(1.2)
    
    # Brightness
    brightness_enhancer = ImageEnhance.Brightness(enhanced)
    enhanced = brightness_enhancer.enhance(1.1)
    
    # Color saturation
    color_enhancer = ImageEnhance.Color(enhanced)
    enhanced = color_enhancer.enhance(1.15)
    
    return enhanced

def enhanceWithOpenCVTraditional(img: np.ndarray) -> np.ndarray:
    """
    Traditional OpenCV image enhancement techniques
    """
    # Denoising
    denoised = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    
    # Sharpening kernel
    kernel = np.array([[-1,-1,-1],
                      [-1, 9,-1],
                      [-1,-1,-1]])
    sharpened = cv2.filter2D(denoised, -1, kernel)
    
    # Contrast enhancement using CLAHE
    lab = cv2.cvtColor(sharpened, cv2.COLOR_BGR2LAB)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    lab[:,:,0] = clahe.apply(lab[:,:,0])
    enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    # Brightness adjustment
    enhanced = cv2.convertScaleAbs(enhanced, alpha=1.1, beta=10)
    
    return enhanced

def enhanceWithOpenCV(image: Union[Image.Image, str]) -> Image.Image:
    """
    Enhance image using OpenCV's built-in super-resolution models
    """
    try:
        # Convert to OpenCV format
        if isinstance(image, str):
            img = cv2.imread(image)
        else:
            img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Create OpenCV super resolution object
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        
        # Try to use EDSR model (you'll need to download this)
        model_path = "EDSR_x4.pb"  # Download from OpenCV's GitHub
        if os.path.exists(model_path):
            sr.readModel(model_path)
            sr.setModel("edsr", 4)
            enhanced = sr.upsample(img)
        else:
            # Fallback to traditional OpenCV enhancement
            enhanced = enhanceWithOpenCVTraditional(img)
        
        # Convert back to PIL
        enhanced_rgb = cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)
        return Image.fromarray(enhanced_rgb)
        
    except Exception as e:
        print(f"OpenCV enhancement failed: {e}")
        return enhanceWithPIL(image)

def enhanceWithRealESRGAN(image: Union[Image.Image, str]) -> Image.Image:
    """
    Enhance image using Real-ESRGAN (State-of-the-art AI upscaling)
    Install: pip install realesrgan
    """
    try:
        from realesrgan import RealESRGANer
        from realesrgan.archs.srvgg_arch import SRVGGNetCompact
        
        # Convert PIL to numpy if needed
        if isinstance(image, str):
            img = cv2.imread(image, cv2.IMREAD_COLOR)
        else:
            img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Initialize Real-ESRGAN
        model = RealESRGANer(
            scale=4,
            model_path='https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth',
            model=SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=32, upscale=4, act_type='prelu'),
            tile=0,
            tile_pad=10,
            pre_pad=0,
            half=False
        )
        
        # Enhance the image
        enhanced, _ = model.enhance(img, outscale=4)
        
        # Convert back to PIL
        enhanced_rgb = cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)
        return Image.fromarray(enhanced_rgb)
        
    except ImportError:
        print("Real-ESRGAN not installed. Install with: pip install realesrgan")
        return enhanceWithOpenCV(image)
    except Exception as e:
        print(f"Real-ESRGAN enhancement failed: {e}")
        return enhanceWithOpenCV(image)

def enhanceImageAdvanced(
    image: Union[Image.Image, str],
    upscale_factor: int = 2,
    denoise: bool = True,
    sharpen: bool = True,
    enhance_contrast: bool = True,
    enhance_brightness: bool = True,
    enhance_colors: bool = True
) -> Image.Image:
    """
    Advanced enhancement with granular control
    """
    if isinstance(image, str):
        img = Image.open(image)
    else:
        img = image.copy()
    
    # First try AI upscaling if factor > 1
    if upscale_factor > 1:
        try:
            img = enhanceWithRealESRGAN(img)
        except:
            # Fallback to PIL resize with high-quality resampling
            new_size = (img.width * upscale_factor, img.height * upscale_factor)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
    
    # Apply OpenCV denoising if requested
    if denoise:
        try:
            cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            denoised = cv2.fastNlMeansDenoisingColored(cv_img, None, 10, 10, 7, 21)
            img = Image.fromarray(cv2.cvtColor(denoised, cv2.COLOR_BGR2RGB))
        except:
            pass  # Skip if OpenCV not available
    
    # Apply PIL enhancements
    if sharpen:
        img = img.filter(ImageFilter.SHARPEN)
        img = img.filter(ImageFilter.DETAIL)
        sharpness_enhancer = ImageEnhance.Sharpness(img)
        img = sharpness_enhancer.enhance(1.2)
    
    if enhance_contrast:
        contrast_enhancer = ImageEnhance.Contrast(img)
        img = contrast_enhancer.enhance(1.15)
    
    if enhance_brightness:
        brightness_enhancer = ImageEnhance.Brightness(img)
        img = brightness_enhancer.enhance(1.05)
    
    if enhance_colors:
        color_enhancer = ImageEnhance.Color(img)
        img = color_enhancer.enhance(1.1)
    
    return img
