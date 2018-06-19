# otus_task_02

> "часть" is everywhere

Habr Stats is tool for analyzing the frequency of using words in the main feed of habr.com

### Installation

1. clone or download the project and install the requirements:
```zsh
$ git clone https://github.com/mentatij/otus_task_02.git
$ cd otus_task_01
$ pip install -r REQUIREMENTS.txt
```

### Example of usage

From command line:

```zsh
$ python3 habr_stat.py
Pages parsed: 10
Weeks parsed (may be not fully): 2
----------------------------------------------------------------------------------------------------
Start of week | End of week | Top5 most popular words
----------------------------------------------------------------------------------------------------
  2018-06-18  | 2018-06-24  | разработка оптимизация часть помощь security
----------------------------------------------------------------------------------------------------
  2018-06-11  | 2018-06-17  | дайджест материал hashflare фронтенд неделя
----------------------------------------------------------------------------------------------------
```
Full format of usage is ```habr_stat.py [-h] [--pages int] [--start int] [--min int] [--top int] [--url str]```.

Use ```habr_stat.py --help``` to see more details.

There is opportunity to use tool not only for main habr.com feed by using parametr ```url```.
```zsh
$ python3 habr_stat.py --url=https://habr.com/top/
Pages parsed: 6
Weeks parsed (may be not fully): 1
----------------------------------------------------------------------------------------------------
Start of week | End of week | Top5 most popular words
----------------------------------------------------------------------------------------------------
  2018-06-18  | 2018-06-24  | разработка помощь security работа доклад
----------------------------------------------------------------------------------------------------
```

### Docs
No additional docs, just this README.md

### Contributing

1. Fork it (<https://github.com/mentatij/otus_task_02.git>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
