import downloader

C = downloader.get("sst")
print(C)
d = C(0, 100, 0.5, "day")
d.download("bla")

