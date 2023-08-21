// Minesweeper 2.0
var readline = require("readline")
var crypto = require("crypto")
var readline = require("readline")
readline.emitKeypressEvents(process.stdin);
var stdin = process.stdin
var stdout = process.stdout
stdin.setRawMode(true);
var width = 35
var height = 15
var minesCount = 75
var started = false
var lost = false
var won = false
var cheated = false
var zoom = false
var currentSpeed = 1
var zoomSpeed = 5
var normalSpeed = 1
var bonuses = 0
var pos = {x:0, y:0}
var mines = Array()
var flags = Array()
var unknowns = Array()
var revealed = Array()
var firstMove = false
var start = null
var moves = 0
var actions = 0
for (var i = 0; i < height; i++) {
  var line = Array()
  for (let j = 0; j < width; j++) {
    line.push(false)
  }
  flags.push(line)
}
for (var i = 0; i < height; i++) {
  var line = Array()
  for (let j = 0; j < width; j++) {
    line.push(false)
  }
  unknowns.push(line)
}
for (var i = 0; i < height; i++) {
  var line = Array()
  for (let j = 0; j < width; j++) {
    line.push(false)
  }
  revealed.push(line)
}
function totalCount() {
  return width * height
}
function mineCount() {
  var count = 0;
  for (var i = 0; i < height; i++) {
    for (let j = 0; j < width; j++) {
      if (mines[i][j]) {
        count += 1
      }
    }
  }
  return count
}
function flagCount() {
  var count = 0;
  for (var i = 0; i < height; i++) {
    for (let j = 0; j < width; j++) {
      if (flags[i][j]) {
        count += 1
      }
    }
  }
  return count
}
function revealedCount() {
  var count = 0;
  for (var i = 0; i < height; i++) {
    for (let j = 0; j < width; j++) {
      if (revealed[i][j]) {
        count += 1
      }
    }
  }
  return count
}
function blankCount() {
  return totalCount() - flagCount() - revealedCount()
}
function show() {
  var string = ""
  string += mineCount().toString() + " mines " + flagCount().toString() + " flags (" + (mineCount() - flagCount()).toString() + " unflagged) " + revealedCount().toString() + " revealed " + blankCount().toString() + " blank \n"
  string += moves + " moves " + time(Date.now() - start) + " " + stat().toString() + " m/s " + stat2().toString() + " a/s\n"
  for (var i = 0; i < height; i++) {
    for (let j = 0; j < width; j++) {
      var value = "."
      if (revealed[i][j]) {
        var nearby = minesNearby({x:j, y:i}).toString()
        if (nearby == "0") {
          value = " "
        } else {
          value = nearby
        }
      } else if (flags[i][j]) {
        value = "F"
      } else if (unknowns[i][j]) {
        value = "?"
      }
      string += color(value);
      if (pos.x == j && pos.y == i) {
        string += "[" + value + "]\x1b[0m"
      } else {
        string += " " + value + " \x1b[0m"
      }
    }
    string += "\n"
  }
  stdout.write(string)
}
function showEmpty() {
  var string = ""
  string += minesCount.toString() + " mines " + flagCount().toString() + " flags (" + minesCount.toString() + " unflagged) 0 revealed " + blankCount().toString() + " blank \n"
  if (firstMove) {
    string += moves + " moves " + time(Date.now() - start) + " " + stat().toString() + " m/s " + stat2().toString() + " a/s\n"
  }
  for (var i = 0; i < height; i++) {
    for (let j = 0; j < width; j++) {
      var value = "."
      if (flags[i][j]) {
        value = "F"
      } else if (unknowns[i][j]) {
        value = "?"
      }
      string += color(value);
      if (pos.x == j && pos.y == i) {
        string += "[" + value + "]\x1b[0m"
      } else {
        string += " " + value + " \x1b[0m"
      }
    }
    string += "\n"
  }
  stdout.write(string)
}
function showLose() {
  if (cheated) {
    stdout.write("You lost (and you cheated)\n")
  } else {
    stdout.write("You lost\n")
  }
  var string = ""
  string += moves + " moves " + time(Date.now() - start) + " " + stat().toString() + " m/s " + stat2().toString() + " a/s\n"
  for (var i = 0; i < height; i++) {
    for (let j = 0; j < width; j++) {
      var value = "."
      if (revealed[i][j]) {
        var nearby = minesNearby({x:j, y:i}).toString()
        if (nearby == "0") {
          value = " "
        } else {
          value = nearby
        }
      } else if (flags[i][j] && !mines[i][j]) {
        value = "X"
      } else if (flags[i][j]) {
        value = "F"
      } else if (mines[i][j]) {
        value = "*"
      }
      string += color(value);
      if (pos.x == j && pos.y == i) {
        string += "[" + value + "]\x1b[0m"
      } else {
        string += " " + value + " \x1b[0m"
      }
    }
    string += "\n"
  }
  stdout.write(string)
}
function showWin() {
  if (cheated) {
    stdout.write("You win (but you cheated)\n")
  } else if (bonuses > 0) {
    stdout.write("You win with " + bonuses.toString() + " extra challenges\n")
  } else {
    stdout.write("You win\n")
  }
  var string = ""
  string += moves + " moves " + time(Date.now() - start) + " " + stat().toString() + " m/s " + stat2().toString() + " a/s\n"
  for (var i = 0; i < height; i++) {
    for (let j = 0; j < width; j++) {
      var value = "."
      if (revealed[i][j]) {
        var nearby = minesNearby({x:j, y:i}).toString()
        if (nearby == "0") {
          value = " "
        } else {
          value = nearby
        }
      } else if (mines[i][j]) {
        value = "*"
      }
      string += color(value) + " " + value + " \x1b[0m"
    }
    string += "\n"
  }
  stdout.write(string)
}
function minesNearby(position) {
  var sum = 0
  if (position.x > 0) {
    if (mines[position.y][position.x - 1]) {
      sum += 1;
    }
    if (position.y > 0) {
      if (mines[position.y - 1][position.x - 1]) {
        sum += 1;
      }   
    }
    if (position.y < height - 1) {
      if (mines[position.y + 1][position.x - 1]) {
        sum += 1;
      }   
    }
  }
  if (position.x < width - 1) {
    if (mines[position.y][position.x + 1]) {
      sum += 1;
    }
    if (position.y > 0) {
      if (mines[position.y - 1][position.x + 1]) {
        sum += 1;
      }   
    }
    if (position.y < height - 1) {
      if (mines[position.y + 1][position.x + 1]) {
        sum += 1;
      }   
    }
  }
  if (position.y > 0) {
    if (mines[position.y - 1][position.x]) {
      sum += 1;
    }   
  }
  if (position.y < height - 1) {
    if (mines[position.y + 1][position.x]) {
      sum += 1;
    }   
  }
  return sum
}
function flagsNearby() {
  var sum = 0
  if (pos.x > 0) {
    if (flags[pos.y][pos.x - 1]) {
      sum += 1;
    }
    if (pos.y > 0) {
      if (flags[pos.y - 1][pos.x - 1]) {
        sum += 1;
      }   
    }
    if (pos.y < height - 1) {
      if (flags[pos.y + 1][pos.x - 1]) {
        sum += 1;
      }   
    }
  }
  if (pos.x < width - 1) {
    if (flags[pos.y][pos.x + 1]) {
      sum += 1;
    }
    if (pos.y > 0) {
      if (flags[pos.y - 1][pos.x + 1]) {
        sum += 1;
      }   
    }
    if (pos.y < height - 1) {
      if (flags[pos.y + 1][pos.x + 1]) {
        sum += 1;
      }   
    }
  }
  if (pos.y > 0) {
    if (flags[pos.y - 1][pos.x]) {
      sum += 1;
    }   
  }
  if (pos.y < height - 1) {
    if (flags[pos.y + 1][pos.x]) {
      sum += 1;
    }   
  }
  return sum
}
function blanksNearby() {
  var sum = 0
  if (pos.x > 0) {
    if (!flags[pos.y][pos.x - 1] && !revealed[pos.y][pos.x - 1]) {
      sum += 1;
    }
    if (pos.y > 0) {
      if (!flags[pos.y - 1][pos.x - 1] && !revealed[pos.y - 1][pos.x - 1]) {
        sum += 1;
      }   
    }
    if (pos.y < height - 1) {
      if (!flags[pos.y + 1][pos.x - 1] && !revealed[pos.y + 1][pos.x - 1]) {
        sum += 1;
      }   
    }
  }
  if (pos.x < width - 1) {
    if (!flags[pos.y][pos.x + 1] && !revealed[pos.y][pos.x + 1]) {
      sum += 1;
    }
    if (pos.y > 0) {
      if (!flags[pos.y - 1][pos.x + 1] && !revealed[pos.y - 1][pos.x + 1]) {
        sum += 1;
      }   
    }
    if (pos.y < height - 1) {
      if (!flags[pos.y + 1][pos.x + 1] && !revealed[pos.y + 1][pos.x + 1]) {
        sum += 1;
      }   
    }
  }
  if (pos.y > 0) {
    if (!flags[pos.y - 1][pos.x] && !revealed[pos.y - 1][pos.x]) {
      sum += 1;
    }   
  }
  if (pos.y < height - 1) {
    if (!flags[pos.y + 1][pos.x] && !revealed[pos.y + 1][pos.x]) {
      sum += 1;
    }   
  }
  return sum
}
function color(string) {
  switch (string) {
    case " ":
      return "\x1b[48;5;238m";
    case "1":
      return "\x1b[48;5;240;38;5;45m";
    case "2":
      return "\x1b[48;5;240;38;5;46m";
    case "3":
      return "\x1b[48;5;240;38;5;208m";
    case "4":
      return "\x1b[48;5;240;38;5;33m";
    case "5":
      return "\x1b[48;5;240;38;5;160m";
    case "6":
      return "\x1b[48;5;240;38;5;43m";
    case "7":
      return "\x1b[48;5;240;38;5;15m";
    case "8":
      return "\x1b[48;5;240;38;5;242m";
    case "F":
      return "\x1b[48;5;236;38;5;220m";
    case "?":
      return "\x1b[48;5;236;38;5;183m";
    case ".":
      return "\x1b[48;5;236m";
    case "X":
      return "\x1b[48;5;88m";
    case "*":
      if (lost) {
        return "\x1b[48;5;88m";
      } else {
        return "\x1b[48;5;236;38;5;196m";
      }
    default:
      break;
  }
}
function pass() {}
function makeGrid() {
  var notReady = true
  while (notReady) {
    for (var i = 0; i < height; i++) {
      var line = Array()
      var bytes = crypto.randomBytes(width)
      for (let j = 0; j < width; j++) {
        var byte = bytes[j];
        if (byte > 256 * minesCount / totalCount()) {
          line.push(false);
        } else {
          if (-1 <= (pos.x - j) && (pos.x - j) <= 1 && -1 <= (pos.y - i) && (pos.y - i) <= 1) {
            line.push(false);
          } else {
            line.push(true);
          }
        }
      }
      mines.push(line)
    }
    if (mineCount() == minesCount) {
      notReady = false;
    } else {
      mines = Array()
    }
  }
}
function reveal() {
  revealArg(pos);
}
function revealArg(position) {
  if (revealed[position.y][position.x]) {
    pass()
  } else if (flags[position.y][position.x]) {
    pass()
  } else {
    if (mines[position.y][position.x]) {
      lost = true
    } else {
      revealed[position.y][position.x] = true;
      if (revealedCount() + minesCount == totalCount()) {
        won = true;
        return;
      }
      if (minesNearby(position) == 0) {
        if (position.x > 0) {
          revealArg({x:position.x - 1, y:position.y})
          if (position.y > 0) {
            revealArg({x:position.x - 1, y:position.y - 1})
          }
          if (position.y < height - 1) {
            revealArg({x:position.x - 1, y:position.y + 1})
          }
        }
        if (position.x < width - 1) {
          revealArg({x:position.x + 1, y:position.y})
          if (position.y > 0) {
            revealArg({x:position.x + 1, y:position.y - 1})
          }
          if (position.y < height - 1) {
            revealArg({x:position.x + 1, y:position.y + 1})
          }
        }
        if (position.y > 0) {
          revealArg({x:position.x, y:position.y - 1})
        }
        if (position.y < height - 1) {
          revealArg({x:position.x, y:position.y + 1})
        }
      }
    }
  }
}
function flag() {
  if (!revealed[pos.y][pos.x]) {
    var currentFlag = flags[pos.y][pos.x]
    if (currentFlag) {
      flagUnset(pos)
    } else {
      flagSet(pos)
    }
  }
}
function flagSet(position) {
  if (!revealed[position.y][position.x]) {
    flags[position.y][position.x] = true
    unknowns[position.y][position.x] = false
  }
}
function flagUnset(position) {
  if (!revealed[position.y][position.x]) {
    flags[position.y][position.x] = false
  }
}
function cord() {
  if (revealed[pos.y][pos.x]) {
    if (minesNearby(pos) == flagsNearby()) {
      if (pos.x > 0) {
        revealArg({x:pos.x - 1, y:pos.y})
        if (pos.y > 0) {
          revealArg({x:pos.x - 1, y:pos.y - 1})
        }
        if (pos.y < height - 1) {
          revealArg({x:pos.x - 1, y:pos.y + 1})
        }
      }
      if (pos.x < width - 1) {
        revealArg({x:pos.x + 1, y:pos.y})
        if (pos.y > 0) {
          revealArg({x:pos.x + 1, y:pos.y - 1})
        }
        if (pos.y < height - 1) {
          revealArg({x:pos.x + 1, y:pos.y + 1})
        }
      }
      if (pos.y > 0) {
        revealArg({x:pos.x, y:pos.y - 1})
      }
      if (pos.y < height - 1) {
        revealArg({x:pos.x, y:pos.y + 1})
      }
    }
  } else {
    flag()
  }
}
function extra() {
  if (revealed[pos.y][pos.x]) {
    if (flagCount() != 0 && blanksNearby() == 0) {
      if (pos.x > 0) {
        flagUnset({x:pos.x - 1, y:pos.y})
        if (pos.y > 0) {
          flagUnset({x:pos.x - 1, y:pos.y - 1})
        }
        if (pos.y < height - 1) {
          flagUnset({x:pos.x - 1, y:pos.y + 1})
        }
      }
      if (pos.x < width - 1) {
        flagUnset({x:pos.x + 1, y:pos.y})
        if (pos.y > 0) {
          flagUnset({x:pos.x + 1, y:pos.y - 1})
        }
        if (pos.y < height - 1) {
          flagUnset({x:pos.x + 1, y:pos.y + 1})
        }
      }
      if (pos.y > 0) {
        flagUnset({x:pos.x, y:pos.y - 1})
      }
      if (pos.y < height - 1) {
        flagUnset({x:pos.x, y:pos.y + 1})
      }
    } else if (blanksNearby() + flagsNearby() == minesNearby(pos)) {
      if (pos.x > 0) {
        flagSet({x:pos.x - 1, y:pos.y})
        if (pos.y > 0) {
          flagSet({x:pos.x - 1, y:pos.y - 1})
        }
        if (pos.y < height - 1) {
          flagSet({x:pos.x - 1, y:pos.y + 1})
        }
      }
      if (pos.x < width - 1) {
        flagSet({x:pos.x + 1, y:pos.y})
        if (pos.y > 0) {
          flagSet({x:pos.x + 1, y:pos.y - 1})
        }
        if (pos.y < height - 1) {
          flagSet({x:pos.x + 1, y:pos.y + 1})
        }
      }
      if (pos.y > 0) {
        flagSet({x:pos.x, y:pos.y - 1})
      }
      if (pos.y < height - 1) {
        flagSet({x:pos.x, y:pos.y + 1})
      }
    }
  } else {
    flag()
  }
}
function unknown() {
  if (!revealed[pos.y][pos.x] && !flags[pos.y][pos.x]) {
    var currentUnknown = unknowns[pos.y][pos.x]
    if (currentUnknown) {
      unknowns[pos.y][pos.x] = false
    } else {
      unknowns[pos.y][pos.x] = true
    }
  }
}
function blank() {
  if (flags[pos.y][pos.x]) {
    flags[pos.y][pos.x] = false
  }
  if (unknowns[pos.y][pos.x]) {
    unknowns[pos.y][pos.x] = false
  }
}
function please() {
  if (!revealed[pos.y][pos.x] && !flags[pos.y][pos.x]) {
    if (unknowns[pos.y][pos.x]) {
      if (!started) {
        makeGrid()
        started = true
      }
      cheated = true
      if (mines[pos.y][pos.x]) {
        flag()
      } else {
        reveal()
      }
    } else {
      unknown()
    }
  }
}
function moreMines() {
  var mineRate = minesCount / totalCount()
  if (started) {
    for (var i = 0; i < height; i++) {
      for (let j = 0; j < width; j++) {
        if (!mines[i][j] & !flags[i][j] & !revealed[i][j]) {
          if (crypto.randomInt(100) < 33.333 * mineRate) {
            mines[i][j] = true;
          }
        }
      }
    }
    if (revealedCount() + mineCount() == totalCount()) {
      won = true;
      cheated = true;
    }
  } else {
    minesCount += crypto.randomInt(Math.floor(mineRate * (totalCount() - minesCount) / 3))
    if (revealedCount() + minesCount == totalCount()) {
      won = true;
      cheated = true;
    }
  }
}
function time(seconds) {
  var seconds = seconds / 1000
  var hours = Math.floor(seconds / 60 / 60)
  var minutes = Math.floor((seconds - hours * 60 * 60) / 60)
  var seconds = seconds - hours * 60 * 60 - minutes * 60
  var string = seconds.toString() + "s"
  if (minutes != 0 || hours != 0) {
    string = minutes.toString() + "m " + string
  }
  if (hours != 0) {
    hours.toString() + "h " + string
  }
  return string
}
function stat() {
  var now = Date.now()
  var seconds = (now - start) / 1000
  var rate = moves / seconds
  if (rate > 100 || isNaN(rate)) {
    return "X"
  } else {
    return Math.round(rate * 10) / 10
  }
}
function stat2() {
  var now = Date.now()
  var seconds = (now - start) / 1000
  var rate = actions / seconds
  if (rate > 100 || isNaN(rate)) {
    return "X"
  } else {
    return Math.round(rate * 10) / 10
  }
}
function quit() {
  process.exit()
}
function controls() {
  stdout.write("Minesweeper 2.0\n")
  stdout.write("Controls:\n")
  stdout.write("WASD: Move\n")
  stdout.write("R: Reveal\n")
  stdout.write("F: Flag\n")
  stdout.write("C: Cord\n")
  stdout.write("E: Extra\n")
  stdout.write("U: Unknown\n")
  stdout.write("B: Blank\n")
  stdout.write("P: Please (cheats)\n")
  stdout.write("IJKL: Move to blank\n")
  stdout.write("N: Move to nearest blank\n")
  stdout.write("N: Move to middle\n")
  stdout.write("Z: Zoom mode (toggle)\n")
  stdout.write("X: Xtra challenge\n")
  stdout.write("H: Help\n")
  stdout.write("Q: Quit\n")
  stdout.write("\n")
}
stdin.on("keypress", (data, key) => {
  input = key.name
  if (input.length == 1) {
    switch (input.toLowerCase()) {
      case "w":
        moves += 1
        if (start == null) {
          start = Date.now()
          firstMove = true
        }
        pos.y-=currentSpeed
        if (pos.y <= -1) {
          pos.y = pos.y + height
        }
        break;
      case "a":
        moves += 1
        if (start == null) {
          start = Date.now()
          firstMove = true
        }
        pos.x-=currentSpeed
        if (pos.x <= -1) {
          pos.x = pos.x + width
        }
        break;
      case "s":
        moves += 1
        if (start == null) {
          start = Date.now()
          firstMove = true
        }
        pos.y+=currentSpeed
        if (pos.y >= height) {
          pos.y = pos.y - height
        }
        break;
      case "d":
        moves += 1
        if (start == null) {
          start = Date.now()
          firstMove = true
        }
        pos.x+=currentSpeed
        if (pos.x >= width) {
          pos.x = pos.x - width
        }
        break;
      case "r":
        moves += 1
        actions += 1
        if (start == null) {
          start = Date.now()
          firstMove = true
        }
        if (started) {
          reveal()
        } else {
          makeGrid()
          started = true
          reveal()
        }
        break;
      case "f":
        moves += 1
        actions += 1
        if (start == null) {
          start = Date.now()
          firstMove = true
        }
        flag()
        break;
      case "c":
        moves += 1
        actions += 1
        if (start == null) {
          start = Date.now()
          firstMove = true
        }
        cord()
        break;
      case "e":
        moves += 1
        actions += 1
        if (start == null) {
          start = Date.now()
          firstMove = true
        }
        extra()
        break;
      case "u":
        moves += 1
        actions += 1
        if (start == null) {
          start = Date.now()
          firstMove = true
        }
        unknown()
        break;
      case "b":
        moves += 1
        actions += 1
        if (start == null) {
          start = Date.now()
          firstMove = true
        }
        blank()
        break;
      case "p":
        moves += 1
        actions += 1
        if (start == null) {
          start = Date.now()
          firstMove = true
        }
        please()
        break;
      case "i":
        moves += 1
        if (start == null) {
          start = Date.now()
          firstMove = true
        }
        var y = pos.y - 1;
        if (y == -1) {
          pos.y = height - 1;
          break;
        }
        while (y != pos.y) {
          if (y == -1) {
            pos.y = 0;
            break;
          }
          if (!revealed[y][pos.x] && !flags[y][pos.x]) {
            pos.y = y;
            break;
          }
          y -= 1;
        }
        break;
      case "j":
        moves += 1
        if (start == null) {
          start = Date.now()
          firstMove = true
        }
        var x = pos.x - 1;
        if (x == -1) {
          pos.x = width - 1;
          break;
        }
        while (x != pos.x) {
          if (x == -1) {
            pos.x = 0;
            break;
          }
          if (!revealed[pos.y][x] && !flags[pos.y][x]) {
            pos.x = x;
            break;
          }
          x -= 1;
        }
        break;
      case "k":
        moves += 1
        if (start == null) {
          start = Date.now()
          firstMove = true
        }
        var y = pos.y + 1;
        if (y == height) {
          pos.y = 0;
          break;
        }
        while (y != pos.y) {
          if (y == height) {
            pos.y = height - 1;
            break;
          }
          if (!revealed[y][pos.x] && !flags[y][pos.x]) {
            pos.y = y;
            break;
          }
          y += 1;
        }
        break;
      case "l":
        moves += 1
        if (start == null) {
          start = Date.now()
          firstMove = true
        }
        var x = pos.x + 1;
        if (x == width) {
          pos.x = 0;
          break;
        }
        while (x != pos.x) {
          if (x == width) {
            pos.x = width - 1;
            break;
          }
          if (!revealed[pos.y][x] && !flags[pos.y][x]) {
            pos.x = x;
            break;
          }
          x += 1;
        }
        break;
      case "m":
        moves += 1
        if (start == null) {
          start = Date.now()
          firstMove = true
        }
        pos.x = Math.floor(width / 2)
        pos.y = Math.floor(height / 2)
        break;
      case "n":
        moves += 1
        if (start == null) {
          start = Date.now()
          firstMove = true
        }
        if (blankCount() == 1) {
          for (var i = 0; i < height; i++) {
            for (let j = 0; j < width; j++) {
              if (!revealed[j][i] && !flags[j][i]) {
                pos.x = j;
                pos.y = i;
              }
            }
          }
        } else {
          var distance = 1;
          var done = false
          while (!done) {
            for (var i = 0; i < height; i++) {
              if (!done) {
                for (let j = 0; j < width; j++) {
                  if (!revealed[i][j] && !flags[i][j]) {
                    if (1 <= Math.abs(i - pos.y) + Math.abs(j - pos.x) && Math.abs(i - pos.y) + Math.abs(j - pos.x) <= distance) {
                      pos.x = j;
                      pos.y = i;
                      done = true;
                      break;
                    }
                  }
                }
              }
            }
            distance += 1
          }
        }
        break;
      case "x":
        moves += 1
        if (start == null) {
          start = Date.now()
          firstMove = true
        }
        moreMines();
        bonuses += 1;
        break;
      case "z":
        moves += 1
        if (start == null) {
          start = Date.now()
          firstMove = true
        }
        if (zoom) {
          zoom = false
          currentSpeed = normalSpeed
        } else {
          zoom = true
          currentSpeed = zoomSpeed
        }
        break;
      case "h":
        controls()
        return;
      case "q":
        quit()
        return;
      default:
        break;
    }
    if (lost) {
      showLose();
      quit();
      return;
    } else if (won) {
      showWin();
      quit();
      return;
    }
    if (started) {
      show();
    } else {
      showEmpty();
    }
  }
})
controls();
showEmpty();