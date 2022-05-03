from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import time
import uncommitable

def __create_ocr_method():
    computer_vision_client = ComputerVisionClient(uncommitable.vision_endpoint, CognitiveServicesCredentials(uncommitable.vision_key))

    def run_ocr(image):
        read_response = computer_vision_client.read_in_stream(image, raw=True)
        read_operation_location = read_response.headers["Operation-Location"]
        operation_id = read_operation_location.split("/")[-1]
        while True:
            read_result = computer_vision_client.get_read_result(operation_id)
            if read_result.status.lower() not in ['notstarted', 'running']:
                break
            time.sleep(1)

        detected_text = []
        if read_result.status == OperationStatusCodes.succeeded:
            detected_text = [line.text 
                for page in read_result.analyze_result.read_results
                for line in page.lines]
        return ' '.join(detected_text).lower()

    return run_ocr


run_ocr = __create_ocr_method()