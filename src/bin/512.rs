#!/usr/bin/env -S cargo +nightly -Zscript
//! ```cargo
//! [package]
//! edition = "2021"
//! authors = [ "RocketRace <oliviaspalmu@gmail.com>" ]
//! description = "The game of 2048 for the Esolangs Code Guessing round 42"
//! 
//! [dependencies]
//! rand = "0.8.5"
//! ti = { version = "1.2", git = "https://github.com/RocketRace/ti.git", features = ["images"] }
//! ```
use ::{std::ops::{Index, IndexMut}, rand::{seq::IteratorRandom, thread_rng}, ti::{color::Color, event::{Direction, Event}, screen::{Blit, Screen}, sprite::{Atlas, ColorMode, Sprite}}};

#[derive(Clone, Copy, PartialEq, Default)]
struct Cell {
    value: u8,
    offset: (i16, i16),
    intention: (i16, i16),
    speed: i16
}
impl Cell {
    fn new(value: u8) -> Self {
        Cell { value, ..Default::default() }
    }
}
#[derive(Default, PartialEq, Clone, Copy)]
struct Grid([[Option<Cell>; 4]; 4]);
type Slides = Vec<(u16, u16)>;

impl Index<u16> for Grid {
    type Output = Option<Cell>;
    fn index(&self, index: u16) -> &Self::Output {
        &self.0[index as usize / 4][index as usize % 4]
    }
}
impl IndexMut<u16> for Grid {
    fn index_mut(&mut self, index: u16) -> &mut Self::Output {
        &mut self.0[index as usize / 4][index as usize % 4]
    }
}
impl Grid {
    fn iter(&self) -> impl Iterator<Item = &Cell> {
        self.0.iter().flatten().flatten()
    }
    fn iter_mut(&mut self) -> impl Iterator<Item = &mut Cell> {
        self.0.iter_mut().flatten().flatten()
    }
    fn spawn_food(&mut self) -> Option<()> {
        (0..16)
            .filter(|&i| self[i].is_none())
            .choose(&mut thread_rng())
            .map(|i| self[i] = Some(Cell::new(if rand::random::<f64>() < 0.9 { 1 } else { 2 })))
    }
    fn gravity(&mut self, direction: Direction) -> Option<(Slides, Grid, u32)> {
        let vertical   = [[0, 4, 8, 12], [1, 5, 9, 13], [2, 6, 10, 14], [3,  7,  11, 15]];
        let horizontal = [[0, 1, 2, 3 ], [4, 5, 6, 7 ], [8, 9, 10, 11], [12, 13, 14, 15]];
        let slices = match direction {
            Direction::Right => horizontal.map(reversed),
            Direction::Left  => horizontal,
            Direction::Up    => vertical,
            Direction::Down  => vertical.map(reversed),
        };
    
        let mut buf = Grid::default();
        let mut sliders = vec![(0, 0); 16];
        let mut scored = 0;
        for slice in slices {
            let mut dst = 0;
            for src in 0..4 {
                match (self[slice[src]], buf[slice[dst]]) {
                    (None, _) => (),
                    (Some(n), None) => {
                        buf[slice[dst]] = Some(n);
                        sliders.push((slice[src], (src - dst) as u16));
                    }
                    (Some(n), Some(m)) => {
                        if n.value == m.value {
                            buf[slice[dst]] = Some(Cell::new(n.value + 1));
                            sliders.push((slice[src], (src - dst) as u16));
                            scored += 1 << (n.value + 1);
                        } else {
                            // this can never panic: dst <= src && this match arm is only
                            // possible after executing the previous arm once => dst < 3
                            buf[slice[dst + 1]] = Some(n);
                            sliders.push((slice[src], (src - dst - 1) as u16));
                        }
                        dst += 1;
                    }
                }
            }
        }
        if *self != buf { Some((sliders, buf, scored)) } else { None }
    }
}


fn draw_borders(screen: &mut Screen, offset_x: u16, offset_y: u16, color: Color) {
    screen.draw_sprite(&Sprite::rectangle(18, 18, Some(color), 0), offset_x, offset_y, Blit::Set);
    screen.draw_sprite(&Sprite::rectangle(16, 16, None, 0), offset_x + 1, offset_y + 1, Blit::Subtract);
}

fn draw_cells(screen: &mut Screen, grid: Grid, sprites: &[Sprite], offset_x: u16, offset_y: u16) {
    (0..16).for_each(|i| {
        let (x, y) = (i % 4, i / 4);
        let rgb = (0..=5).choose_multiple(&mut thread_rng(), 3);
        let fuzzy = Sprite::rectangle(4, 4, Some(Color::from_ansi_components(rgb[0], rgb[1], rgb[2])), 1);
        if let Some(Cell {value, offset, .. }) = grid[i] {
            let sprite = sprites.get(value as usize - 1).unwrap_or(&fuzzy);
            screen.draw_sprite(sprite, (x * 4 + offset_x).wrapping_add_signed(offset.0), (y * 4 + offset_y).wrapping_add_signed(offset.1), Blit::Set);
        }
    })
}

