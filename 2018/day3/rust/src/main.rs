#[macro_use] extern crate lazy_static;
use std::error::Error;
use std::str::FromStr;
use std::io::{self, Read, Write};

use regex::Regex;

type Result<T> = std::result::Result<T, Box<Error>>;

fn main() -> Result<()> {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf)?;
    let mut claims: Vec<Claim> = vec![];

    for line in buf.lines() {
        //let claim = line.parse()?; 这样也可以，但传递的错误信息不好看
        let claim = line.parse().or_else(|err| {
            Err(Box::<Error>::from(format!("failed to parse '{:?}': {}", line, err)))
        })?;
        claims.push(claim);
    }
    // part1(&buf)?;
    // part2(&buf)?;
    Ok(())
}

fn part1(input: &str) -> Result<()> {
    writeln!(io::stdout(), "{}", 42)?;
    Ok(())
}

fn part2(input: &str) -> Result<()> {
    Err(From::from("could not find two correct box ids"))
}

#[derive(Debug)]
struct Claim{
    id: u32,
    x: u32,
    y: u32,
    width: u32,
    height: u32,
}

impl Claim {
    fn iter_points(&self) -> IterPoints {
        // 有点想念Python的yield😂
        IterPoints{
            claim: self,
            px: self.x,
            py: self.y,
        }
    }
}

// 迭代器对象
// 该结构体的生命周期必须小于claim借用的生命周期
struct IterPoints<'c> {
    claim: &'c Claim,
    px: u32,
    py: u32,
}


// ? IterPoints<'C>是独立的类型，显式声明
impl<'c> Iterator for IterPoints<'c> {
    type Item = (u32, u32);

    fn next(&mut self) -> Option<(u32, u32)> {
        if self.py >= self.claim.y + self.claim.height {
            self.py = self.claim.y;
            self.px += 1;
        }
        if self.px >= self.claim.x + self.claim.width {
            return None;
        }
        let (px, py) = (self.px, self.py);
        self.py += 1;
        Some((px, py))
    }
}

// parse使用的trait，没有生命周期参数，所以不能转换存在借用的结构
impl FromStr for Claim {
    type Err = Box<Error>;

    fn from_str(s: &str) -> Result<Claim> {
        // 编译期函数执行(CTFE)受限的 work around
        // 运行时执行且执行一次，结果进入只读内存区
        lazy_static! {
            static ref RE: Regex = Regex::new(r"(?x) //忽略空格并允许行#注释
                \# #转义开始的'#'
                (?P<id>[0-9]+)
                \s+@\s+
                (?P<x>[0-9]+),(?P<y>[0-9]+)):
                \s+
                (?P<width>[0-9]+)x(?P<height>[0-9]+)
            ").unwrap();
        }

        let caps = match RE.captures(s) {
            None => return Err(Box::<Error>::from("unrecoginzed claim")),
            Some(caps) => caps,
        };

        Ok(Claim{
            id: caps["id"].parse()?,
            x: caps["x"].parse()?,
            y: caps["y"].parse()?,
            width: caps["width"].parse()?,
            height: caps["height"].parse()?,
        })
    }
}
