from django.middleware.common import CommonMiddleware



class MyMiddleware(CommonMiddleware):
    def process_request(self, request):
        print('This is my custom middleware.')
        print("\n\n\n\n")
        print("The request came is:")
        print(request)
        print(request.body)
        print(request.headers)

        return None