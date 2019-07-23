use std::error::Error;
use std::str::FromStr;
use std::collections::HashMap;
use std::io::{self, Read, Write};

// 2018 edition
use regex::Regex;
use lazy_static::lazy_static;


macro_rules! err {
    ($($e:tt)*) => {
        Err(Box::<Error>::from(format!($($e)*))) //具体Result类型会在函数中利用返回值推断
    };
}


type Result<T> = std::result::Result<T, Box<dyn Error>>; //dyn显示表明Error是trait
type Grid = HashMap<(u32, u32), u32>;

fn main() -> Result<()> {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf)?;

    let mut claims: Vec<Claim> = vec![];
    for line in buf.lines() {
        //let claim = line.parse()?; 这样也可以，但传递的错误信息不好看
        let claim = line.parse().or_else(|err| {
            err!("failed to parse {:?}: {}", line, err)
        })?;
        claims.push(claim);
    }

    let mut grid = Grid::new();
    for claim in &claims { // 等效于 in claims.iter() {
        for (x, y) in claim.iter_points() {
            *grid.entry((x, y)).or_default() += 1;
        }
    }

    part1(&grid)?;
    part2(&claims, &grid)?;
    Ok(())
}

fn part1(grid: &Grid) -> Result<()> {
    // values借用，filter再借用，所以&&, 这在filter的文档中有记录
    let count = grid.values().filter(|&&count| count > 1).count();
    writeln!(io::stdout(), "contested points: {}", count)?;
    Ok(())
}

fn part2(claims: &[Claim], grid: &Grid) -> Result<()> {
    for claim in claims { // 这里的claims本身就是借用
        if claim.iter_points().all(|p| grid[&p] == 1){
            writeln!(io::stdout(), "uncontested claim: {}", claim.id)?;
            return Ok(());
        }
    }
    err!("could not find uncontested claim")
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
    type Err = Box<dyn Error>; // 转换成统一的错误类型，一个trait 对象

    fn from_str(s: &str) -> Result<Claim> {
        // 编译期函数执行(CTFE)受限的 work around
        // 运行时执行且执行一次，结果进入只读内存区
        lazy_static! {
            static ref RE: Regex = Regex::new(r"(?x) #忽略空格并允许注释
                \#  # 转义掉开头的#号
                (?P<id>[0-9]+)
                \s+@\s+
                (?P<x>[0-9]+),(?P<y>[0-9]+):
                \s+
                (?P<width>[0-9]+)x(?P<height>[0-9]+)
            ").unwrap();
        }

        let caps = match RE.captures(s) {
            None => return err!("unrecoginzed claim"),
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
