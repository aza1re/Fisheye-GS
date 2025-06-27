from pathlib import Path
from rosbags.highlevel import AnyReader

bag_dir = Path("/home/user/Fisheye-GS/data/fgsdata/2025-06-18_16-57-10/data")

print("Checking for bag files in:", bag_dir)
for bag_file in bag_dir.glob("*.bag"):
    print(f"\nBag file: {bag_file}")
    with AnyReader([bag_file]) as reader:
        print("Topics found:")
        for topic in reader.topics:
            print(f"  {topic} ({reader.topics[topic].msgtype})")