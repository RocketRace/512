function entry(board, actions)
    
end

local tiles = {
    -- these first six entries are made to mirror the problem statement
    [0] = {name = "empty", type = "empty", glyph = "\u{3000}"}, -- 　
    [-3] = {name = "pico", type = "object", glyph = "\u{ffee}"}, -- ￮
    [6] = {name = "wall", type = "object", glyph = ""},
    [1] = {name = "pico", type = "noun", glyph = "\u{3330}"}, -- ㌰
    [3] = {name = "is", type = "verb", glyph = "\u{306f}"}, -- は
    [2] = {name = "you", type = "adjective", glyph = "\u{ff6d}\u{ff70}"}, -- ｭｰ
}

function make_level(board)
    local level = {width = #board[0]}
    for y, row in ipairs(board) do
        for x, n in ipairs(row) do
            level[y * level.width + x] = tiles[n]
        end
    end
    return level
end

function find_verbs(level)
    local positions = {}
    for i, z in ipairs(level) do
        if z.type == "verb" then
            table.insert(positions, i)
        end
    end
    return positions
end

function act(level, action)
    
end

print(tiles[1].glyph..tiles[3].glyph..tiles[2].glyph)