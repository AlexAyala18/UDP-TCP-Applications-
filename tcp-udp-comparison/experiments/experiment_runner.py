import csv
import time
import subprocess

FILES = ["small.txt", "medium.txt", "large.txt"]

results = []

print("Running TCP file transfer experiments...\n")

for file in FILES:
    print(f"Testing {file}...")

    start = time.time()

    # Run client automatically and pass filename
    process = subprocess.Popen(
        ["python", "tcp_file_client.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    output, _ = process.communicate(input=file + "\n")

    end = time.time()
    elapsed = end - start

    # Extract throughput from output
    throughput = 0
    for line in output.split("\n"):
        if "Throughput" in line:
            throughput = float(line.split(":")[1].strip().split()[0])

    results.append([file, elapsed, throughput])

# Save to CSV
with open("results/metrics.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["File", "Time(sec)", "Throughput(bytes/sec)"])
    writer.writerows(results)

print("\nExperiments complete. Data saved to results/metrics.csv")