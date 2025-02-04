import os
import argparse
import multiprocessing


def split_list(lst, n):
    if len(lst) <= n:
        return [lst]

    chunk_size = len(lst) // n
    
    chunks = [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

    # if len(chunks[-1]) < chunk_size:
    #     chunks[-2].extend(chunks[-1])
    #     chunks.pop()
    
    if len(chunks) > 1 and len(chunks[-1]) < chunk_size:
        chunks[-2].extend(chunks[-1])
        chunks.pop()

    return chunks


def download(i):
    for j in i:
        key = "e0c715109421c1282aeea45d09f68baaa6eb65304d9f52e9fa3bf83f494dc691"
        cmd = "curl -O --remote-header-name -G -d apikey=" + key + " -d sha256=" + j.strip() + " https://androzoo.uni.lu/api/download"
        print(cmd)
        os.system(cmd)



# way1 : apt install parallel
def main(filename):
    if os.path.isfile(filename):
        print(f"Processing file: {filename}")
        cmd = f"time cat {filename} | parallel -j20 -C '\s+' curl -# -O --remote-header-name -G -d " + \
          "apikey=e0c715109421c1282aeea45d09f68baaa6eb65304d9f52e9fa3bf83f494dc691 " + \
          "-d sha256={1} https://androzoo.uni.lu/api/download"
        print(cmd)
        os.system(cmd)
    else:
        print(f"[!] File {filename} not found.")


def main1(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        lists = split_list(lines, 20)

        processes = []
        for i in lists:
            p = multiprocessing.Process(target=download, args=(i,))
            p.start()
            processes.append(p)

        for process in processes:
            process.join()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a text file.")
    parser.add_argument('filename', type=str, help='The name of the file to process')

    args = parser.parse_args()

    # way1 
    main(args.filename)

    # way2
    # main1(args.filename)