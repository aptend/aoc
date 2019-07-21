use std::collections::HashSet;
use std::error::Error;
use std::io::{self, Write, Read};

type Result<T> = std::result::Result<T, Box<Error>>;

fn main() -> Result<()> {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf)?;
    part1(&buf)?;
    part2(&buf)?;
    Ok(())
}


fn part1(input: &str) -> Result<()> {
    let mut freq = 0;
    for line in input.lines() {
        let change: i32 = line.parse()?;
        freq += change;
    }
    writeln!(io::stdout(), "{}", freq)?;
    Ok(())
}

fn part2(input: &str) -> Result<()> {
    let mut freq = 0;
    let mut seen = HashSet::new();
    seen.insert(0);
    loop {
        for line in input.lines() {
            let change: i32 = line.parse()?;
            freq += change;
            if seen.contains(&freq) {
                writeln!(io::stdout(), "{}", freq)?;
                return Ok(());
            }
            seen.insert(freq);
        }
    }
    
    // for line in input.lines().cycle() {
    //     let change: i32 = line.parse()?;
    //     freq += change;
    //     if seen.contains(&freq) {
    //         writeln!(io::stdout(), "{}", freq)?;
    //         return Ok(())
    //     }
    //     seen.insert(freq);
    // }
    // writeln!(io::stdout(), "{}", "can't reach here")?;
    // Ok(())
}
