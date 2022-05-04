import requests


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
            # TODO: Handle error
            print('Oh no!')
            return 
        image_type = data['imageType']

        # TODO: Do sth with results
        print(image_type)

    def ask_provider(self, fileobj) -> dict | None:
        headers = {'Ocp-Apim-Subscription-Key': f'{self._sub_key}'}
        params = {'visualFeatures': 'ImageType'}
        files = {'file': (None, fileobj, 'multipart/form-data')}

        retrials = 3

        while retrials:
            try:
                response = requests.post(self.ENDPOINT, params=params,
                                        headers=headers, files=files)
                response.raise_for_status()
                return response.json()
            except (requests.exceptions.HTTPError,
                    requests.exceptions.RequestException) as _:
                retrials -= 1
            
        return None


if __name__ == '__main__':
    sd = StyleDetector()
    sd.detect_style('iroh lines.png')
    sd.detect_style('clipart.png')
    sd.detect_style('General_Iroh.jpg')

