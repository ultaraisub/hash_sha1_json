# 概要

- test01
    - 大量ファイルのテスト
- test02
    - 0Bytesファイルのテスト
- test03
    - 約2.5MBytesファイルのテスト
- test04
    - 複雑なディレクトリ構造のテスト
- test05
    - 別のディレクトリに同じ名前のファイルがある場合のテスト
- test06
    - 変なファイル名のテスト
- test07
    - ファイル名として大文字・小文字を区別するかのテスト
- test08
    - 深いディレクトリ構造のテスト
- test09
    - ファイルが存在しないディレクトリを含むディレクトリ構造のテスト

# 詳細
## test04
```
└── test
      └── test04
            ├── a
            │   ├── aa
            │   │    └── aa.txt
            │   ├── ab
            │   │    └── ab.txt
            │   └── a.txt
            ├── b
            │   ├── ba
            │   │    ├── baa
            │   │    │    └── baa.txt
            │   │    ├── bab
            │   │    │    └── bab.txt
            │   │    └── ba.txt
            │   ├── bb
            │   │    ├── bba
            │   │    │    └── bba.txt
            │   │    ├── bbb
            │   │    │    └── bbb.txt
            │   │    └── bb.txt
            │   └── b.txt
            ├── c
            │   ├── ca
            │   │    ├── caa
            │   │    │    ├── caaa
            │   │    │    │     ├── caaaa
            │   │    │    │     │    └── caaaa.txt
            │   │    │    │     ├── caaab
            │   │    │    │     │    └── caaab.txt
            │   │    │    │     └── caaa.txt
            │   │    │    ├── caab
            │   │    │    │     ├── caaba
            │   │    │    │     │     └── caaba.txt
            │   │    │    │     ├── caabb
            │   │    │    │     │     └── caabb.txt
            │   │    │    │     └── caab.txt
            │   │    │    └── caa.txt
            │   │    └── ca.txt
            │   ├── cb
            │   │    └── cb.txt
            │   └── c.txt
            └── d
                └── d.txt

```


## test05

