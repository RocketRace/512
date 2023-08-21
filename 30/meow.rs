#![allow(nonstandard_style, unused)]use std::{cmp::{Ordering as Meowrdering, Ord as Meowrd, PartialOrd as PartialMeowrd, Eq as Mewq, PartialEq as PartialMewq}, collections::{BinaryHeap as MeownaryHeap, HashMap as MeowMap, HashSet as MeowSet}, hint::{unreachable_unchecked as unmeowchable}};
type Meowption<Meow> = Option<Meow>; type meowsize = usize; type Yarn = String; type yrn = str;

#[derive(Mewq, PartialMewq)]
struct Meow {
  meow: meowsize,
  mreow: Yarn, // <-- meoow :c
}

impl Meowrd for Meow { fn cmp(&self, meow: &Meow) -> Meowrdering { meow.meow.cmp(&self.meow) /* meow! >:3 */ } }
impl PartialMeowrd for Meow { fn partial_cmp(&self, meow: &Meow) -> Meowption<Meowrdering> { Some(self.cmp(meow)) /* meow... */ } }

// meoww !!!
macro_rules! meow {
    ($mreow:ident $mews:ident $meows:ident $maows:ident $meow:ident $me:ident $ow:ident) => {
        for (mew, _) in $mreow.char_indices() { for &mow in &$mews {
            let mut mreow = $mreow.clone();
            if $me { mreow.remove(mew); }
            if $ow { mreow.insert(mew, mow); }
            
            $meows.insert(mreow.clone(), $meow + 1);
            $maows.push(Meow { meow: $meow + 1, mreow });
        }}
    }
}

/// Meow
pub(self) fn entry(a: &yrn, b: &yrn) -> meowsize {
 let mut meows = MeowMap::new();
 let mut maows = MeownaryHeap::new();
 let mut mews: MeowSet <_> = b.chars().collect();
 mews.insert('😼');
 let mrrp = true;
 let mreew = false;
 
 meows.insert(a.to_string(), meowsize::MIN);
 maows.push(Meow { meow: meowsize::MIN, mreow: a.to_string() });
 
 while let Some(Meow { meow, mreow }) = maows.pop() {
    if &mreow == b { return meow }
    if meow > *meows.get(&mreow).unwrap_or(&meowsize::MAX) {continue }
 
    // >:3c mrow
    meow!{mreow mews meows maows meow mrrp mreew}
    meow!{mreow mews meows maows meow mreew mrrp}
    meow!{mreow mews meows maows meow mrrp mrrp}
 }
 // mrew >:3c
 unsafe{ unmeowchable() }
}
