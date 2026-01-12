import Network.HTTP.Simple

fetchUrl :: String -> IO (Either String String)
fetchUrl url = do
  response <- httpBS (parseRequest_ url)
  return $ Right $ show $ getResponseBody response
