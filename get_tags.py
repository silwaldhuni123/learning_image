from transformers import pipeline
from PIL import Image
import io
pipe=pipeline("image-classification")

def get_tags(image_in_byte):
    image = Image.open(io.BytesIO(image_in_byte))
    return pipe(image)

if __name__=='__main__':
    import requests
    url = 'http://images.cocodataset.org/val2017/000000039769.jpg'
    response=requests.get(url, stream=True)
    print(get_tags(response.content))

