def detect_type1_clones(files):
    clones = []
    n = len(files)

    for i in range(n):
        for j in range(i + 1, n):
            if files[i]["clean_code"].strip() == files[j]["clean_code"].strip():
                clones.append({
                    "file1": files[i]["file_path"],
                    "file2": files[j]["file_path"],
                    "similarity": 100.0
                })

    return clones