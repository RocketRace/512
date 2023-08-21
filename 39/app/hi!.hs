{-# LANGUAGE LambdaCase #-} {-# LANGUAGE OverloadedStrings #-} {--                                                    ##                        --}
import Text.Megaparsec (parse, errorBundlePretty, between, choice, many, sepBy, Parsec, eof) {--                      ##       ##               --}
{--                              --} ; import Control.Lens ((<&>), uncons, uses, (%=), (.=), _1) {--                 ##      ##     ###         --}
{--       ######                           --} ; import Text.Megaparsec.Char (char, newline, space1) {--             ##### ###         ###      --}
{--    ####    ##        #####                 --} ; import Text.Megaparsec.Char.Lexer (decimal, signed) {--        ##   ####           ## #### --}
{--  ###               ##    ###    ###                         --} ; import Control.Monad.State (execState) {--  ##       ##         ##        --}
{-- ##               ##       ##    ## ##    ##                            --} ; import Data.Maybe (listToMaybe) {--      ##         ##         --}
{--##               ##        ##   ##   ##   #######             #####          --} ; import Control.Monad.Fix (fix) {--       ###  ##          --}
{--##              ##        ##   ##    ##   ##     ####       ###    ###            --} ; import Data.Text (pack, Text) {--     #####          --}
{-- ##             ##       ##   ##     ##   ##              ##         ##   ##               --} ; import Data.Tuple (swap) {--     ####     ##--}
{--  ###     ##    ##     ##   ##      ##   #####          ##               ##                     --} ; import Data.Void (Void) {--         ## --}
{--     ####        #####     ##     ##    ##             ##      ###      ##         ##               --} ; import Data.Bool (bool) {--    #   --}
{--                            ######     ##              ##        ###   ##         ##    ###              --} ; data T = P | B | C | A {--    --}
{--                                     ######            ##        ##    ##        ##    ##  ####                    --} ; data F = F T [F] {----}
main = getContents >>= ((\case {--          ######         ###   ###     ##         ##   ##      ###                                            --}
{--} Left e -> putStrLn $ errorBundlePretty {--              ####        ##        ##   ##           ######                                     --}
{--   --} e; Right (f, i) -> (putStrLn . unwords {--                      ###    ##    ######      ###    ##    ####                            --}
{--        --} . (show <$>) . reverse . fst) (execState {--                 #####     ##    ##    ##       #  ##   ###                          --}
{--             --} (fix (\x -> foldl (\a f -> a >>= (\n -> ( {--                   ###           ##         ##      ##                         --}
{--                  --} n +) <$> (\(F t p) -> if null p then case {--             ######           ###     ##            ##                    --}
{--         ##            --} t of P -> return 1 ; B -> uses _1 length {--              ####  ##      ##     ##          ##   ##                --}
{--         ##        ##       --} C -> uses _1 uncons >>= maybe (return 0) {--                ##    ##        ###      ##   ###   ##           --}
{-- #####  ##       ##              --} (\(h, t) -> _1 .= t >> return h); A -> {--              #####    #       ##     ##  ####  ##     ###### --}
{--    #########   ##        ######      --} id %= swap >> return 0 else case t of{--                    ###    ##     ##  ##  ## ##   ##    ###--}
{--      ##    ########            ###        --} P -> x p >>= (\n -> _1 %= (n :) >> return {--           ######      ##   ##  ###   ##        #--}
{--     ##       ##                  ##            --} n); B -> negate <$> x p; C -> fix (\l f -> {--               ###   ##   ##   ##   ###    --}
{-- ### ##      ##                   ##     ######      --} uses _1 ((0 `elem`) . listToMaybe) >>= bool {--        ##    ##    ##   ##     ###  --}
{--   ######   ###          ###    ##     ##     ###         --} (x f >>= (\n -> (n +) <$> l f)) (return 0)) {--              ##    ##    ##    --}
{--   ##    ##########         ####      ##       ##    ####      --} p; A -> x p >> return 0) f)) (return 0)) f) {--                #####      --}
{--  ##       ##                  ##     ###      ##    ###   ####     --} (reverse i, []))) . parse ((,) <$> many (fix {--                     --}
{--  ##      ###       ##         ##        #######    ###    ###           --} (\t -> choice $ zipWith3 between (char <$> {--                  --}
{-- ##       ##        ####     ###   #          ##    ##     ##                 --} "([{<") (char <$> ")]}>") ((many t <&>) . {--              --}
{--         ##            ######      ###       ##    ##     ##                       --} F <$> [P, B, C, A]))) <* newline <*> signed {--       --}
{--                                     ########                                           --} (pure ()) decimal `sepBy` space1 <* eof :: {--   --}
{--                                                 ###    ##                                   --} Parsec Void Text ([F], [Int])) "") . pack {---}