import Text.Read (readMaybe)

parseInt :: String -> Either String Int
parseInt s = case readMaybe s of
  Just n  -> Right n
  Nothing -> Left $ "Invalid integer: " ++ s
