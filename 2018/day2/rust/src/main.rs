use std::error::Error;
use std::io::{self, Read, Write};

type Result<T> = std::result::Result<T, Box<Error>>;

fn main() -> Result<()> {
    let mut buf = String::new();
    io::stdin().read_to_string(&mut buf)?;
    part1(&buf)?;
    part2(&buf)?;
    Ok(())
}

fn part1(input: &str) -> Result<()> {
    //初始化256数组
    let mut frequencies = [0u8; 256];
    let (mut twos, mut threes) = (0, 0);
    for line in input.lines() {
        // 使用数组模拟字典，需要确定输入不越界
        if !line.is_ascii() {
            // std::error中定义了 impl From<&str> for Box<dyn Error>
            // 这里手动转换
            return Err(From::from("part1 only supports ASCII"));
        }
        for f in frequencies.iter_mut() {
            *f = 0;
        }
        // as_bytes的b是u8, 索引要用usize，依平台切换32/64
        for b in line.as_bytes().iter().map(|&b| b as usize) {
            // 溢出时截断在边界值，对应overflowing_add，给提示后自然溢出
            frequencies[b] = frequencies[b].saturating_add(1);
        }
        if frequencies.iter().any(|&f| f == 2) {
            twos += 1;
        }
        if frequencies.iter().any(|&f| f == 3) {
            threes += 1;
        }
    }
    writeln!(io::stdout(), "{}", twos * threes)?;
    Ok(())
}

fn part2(input: &str) -> Result<()> {
    let ids: Vec<&str> = input.lines().collect();
    for i in 0..ids.len(){
        for j in i+1..ids.len(){
            if let Some(common) = common_letters_one_mismatched(ids[i], ids[j]){
                writeln!(io::stdout(), "{}", common)?;
                return Ok(());
            }
        }
    }
    Err(From::from("could not find two correct box ids"))
}

fn common_letters_one_mismatched(id1: &str, id2:&str) -> Option<String>{
    if id1.len() != id2.len(){
        return None;
    }

    let mut one_mismatch_found = false;
    for (c1, c2) in id1.chars().zip(id2.chars()){
        if c1 != c2{
            if one_mismatch_found{
                return None;
            }
            one_mismatch_found = true;
        }
    }
    // 全部匹配或者错位1个
    Some(
        id1.chars().zip(id2.chars())
        .filter(|&(c1, c2)| c1 == c2)
        .map(|(c, _)| c) // c1 == c2 选其中一个
        .collect()
    )
}