fn draw_score(screen: &mut Screen, score: u32, offset_x: u16, offset_y: u16, color: Color) {
    for i in 2..32 {
        screen.draw_pixel_colored(offset_x + i % 2, offset_y + i / 2, if score & (1 << i) != 0 { Blit::Add } else { Blit::Subtract}, Some(color));
    }
}

fn reversed<const N: usize, T>(array: [T; N]) -> [T; N] {
    let mut copy = array;
    copy.reverse();
    copy
}

struct Game {
    grid: Grid,
    next_grid: Grid,
    sliding: bool,
    over: bool,
    won: bool,
    score: u32,
    grid_pos: (u16, u16),
    score_pos: (u16, u16)
}

impl Game {
    fn new(grid_pos: (u16, u16), score_pos: (u16, u16)) -> Self {
        let mut this = Game {
            grid: Grid::default(),
            next_grid: Grid::default(),
            sliding: false,
            over: false,
            won: false,
            score: 0,
            grid_pos,
            score_pos
        };
        this.grid.spawn_food();
        this
    }
    fn tick(&mut self, screen: &mut Screen, event: Option<Event>, best: &mut u32, breath: u8, sprites: &[Sprite]) {
        if !self.sliding {
            if let Some(event) = event {
                if let Some(dir) = event.direction_wasd() {
                    if let Some((sliders, new_grid, scored)) = self.grid.gravity(dir) {
                        self.sliding = true;
                        self.score += scored;
                        *best = (*best).max(self.score);
                        self.next_grid = new_grid;
                        for (slider, cells) in sliders {
                            if let Some(c) = self.grid[slider].as_mut() {
                                let dist = cells as i16 * 4;
                                c.speed = cells as i16;
                                c.intention = match dir {
                                    Direction::Up    => (0, -dist),
                                    Direction::Down  => (0,  dist),
                                    Direction::Right => ( dist, 0),
                                    Direction::Left  => (-dist, 0),
                                };
                            };
                        }
                        if !self.won && self.grid.iter().any(|c| c.value >= 11) {
                            // 2^11 = 2048
                            self.won = true;
                        }
                    }
                    else if !self.over && [Direction::Up, Direction::Down, Direction::Right, Direction::Left].into_iter().all(|dir| self.grid.clone().gravity(dir).is_none()) {
                        self.over = true;
                    }
                } else if let Event::Char('r') = event {
                    self.grid = Grid::default();
                    self.grid.spawn_food();
                    self.grid.spawn_food();
                    self.over = false;
                    self.score = 0;
                }
            }
        }
        else if self.grid.iter_mut().fold(true, |equal, cell| {
            if cell.offset != cell.intention { 
                cell.offset.0 += cell.intention.0.signum() * cell.speed;
                cell.offset.1 += cell.intention.1.signum() * cell.speed;
            }
            equal && cell.offset == cell.intention
        }) {
            self.sliding = false;
            self.grid = self.next_grid;
            self.grid.iter_mut().for_each(|cell| *cell = Cell { value: cell.value, ..Default::default() });
            self.grid.spawn_food();
        }
        
        let playing_color = Color::from_ansi_greyscale(breath / 4 + 6);
        let c = breath * 3 + 112;
        let lost_color    = Color::from_rgb_approximate(c,  64, 64);
        let won_color     = Color::from_rgb_approximate(64, c,  64);
        let score_color   = Color::from_rgb_approximate(c,  64, c );
        let record_color  = Color::from_rgb_approximate(c,  c,  64);
        let border_color = if self.over { if self.won { won_color } else { lost_color }} else { playing_color };
        draw_borders(screen, self.grid_pos.0, self.grid_pos.1, border_color);
        draw_cells(screen, self.grid, sprites, self.grid_pos.0 + 1, self.grid_pos.1 + 1);
        draw_score(screen, self.score, self.score_pos.0, self.score_pos.1, if self.score == *best { record_color } else { score_color });
    }
}

fn main() {
    let mut screen = Screen::new_pixels(54, 24);
    let sprites = Atlas::open("atlas.png", ColorMode::Rgb, true).map(|atlas| (0..16).map(|i| atlas.sprite(i % 4 * 4, i / 4 * 4, 4, 4, 1, 1)).collect::<Vec<Sprite>>()).expect("sprite error");
    
    let mut game = Game::new((1, 3), (22, 4));
    let mut redo = false;
    let mut p2 = Game::new((35, 3), (30, 4));
    let mut best = 0;

    let mut inhaling = true;
    let mut breath = 0;

    screen
        .start_loop(60, |screen, event| {
            if let Some(Event::Char('y')) = event {
                redo = true;
            }
            if inhaling {
                breath += 1; if breath == 47 { inhaling = false; }
            } else {
                breath -= 1; if breath == 0  { inhaling = true;  }
            }
            game.tick(screen, event, &mut best, breath, &sprites);
            if redo {
                p2.tick(screen, event, &mut best, breath, &sprites);
            }
            let best_color = Color::from_rgb_approximate(64, breath * 3 + 112, 64);
            draw_score(screen, best, 26, 4, best_color);
            Ok(())
        })
        .unwrap()
}
