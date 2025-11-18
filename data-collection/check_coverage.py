#!/usr/bin/env python3
"""
추출된 시간 데이터의 커버리지를 확인합니다.
"""

import json

def main():
    """시간 데이터 커버리지 분석"""
    with open('../public/times.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_times = len(data)
    total_quotes = sum(len(quotes) for quotes in data.values())

    print('📊 시간 추출 결과:')
    print(f'  - Distinct 시간대: {total_times}개 / 1440개')
    print(f'  - 커버율: {total_times/1440*100:.1f}%')
    print(f'  - 총 문장 수: {total_quotes}개')
    if total_times > 0:
        print(f'  - 시간대당 평균 문장: {total_quotes/total_times:.1f}개')
    print()

    # 시간대별 문장 수 분포
    counts = {}
    for quotes in data.values():
        count = len(quotes)
        counts[count] = counts.get(count, 0) + 1

    print('📈 시간대별 문장 수 분포 (상위 15개):')
    for count in sorted(counts.keys(), reverse=True)[:15]:
        print(f'  {count}개 문장: {counts[count]}개 시간대')

    print()
    print('⚠️  커버되지 않은 시간대:')
    missing = 1440 - total_times
    print(f'  - 커버 안됨: {missing}개 ({missing/1440*100:.1f}%)')

    # 추가 통계
    print()
    print('📋 추가 통계:')
    if data:
        quotes_counts = [len(quotes) for quotes in data.values()]
        print(f'  - 최대 문장 수: {max(quotes_counts)}개')
        print(f'  - 최소 문장 수: {min(quotes_counts)}개')
        print(f'  - 중간값: {sorted(quotes_counts)[len(quotes_counts)//2]}개')

    # 모든 시간대 생성 (00:00 ~ 23:59)
    all_times = []
    for hour in range(24):
        for minute in range(60):
            all_times.append(f'{hour:02d}:{minute:02d}')

    # 커버된 시간대와 안 된 시간대 분류
    covered_times = sorted(data.keys())
    missing_times = sorted([t for t in all_times if t not in data])

    # 커버된 시간대 목록 저장
    with open('covered_times.txt', 'w', encoding='utf-8') as f:
        f.write(f'커버된 시간대 ({len(covered_times)}/1440)\n')
        f.write('=' * 50 + '\n\n')
        for i, time in enumerate(covered_times, 1):
            quote_count = len(data[time])
            f.write(f'{time}  ({quote_count}개 문장)\n')
            if i % 60 == 0:  # 매 60개마다 구분선
                f.write('\n')

    # 커버 안 된 시간대 목록 저장
    with open('missing_times.txt', 'w', encoding='utf-8') as f:
        f.write(f'커버 안 된 시간대 ({len(missing_times)}/1440)\n')
        f.write('=' * 50 + '\n\n')
        for i, time in enumerate(missing_times, 1):
            f.write(f'{time}\n')
            if i % 60 == 0:  # 매 60개마다 구분선
                f.write('\n')

    print()
    print('📝 시간대 목록 파일 생성:')
    print(f'  - covered_times.txt ({len(covered_times)}개 시간대)')
    print(f'  - missing_times.txt ({len(missing_times)}개 시간대)')

if __name__ == "__main__":
    main()
