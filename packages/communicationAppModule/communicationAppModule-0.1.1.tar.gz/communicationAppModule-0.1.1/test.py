from communicationApp import createClient
def main():

  telegram = createClient('telegram', bot_token ='1632387033:AAEgUxJiAwZBRVXwVpocXohQOxZYFhkkR6g')
  result = telegram.send_photo("https://im.uniqlo.com/style/SDP1779_30012719.jpg")
  print("---------end")
  print(result)

if __name__ == '__main__':
  try:
      main()
  except KeyboardInterrupt:
      exit()