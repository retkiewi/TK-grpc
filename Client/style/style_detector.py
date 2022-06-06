import requests
import enum


class Type(enum.Enum):
    line = 'line drawing'
    clipart = 'clip art'
    photo = 'photo'


class StyleDetector:
    ENDPOINT = 'https://westeurope.api.cognitive.microsoft.com/vision/v3.2/analyze'

    def __init__(self):
        self._sub_key = None

        with open('.skey', 'r') as f:
            self._sub_key = f.read().replace('\n', '')
        
        if self._sub_key is None:
            raise ValueError('Subscription key file was not read properly.')

    def detect_style(self, file_path: str):
        with open(file_path, 'rb') as fileobj:
            data = self.ask_provider(fileobj)

        if data is None:
            return Type.photo
        
        image_type = data['imageType']

        if image_type['lineDrawingType'] == 1:
            return Type.line
        elif image_type['clipArtType'] >= 2:
            return Type.clipart
        else:
            return Type.photo

    def ask_provider(self, fileobj):
        headers = {'Ocp-Apim-Subscription-Key': f'{self._sub_key}'}
        params = {'visualFeatures': 'ImageType'}
        files = {'file': (None, fileobj, 'multipart/form-data')}

        retrials = 3

        while retrials:
            try:
                response = requests.post(self.ENDPOINT, params=params,
                                        headers=headers, files=files, timeout=0.5)
                response.raise_for_status()
                return response.json()
            except (requests.exceptions.HTTPError,
                    requests.exceptions.RequestException) as _:
                retrials -= 1
            
        return None


if __name__ == '__main__':
    sd = StyleDetector()
    file_name = 'iroh lines.png'
    print(f'{file_name} is {sd.detect_style(file_name)}')
    file_name = 'clipart.png'
    print(f'{file_name} is {sd.detect_style(file_name)}')
    file_name = 'General_Iroh.jpg'
    print(f'{file_name} is {sd.detect_style(file_name)}')

