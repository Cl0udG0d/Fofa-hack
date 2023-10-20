import base64

encoded_data = "SGVsbG8gV29ybG"
try:
    decoded_data = base64.b64decode(encoded_data).decode('utf-8')
except Exception as e:
    print(e)
    decoded_data=""
    pass

print(decoded_data)