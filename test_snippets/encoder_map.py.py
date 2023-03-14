import encoder_reader
import time

E1 = encoder_reader.EncoderReader('C6', 'C7', 8, 1, 2)
E2 = encoder_reader.EncoderReader('B6', 'B7', 4, 1, 2)

while True:
    print(E2.read())
    time.sleep(0.5)