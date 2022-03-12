import tweepy

api_key = "AzvQgqGxCzzyUk78wg3q9TEcO"
api_secret = "rNHgvgXtA13lRRizXne3PAPIPgZWJjWDww5AOr7X5DCEklIzNw"
access_token = "848078166883053568-mqymPaAQASoAjGsZnNNO0sEixHCo0sN"
access_token_screet = "v88Qd5Gq5LKZuXut0QhMdFa2aRpxB9L3ZxDInrN3duLbB"

auth = tweepy.OAuthHandler(consumer_key = api_key, consumer_secret = api_secret)
auth.set_access_token(access_token, access_token_screet)

api = tweepy.API(auth)

api.update_status(status="tweepy test...")