import json
import logging

class ApiBase:
     def __init__(self, session):
         self.response = None
         self.session = session


     def api_request(self, method, url, **kwargs):
         logging.info(f'Request method: {method}')
         logging.info(f'Request URL: {url}')       
         logging.info(f'Request Cookies: {self.session.cookies}')
         logging.info(f'Request headers: {self.session.headers}')

         json_body = kwargs.get("json", None)
         logging.info(f'Request Json body: {json.dumps(json_body, indent=4, ensure_ascii=False)}')

         form_data = kwargs.get("data", None)
         logging.info(f'Request Form Data: {json.dumps(form_data, indent=4, ensure_ascii=False)}')

         self.response = self.session.request(method, url, **kwargs)
         logging.info(f'Response headers: {self.response.headers}')
         logging.info(f'Response code: {self.response.status_code}')                      

         try:
             json_body = self.response.json()
             logging.info(f'Response: {json.dumps(json_body, indent=4, sort_keys=True, ensure_ascii=False)}')
         except Exception as e:
             logging.info(f"Exception: {e}")
             logging.info("Response: No Json Response Body")
