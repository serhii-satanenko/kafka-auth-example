import socketio

# Створення екземпляра клієнта Socket.IO
sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.event
def kafka_message(data):
    print("Message received:", data)

if __name__ == '__main__':
    # Підключення до Socket.IO сервера
    sio.connect('http://localhost:5001')
    try:
        # Тримати скрипт активним
        sio.wait()
    except KeyboardInterrupt:
        # Від'єднати клієнта при завершенні роботи
        sio.disconnect()