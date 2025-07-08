




















































# class KahootAnswerFetcherApi: 
#     BASE_API_URL = "https://play.kahoot.it/rest/kahoots/"
#     CHALLENGE_API_URL = "https://kahoot.it/rest/challenges/pin/"
#     REQUEST_TIMEOUT = 10  # seconds
    
#     @staticmethod
#     def _create_request(url, headers=None):
#         default_headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
#             "Accept": "application/json"
#         }

#         return httpx.Request(
#             url=url,
#             method="GET",
#             headers=default_headers,
#         )


    
#     @staticmethod
#     async def get_quiz_by_id(quiz_id):
#         if not re.fullmatch(r"^[A-Za-z0-9-]*$", quiz_id):
#             return {'error': 'Invalid quiz ID format'}
        
#         url = f"{KahootAnswerFetcherApi.BASE_API_URL}{quiz_id}"


#         try:
#             request = KahootAnswerFetcherApi._create_request(url)
#             async with httpx.AsyncClient() as client:
#                 response = await client.send(request)

#             json_bytes = orjson.dumps(response.body, option=orjson.OPT_INDENT_2)
#             print(json_bytes.decode()) 

        
#         # return json.loads(response.read().decode('utf-8'))



#         except:
#             print("broky")


#         # except HTTPError as e:
#         #     if e.code == 404:
#         #         return {'error': 'Quiz not found. The ID may be incorrect.'}
#         #     return {'error': f'HTTP Error: {e.code} - {e.reason}'}
#         # except URLError as e:
#         #     return {'error': f'Connection error: {e.reason}. Check your internet connection.'}
#         # except InvalidURL:
#         #     return {'error': 'Invalid URL format for the Kahoot API.'}
#         # except json.JSONDecodeError:
#         #     return {'error': 'Failed to parse the response from Kahoot servers.'}
#         # except Exception as e:
#         #     return {'error': f'Unexpected error: {str(e)}'}
    
#     @staticmethod
#     async def get_quiz_id_from_pin(pin):
#         # if not pin.isdigit():
#         #     return {'error': 'PIN must contain only digits'}
            
#         url = f"{KahootAnswerFetcherApi.CHALLENGE_API_URL}{pin}"
        
       
#         request = KahootAnswerFetcherApi._create_request(url)
#         async with httpx.AsyncClient() as client:
#             response = await client.send(request)
#             data = orjson.loads(response.content)  # parse raw bytes to Python object

#         # Now you can pretty-print it if you want:
#         json_bytes = orjson.dumps(data, option=orjson.OPT_INDENT_2)
#         print(json_bytes.decode())

        
#         # return json.loads(response.read().decode('utf-8'))


