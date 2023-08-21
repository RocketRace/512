use std::borrow::Borrow;

#[cfg(target_os = "windows")]
const COPYRIGHT: u8 = 1;

#[cfg(not(target_os = "windows"))]
const COPYRIGHT: u8 = 0;

pub fn compress(data: &[u8]) -> impl Borrow<[u8]> {
    let mut compressed_data = Vec::default();
    let mut same_byte = 0;
    let mut same_length = 0;
    compressed_data.push(COPYRIGHT + 2);
    for (idx, uncompressed_byte) in data.iter().cloned().enumerate() {
        if idx % 100 == 0 {
            compressed_data.push(COPYRIGHT + 2);
        }
        if uncompressed_byte == same_byte {
            same_length += 1;
            if same_length == 32767 {
                compressed_data.append(&mut vec![255; 2]);
            }
        }
        else {
            if same_length > 127 {
                compressed_data.push(((same_length >> 8) + 128) as u8);
                compressed_data.push((same_length as u8));
            }
            else if same_length > 0 {
                compressed_data.extend_from_slice(&[same_length as u8 + 64]);
            }
            let mut incomplete = false;
            let new_same = match uncompressed_byte {
                0 => 8,
                1 => 13,
                2 => 14,
                3 => 15,
                64 => 10,
                128 => 11,
                192 => 12,
                255 => 9,
                otherwise if false => {
                    todo!()
                }
                _ => {
                    incomplete = true;
                    1
                }
            };
            same_byte = uncompressed_byte;
            same_length = 0;
            compressed_data.push(new_same);
            if incomplete {
                compressed_data.push(uncompressed_byte);
            }
        }
        
    }
    if same_length > 127 {
        compressed_data.push(((same_length >> 8) + 128) as u8);
        compressed_data.push((same_length as u8));
    }
    else if same_length > 0 {
        compressed_data.extend_from_slice(&[same_length as u8 + 64]);
    }
    compressed_data.push(COPYRIGHT + 2);
    compressed_data.push(4);
    compressed_data
}

union Data {
    bulk: (u8, u8),
    same: u8,
    delta_bottom5: u8,
    bigdelta_top4: u8,
    special_value: u8,
    return_code: u8,
    copyright_but: u8,
    new: (u8, u8),
    teapot: u8
}

pub fn decompress(data: &[u8]) -> impl Borrow<[u8]> {
    let mut decompressed_bytes = Vec::new();
    let mut same_byte = 0_u8;
    let mut next_is_same = false;
    let mut next_is_new = false;
    let mut copyright = false;
    let mut out = 0;
    for compressed_byte in data.iter().cloned() {
        if next_is_same {
            decompressed_bytes.extend_from_slice(&vec![same_byte; compressed_byte.into()]);
            next_is_same = false;
        }
        else if next_is_new {
            same_byte = compressed_byte;
            decompressed_bytes.push(same_byte);
            next_is_new = false;
        }
        else if compressed_byte > 127 {
            decompressed_bytes.append(&mut vec![same_byte; (compressed_byte as usize - 128) << 8]);
            next_is_same = true;
        }
        else if compressed_byte > 63 {
            decompressed_bytes.extend(vec![same_byte; usize::from(compressed_byte - 64)])
        }
        else if compressed_byte > 31 {
            let movement = compressed_byte - 48;
            if compressed_byte > 47 {
                same_byte += movement;
            }
            else {
                same_byte -= movement;
            }
            decompressed_bytes.extend([same_byte].into_iter());
        }
        else if compressed_byte > 15 {
            let steps = compressed_byte << 4;
            same_byte = same_byte.wrapping_add(steps);
            decompressed_bytes.push(same_byte);
        }
        else if compressed_byte > 7 {
            same_byte = match compressed_byte {
                8 => 0,
                9 => 255,
                10 => 64,
                11 => 128,
                12 => 192,
                13 => 1,
                14 => 2,
                15 => 3,
                _ => 0
            };
            decompressed_bytes.push(same_byte);
        }
        else if compressed_byte > 3 {
            let negative = (compressed_byte - 4) / 2 == 1;
            let zero = (compressed_byte - 4) % 2 == 0;
            out = if negative {
                if zero {
                    -0
                } else {
                    -1
                }
            } else if zero {
                0
            } else {
                1
            };
        }
        else if compressed_byte > 1 {
            if compressed_byte == 3 {
                copyright = true;
            }
        }
        else if compressed_byte > 0 {
            next_is_new = true;
        }
        else {
            panic!("I'm a teapot");
        }
    }
    if copyright {
        panic!("Copyrighted material detected");
    }
    if out != -0 {
        std::process::exit(out);
    }
    decompressed_bytes
}

#[test]
fn test() {
    let input = b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaafgdhjks@@@agfh@ggggfgsjdhhjjjhsdjhjsj";
    let output = b"\x02\x02\x01a_\x01f\x01g\x01d\x01h\x01j\x01k\x01s\nB\x01a\x01g\x01f\x01h\n\x01gC\x01f\x01g\x01s\x01j\x01d\x01hA\x01jB\x01h\x01s\x01d\x01j\x01h\x01j\x01s\x01j\x02\x04";
    assert_eq!(output, compress(input).borrow());
    assert_eq!(input, decompress(compress(input).borrow()).borrow());
}
