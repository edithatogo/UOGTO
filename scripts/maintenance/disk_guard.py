import shutil
import os
import sys

def check_disk_space(path="C:\\", threshold_mb=50):
    total, used, free = shutil.disk_usage(path)
    free_mb = free / (1024 * 1024)
    print(f"Free disk space on {path}: {free_mb:.2f} MB")
    
    if free_mb < threshold_mb:
        print(f"⚠️ Warning: Free space is below threshold of {threshold_mb} MB!")
        return False
    return True

def clean_caches():
    print("Initiating cache cleanup...")
    # Clean Python bytecode cache
    import glob
    for pyc in glob.glob("**/*.pyc", recursive=True):
        try:
            os.remove(pyc)
        except OSError:
            pass
    for cache_dir in glob.glob("**/__pycache__", recursive=True) + glob.glob("**/.pytest_cache", recursive=True):
        try:
            shutil.rmtree(cache_dir)
            print(f"Removed cache directory: {cache_dir}")
        except OSError:
            pass

def main():
    if not check_disk_space():
        clean_caches()
        # Verify again
        check_disk_space()

if __name__ == "__main__":
    main()
