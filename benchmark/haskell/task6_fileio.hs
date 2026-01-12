import qualified Data.Map as M
import Data.Char (toLower)

main = do
  contents <- readFile "input.txt"
  let words' = words (map toLower contents)
      counts = M.toList $ foldr (\w m -> M.insertWith (+) w 1 m) M.empty words'
  writeFile "output.txt" $ unlines [w ++ ": " ++ show c | (w, c) <- counts]
