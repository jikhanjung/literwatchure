#!/usr/bin/env python3
"""
프로젝트 구텐베르크에서 인기 문학 작품을 다운로드합니다.
"""

import os
import sys
import requests
from time import sleep
from datetime import datetime
import random
import json

# 프로젝트 구텐베르크의 인기 문학 작품 ID와 메타데이터
def load_books_list(books_file="books_list.json"):
    """책 목록을 파일에서 로드합니다."""
    try:
        with open(books_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Books list file not found: {books_file}")
        sys.exit(1)


def load_excluded_books(excluded_file="excluded_books.json"):
    """제외할 책 목록을 로드합니다."""
    try:
        with open(excluded_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            excluded_titles = {book['title'] for book in data.get('excluded', [])}
            excluded_patterns = data.get('patterns', [])
            return excluded_titles, excluded_patterns
    except FileNotFoundError:
        print(f"⚠ Excluded books file not found: {excluded_file}")
        return set(), []

def log_download_error(book_id, title, url, status_code, log_file="download_errors.log"):
    """다운로드 에러를 로그 파일에 기록합니다."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Book ID: {book_id}, Title: {title}, URL: {url}, Status: {status_code}\n"

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def is_book_excluded(title, excluded_titles, excluded_patterns):
    """책이 제외 목록에 있는지 확인합니다."""
    # 정확한 제목 매칭
    if title in excluded_titles:
        return True

    # 패턴 매칭
    title_lower = title.lower()
    for pattern_obj in excluded_patterns:
        pattern = pattern_obj['pattern']
        case_sensitive = pattern_obj.get('case_sensitive', False)

        if case_sensitive:
            if pattern in title:
                return True
        else:
            if pattern in title_lower:
                return True

    return False

def download_book(book_id, title, author, output_dir="books", max_retries=3):
    """
    프로젝트 구텐베르크에서 책을 다운로드합니다.

    Returns:
        True: 성공적으로 다운로드됨
        False: 일반적인 실패
        "403": 403 Forbidden 에러 발생
    """
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

    # User-Agent 헤더 추가 (봇으로 인식되지 않도록)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for attempt in range(max_retries):
        try:
            if attempt > 0:
                wait_time = 10 * attempt  # 재시도 시 대기 시간 증가
                print(f"  Retry {attempt}/{max_retries-1} for {title} (waiting {wait_time}s)...")
                sleep(wait_time)

            print(f"Downloading: {title} by {author}...")
            print(f"  URL: {url}")
            response = requests.get(url, headers=headers, timeout=30)

            # 첫 번째 URL이 실패하면 대체 URL 시도
            if response.status_code != 200:
                print(f"  Trying alternative URL: {alt_url}")
                sleep(2)  # 대체 URL 시도 전 잠시 대기
                response = requests.get(alt_url, headers=headers, timeout=30)

            if response.status_code == 200:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"✓ Downloaded: {title}")
                return True
            elif response.status_code == 403:
                print(f"✗ 403 Forbidden for {title} - Server blocking requests")
                print(f"📋 Response Headers:")
                for header, value in response.headers.items():
                    print(f"   {header}: {value}")
                print(f"⚠ Skipping this book and continuing...")
                # 에러 로그 기록
                log_download_error(book_id, title, response.url, 403)
                return "403"
            else:
                print(f"✗ Failed to download {title} (Status: {response.status_code})")
                # 에러 로그 기록 (404 등 다른 에러)
                log_download_error(book_id, title, response.url, response.status_code)
                return False

        except requests.exceptions.Timeout:
            print(f"⚠ Timeout for {title}")
            if attempt < max_retries - 1:
                sleep(5)
                continue
            return False
        except Exception as e:
            print(f"✗ Error downloading {title}: {str(e)}")
            if attempt < max_retries - 1:
                sleep(3)
                continue
            return False

    return False

def main():
    """모든 책을 다운로드합니다."""
    print("=" * 60)
    print("프로젝트 구텐베르크에서 문학 작품 다운로드")
    print("=" * 60)
    print()

    # 책 목록 로드
    BOOKS = load_books_list()
    print(f"✓ Loaded {len(BOOKS)} books from books_list.json")

    # 제외할 책 목록 로드
    excluded_titles, excluded_patterns = load_excluded_books()
    print(f"✓ Loaded {len(excluded_titles)} excluded titles and {len(excluded_patterns)} patterns")
    print()

    # BOOKS 목록 필터링
    filtered_books = []
    excluded_count = 0

    for book in BOOKS:
        if is_book_excluded(book["title"], excluded_titles, excluded_patterns):
            print(f"⊘ Excluding: {book['title']}")
            excluded_count += 1
        else:
            filtered_books.append(book)

    # 다운로드 순서를 랜덤하게 섞어서 연속된 ID가 나오지 않도록 함
    random.shuffle(filtered_books)
    print(f"✓ Shuffled download order to avoid consecutive book IDs")

    print()
    print(f"Total books: {len(BOOKS)}, Excluded: {excluded_count}, To download: {len(filtered_books)}")
    print()

    success_count = 0
    total_count = len(filtered_books)
    consecutive_403_count = 0  # 연속 403 에러 카운터

    for book in filtered_books:
        filename = os.path.join("books", f"{book['id']}.txt")
        already_exists = os.path.exists(filename)

        result = download_book(book["id"], book["title"], book["author"])

        if result == "403":
            consecutive_403_count += 1
            print(f"⚠ Consecutive 403 errors: {consecutive_403_count}/10")

            if consecutive_403_count >= 10:
                print()
                print("=" * 60)
                print("⛔ 연속 10회 403 에러 발생으로 스크립트를 종료합니다.")
                print("=" * 60)
                break
        elif result == True:
            success_count += 1
            consecutive_403_count = 0  # 성공 시 카운터 리셋
        else:
            consecutive_403_count = 0  # 일반 실패 시에도 카운터 리셋

        # 실제로 다운로드를 시도한 경우에만 대기
        if not already_exists:
            delay = random.uniform(5, 8)
            print(f"  다음 다운로드까지 {delay:.1f}초 대기 중...")
            sleep(delay)

    print()
    print("=" * 60)
    print(f"다운로드 완료: {success_count}/{total_count} 작품")
    print("=" * 60)

    # 메타데이터 저장 (필터링된 목록만)
    with open("books_metadata.json", "w", encoding="utf-8") as f:
        json.dump(filtered_books, f, indent=2, ensure_ascii=False)
    print(f"메타데이터 저장: books_metadata.json ({len(filtered_books)} books)")

if __name__ == "__main__":
    main()
