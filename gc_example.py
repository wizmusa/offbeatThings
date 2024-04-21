import gc

def run_garbage_collection():
    # 가비지 콜렉션 실행 및 개수 출력
    num_collected = gc.collect()
    print(f"Collected {num_collected} objects.")

# 메인 프로그램
if __name__ == "__main__":
    run_garbage_collection()
    print(gc.get_stats())
    print(gc.isenabled())