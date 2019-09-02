from time import sleep

message_number = 0

while True:
  print("This is message number {}".format(message_number))
  message_number += 1
  sleep(1)