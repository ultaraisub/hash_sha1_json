#!/usr/bin/env python3
import hashlib
import argparse
import sys
import os
import json

def calculate_sha1(filepath):
    """FileのSHA1を計算する"""
    sha1 = hashlib.sha1()

    try:
        with open(filepath, 'rb') as f:
            # Fileを1MBずつ読み込んで処理
            while chunk := f.read(1024 * 1024):
                sha1.update(chunk)
        return sha1.hexdigest()
    except Exception as e:
        print(f"Error: {filepath}を読み込めません: {e}", file=sys.stderr)
        return None

def process_path(path):
    """Fileまたはディレクトリを処理する"""
    if not os.path.exists(path):
        print(f"Error: Pathが見つかりません: {path}", file=sys.stderr)
        sys.exit(1)
    
    # Symbolic Linkをチェック
    if os.path.islink(path):
        print(f"Warning: Symbolic LinkはSkipされます: {path}", file=sys.stderr)
        return []
    
    results = []

    # Fileの場合
    if os.path.isfile(path):
        sha1_hash = calculate_sha1(path)
        if sha1_hash:
            results.append({
                "path": path,
                "type": "file",
                "sha1": sha1_hash
            })
    
    # ディレクトリの場合
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            # Symbolic Link ディレクトリを除外
            dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]

            # Fileを処理
            for filename in sorted(files):
                filepath = os.path.join(root, filename)

                # Symbolic Link FileをSkip
                if os.path.islink(filepath):
                    continue
                sha1_hash = calculate_sha1(filepath)
                if sha1_hash:
                    results.append({
                        "path": filepath,
                        "type": "file",
                        "sha1": sha1_hash
                    })
            
            # ディレクトリを処理
            for dirname in sorted(dirs):
                dirpath = os.path.join(root, dirname)
                results.append({
                    "path": dirpath,
                    "type": "directory"
                })
    
    return results

def load_json(json_file):
    """JSON Fileを読み込む"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON Fileが見つかりません: {json_file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: JSON Fileを読み込めません: {e}", file=sys.stderr)
        sys.exit(1)

def compare_results(current, previous):
    """現在の結果と過去の結果を比較する"""
    # PathをKeyにしたmapを作成する
    current_map  = {item["path"]: item for item in current}
    previous_map = {item["path"]: item for item in previous}

    comparison = {
        "added": [],
        "deleted": [],
        "modified": [],
        "unchanged": []
    }

    # 現在のアイテムをチェック
    for path, current_item in current_map.items():
        if path not in previous_map:
            comparison["added"].append(current_item)
        else:
            previous_item = previous_map[path]
            # Fileの場合はSHA1を比較
            if current_item["type"] == "file":
                if current_item.get("sha1") != previous_item.get("sha1"):
                    comparison["modified"].append({
                        "path": path,
                        "previous_sha1": previous_item.get("sha1"),
                        "current_sha1": current_item.get("sha1")
                    })
                else:
                    comparison["unchanged"].append(current_item)
            else:
                # ディレクトリの場合はunchangedとして扱う
                comparison["unchanged"].append(current_item)
            
    # 過去のアイテムで削除されたものをチェック
    for path, previous_item in previous_map.items():
        if path not in current_map:
            comparison["deleted"].append(previous_item)
    
    return comparison

def save_comparison(comparison, output_file):
    """比較結果をJSON Fileに保存する"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(comparison, f, indent=2, ensure_ascii=False)
        print(f"比較結果を保存しました {output_file}")
    except Exception as e:
        print(f"Error: 比較結果を保存できません {e}", file=sys.stderr)
        sys.exit(1)

def print_comparison(comparison):
    """比較結果を表示する"""
    print(f"\n========== 比較結果 ==========")

    if comparison["added"]:
        print(f"\n【追加】{len(comparison['added'])}件")
        for item in comparison["added"]:
            print(f"  + {item['path']} ({item['type']})")
    
    if comparison["deleted"]:
        print(f"\n【削除】{len(comparison['deleted'])}件")
        for item in comparison["deleted"]:
            print(f"  - {item['path']} ({item['type']})")
    
    if comparison["modified"]:
        print(f"\n【変更】{len(comparison['modified'])}件")
        for item in comparison["modified"]:
            print(f"  ~ {item['path']}")
            print(f"    前: {item['previous_sha1']}")
            print(f"    後: {item['current_sha1']}")
    
    if comparison["unchanged"]:
        print(f"\n【変更なし】{len(comparison['unchanged'])}件")
    
    print(f"\n合計: 追加{len(comparison['added'])}件  削除{len(comparison['deleted'])}件  変更{len(comparison['modified'])}件")

def main():
    parser = argparse.ArgumentParser(
        description='FileまたはディレクトリのSHA1を計算・比較します (Symbolic Linkは無視)'
    )
    parser.add_argument(
        'path',
        help='対象File または ディレクトリ のPath'
    )
    parser.add_argument(
        '-o', '--output',
        default='result.json',
        help='現在の結果を保存するファイル名 (default: result.json)'
    )
    parser.add_argument(
        '-c', '--compare',
        help='比較対象の過去のJSONファイルPath'
    )
    parser.add_argument(
        '-co', '--compare-output',
        default='comparison.json',
        help='比較結果を保存するファイル名 (default: comparison.json)'
    )

    args = parser.parse_args()

    # 現在の状態を取得
    print(f"処理中: {args.path}")
    current_results = process_path(args.path)

    # 現在の結果を保存
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(current_results, f, indent=2, ensure_ascii=False)
            print(f"現在の結果を保存しました {args.output}")
    except Exception as e:
        print(f"Error: JSONを保存できません {e}", file=sys.stderr)
        sys.exit(1)
    
    # 比較を実行
    if args.compare:
        print(f"\n比較中: {args.compare}")
        previous_results = load_json(args.compare)
        comparison = compare_results(current_results, previous_results)

        # 比較結果を保存
        save_comparison(comparison, args.compare_output)

        # 比較結果を表示
        print_comparison(comparison)
    else:
        print(f"\n処理終了: {len(current_results)}件")

if __name__ == '__main__':
    main()
