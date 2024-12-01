import gleam/dict
import gleam/int
import gleam/io
import gleam/list
import gleam/string
import gleam/yielder
import utils/stdin

fn build_lists(nums: List(String)) -> Result(#(List(Int), List(Int)), String) {
  let tuples =
    nums
    |> list.try_map(fn(x) {
      case x |> string.trim |> string.split("   ") {
        [a, b] ->
          case int.parse(a) {
            Ok(a) ->
              case int.parse(b) {
                Ok(b) -> Ok(#(a, b))
                Error(_) ->
                  Error(
                    "Invalid input, second number " <> b <> " is not an integer",
                  )
              }
            Error(_) ->
              Error("Invalid input, first number " <> a <> " is not an integer")
          }
        _ -> Error("Invalid input, string has more or less than two terms")
      }
    })
  case tuples {
    Ok(tuples) -> Ok(list.unzip(tuples))
    Error(e) -> Error(e)
  }
}

fn part1(lista: List(Int), listb: List(Int)) -> Int {
  list.zip(lista, listb)
  |> list.fold(0, fn(acc, ab) { acc + int.absolute_value(ab.0 - ab.1) })
}

fn part2(lista: List(Int), listb: List(Int)) -> Int {
  let counts =
    list.fold(listb, dict.new(), fn(acc, b) {
      case dict.get(acc, b) {
        Ok(count) -> dict.insert(acc, b, count + 1)
        Error(_) -> dict.insert(acc, b, 1)
      }
    })
  list.fold(lista, 0, fn(acc, a) {
    case dict.get(counts, a) {
      Ok(count) -> acc + a * count
      Error(_) -> acc
    }
  })
}

pub fn main() {
  let nums = stdin.stdin() |> yielder.to_list()
  let lists = build_lists(nums)
  let #(lista, listb) = case lists {
    Ok(lists) -> lists
    Error(e) -> {
      io.println_error(e)
      panic
    }
  }
  let lista = list.sort(lista, int.compare)
  let listb = list.sort(listb, int.compare)

  io.println(int.to_string(part1(lista, listb)))
  io.println(int.to_string(part2(lista, listb)))
}
