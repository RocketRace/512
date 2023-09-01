#!/usr/bin/env -S cargo +nightly -Zscript
//! ```cargo
//! [dependencies]
//! rand = "0.8.5"
//! ti = { version = "1.2", git = "https://github.com/RocketRace/ti.git", features = ["images"] }
//! ```
use ::{std::ops::{Index, IndexMut}, rand::{seq::IteratorRandom, thread_rng}, ti::{color::Color, event::{Direction, Event}, screen::{Blit, Screen}, sprite::{Atlas, ColorMode, Sprite}}};

const OFFSET_X: u16 = 2;
const OFFSET_Y: u16 = 4;

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
}

fn spawn_food(grid: &mut Grid) -> Option<()> {
    (0..16)
        .filter(|&i| grid[i].is_none())
        .choose(&mut thread_rng())
        .map(|i| grid[i] = Some(Cell::new(if rand::random::<f64>() < 0.9 { 1 } else { 2 })))
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

fn is_over(grid: &Grid) -> bool {
    [Direction::Up, Direction::Down, Direction::Right, Direction::Left].into_iter().all(|dir| {
        let mut clone = *grid;
        gravity(&mut clone, dir).is_none()
    })
}

fn is_won(grid: &Grid) -> bool {
    grid.iter().any(|c| c.value >= 11) // 2^11 = 2048
}

fn gravity(grid: &mut Grid, direction: Direction) -> Option<(Slides, Grid, u32)> {
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
            match (grid[slice[src]], buf[slice[dst]]) {
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
    if *grid != buf { Some((sliders, buf, scored)) } else { None }
}

fn main() {
    let mut screen = Screen::new_pixels(32, 24);
    let sprites = Atlas::open("atlas.png", ColorMode::Rgb, true).map(|atlas| (0..16).map(|i| atlas.sprite(i % 4 * 4, i / 4 * 4, 4, 4, 1, 1)).collect::<Vec<Sprite>>()).expect("sprite error");
    let mut grid = Grid::default();
    let mut next_grid = Grid::default();
    spawn_food(&mut grid).unwrap();
    spawn_food(&mut grid).unwrap();
    
    let mut sliding = false;
    let mut over = false;
    let mut won = false;
    let mut inhaling = true;
    let mut breath = 0;
    let mut score = 0;
    let mut best = 0;
    screen
        .start_loop(60, |screen, event| {
            if !sliding {
                if let Some(event) = event {
                    if let Some(dir) = event.direction_wasd() {
                        if let Some((sliders, new_grid, scored)) = gravity(&mut grid, dir) {
                            sliding = true;
                            score += scored;
                            best = best.max(score);
                            next_grid = new_grid;
                            for (slider, cells) in sliders {
                                if let Some(c) = grid[slider].as_mut() {
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
                            if !won && is_won(&grid) {
                                won = true;
                            }
                        }
                        else if !over && is_over(&grid) {
                            over = true;
                        }
                    } else if let Event::Char('r') = event {
                        grid = Grid::default();
                        spawn_food(&mut grid);
                        spawn_food(&mut grid);
                        over = false;
                        score = 0;
                    }
                }
            }
            else if grid.iter_mut().fold(true, |equal, cell| {
                if cell.offset != cell.intention { 
                    cell.offset.0 += cell.intention.0.signum() * cell.speed;
                    cell.offset.1 += cell.intention.1.signum() * cell.speed;
                }
                equal && cell.offset == cell.intention
            }) {
                sliding = false;
                grid = next_grid;
                grid.iter_mut().for_each(|cell| *cell = Cell { value: cell.value, ..Default::default() });
                spawn_food(&mut grid);
            }
            if inhaling {
                breath += 1; if breath == 47 { inhaling = false; }
            } else {
                breath -= 1; if breath == 0  { inhaling = true;  }
            }
            let playing_color = Color::from_ansi_greyscale(breath / 4 + 6);
            let lost_color    = Color::from_rgb_approximate(breath * 3 + 112, 64,               64              );
            let won_color     = Color::from_rgb_approximate(64,               breath * 3 + 112, 64              );
            let score_color   = Color::from_rgb_approximate(breath * 3 + 112, 64,               breath * 3 + 112);
            let record_color  = Color::from_rgb_approximate(breath * 3 + 112, breath * 3 + 112, 64              );
            let best_color    = Color::from_rgb_approximate(64,               breath * 3 + 112, 64              );
            let border_color = if over { if won { won_color } else { lost_color }} else { playing_color };
            draw_borders(screen, OFFSET_X - 1, OFFSET_Y - 1, border_color);
            draw_cells(screen, grid, &sprites, OFFSET_X, OFFSET_Y);
            draw_score(screen, score, OFFSET_X + 20, OFFSET_Y, if score == best { record_color } else { score_color });
            draw_score(screen, best, OFFSET_X + 24, OFFSET_Y,best_color );
            Ok(())
        })
        .unwrap()
}
