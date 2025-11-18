#!/usr/bin/env python3
"""
프로젝트 구텐베르크에서 인기 문학 작품을 다운로드합니다.
"""

import os
import requests
from time import sleep

# 프로젝트 구텐베르크의 인기 문학 작품 ID와 메타데이터
BOOKS = [
    {"id": 1342, "title": "Pride and Prejudice", "author": "Jane Austen"},
    {"id": 84, "title": "Frankenstein", "author": "Mary Shelley"},
    {"id": 1661, "title": "The Adventures of Sherlock Holmes", "author": "Arthur Conan Doyle"},
    {"id": 11, "title": "Alice's Adventures in Wonderland", "author": "Lewis Carroll"},
    {"id": 158, "title": "Emma", "author": "Jane Austen"},
    {"id": 1952, "title": "The Yellow Wallpaper", "author": "Charlotte Perkins Gilman"},
    {"id": 174, "title": "The Picture of Dorian Gray", "author": "Oscar Wilde"},
    {"id": 345, "title": "Dracula", "author": "Bram Stoker"},
    {"id": 1260, "title": "Jane Eyre", "author": "Charlotte Brontë"},
    {"id": 768, "title": "Wuthering Heights", "author": "Emily Brontë"},
    {"id": 2701, "title": "Moby Dick", "author": "Herman Melville"},
    {"id": 1400, "title": "Great Expectations", "author": "Charles Dickens"},
    {"id": 98, "title": "A Tale of Two Cities", "author": "Charles Dickens"},
    {"id": 46, "title": "A Christmas Carol", "author": "Charles Dickens"},
    {"id": 1232, "title": "The Prince", "author": "Niccolò Machiavelli"},
    {"id": 16, "title": "Peter Pan", "author": "J. M. Barrie"},
    {"id": 844, "title": "The Importance of Being Earnest", "author": "Oscar Wilde"},
    {"id": 1184, "title": "The Count of Monte Cristo", "author": "Alexandre Dumas"},
    {"id": 2600, "title": "War and Peace", "author": "Leo Tolstoy"},
    {"id": 1080, "title": "A Modest Proposal", "author": "Jonathan Swift"},
    {"id": 145, "title": "Middlemarch", "author": "George Eliot"},
    {"id": 1322, "title": "Leaves of Grass", "author": "Walt Whitman"},
    {"id": 55, "title": "The Wonderful Wizard of Oz", "author": "L. Frank Baum"},
    {"id": 1399, "title": "Anna Karenina", "author": "Leo Tolstoy"},
    {"id": 4300, "title": "Ulysses", "author": "James Joyce"},
]

def download_book(book_id, title, author, output_dir="books"):
    """프로젝트 구텐베르크에서 책을 다운로드합니다."""
    os.makedirs(output_dir, exist_ok=True)

    # 텍스트 파일 URL (UTF-8)
    url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"

    # 대체 URL (일부 책은 다른 형식)
    alt_url = f"https://www.gutenberg.org/files/{book_id}/{book_id}.txt"

    filename = os.path.join(output_dir, f"{book_id}.txt")

    # 이미 다운로드되어 있으면 스킵
    if os.path.exists(filename):
        print(f"✓ Already downloaded: {title} by {author}")
        return True

    try:
        print(f"Downloading: {title} by {author}...")
        response = requests.get(url, timeout=30)

        # 첫 번째 URL이 실패하면 대체 URL 시도
        if response.status_code != 200:
            response = requests.get(alt_url, timeout=30)

        if response.status_code == 200:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"✓ Downloaded: {title}")
            return True
        else:
            print(f"✗ Failed to download {title} (Status: {response.status_code})")
            return False

    except Exception as e:
        print(f"✗ Error downloading {title}: {str(e)}")
        return False

def main():
    """모든 책을 다운로드합니다."""
    print("=" * 60)
    print("프로젝트 구텐베르크에서 문학 작품 다운로드")
    print("=" * 60)
    print()

    success_count = 0
    total_count = len(BOOKS)

    for book in BOOKS:
        if download_book(book["id"], book["title"], book["author"]):
            success_count += 1
        # 서버에 부담을 주지 않기 위해 잠시 대기
        sleep(1)

    print()
    print("=" * 60)
    print(f"다운로드 완료: {success_count}/{total_count} 작품")
    print("=" * 60)

    # 메타데이터 저장
    import json
    with open("books_metadata.json", "w", encoding="utf-8") as f:
        json.dump(BOOKS, f, indent=2, ensure_ascii=False)
    print("메타데이터 저장: books_metadata.json")

if __name__ == "__main__":
    main()
