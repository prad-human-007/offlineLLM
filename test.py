import hashlib

message = '123'
digest = hashlib.sha256(message.encode()).hexdigest()

print(message + " : " + digest)


message = '456'
h = hashlib.sha256(message.encode())
digest = h.hexdigest()
print(message + " : " + digest)


message = '789'
h = hashlib.sha256(message.encode())
digest = h.hexdigest()
print(message + " : " + digest)

