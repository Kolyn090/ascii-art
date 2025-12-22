import numpy as np


def reconstruct(long_img: np.ndarray, short_imgs: list[np.ndarray]) -> tuple[list[np.ndarray], float] | None:
    long_img = long_img.astype(bool)
    short_imgs = [t.astype(bool) for t in short_imgs]

    H, W = long_img.shape

    # --- DP arrays ---
    dp = [float('inf')] * (W + 1)
    choice: list[np.ndarray | None] = [None] * (W + 1)
    prev: list[int | None] = [None] * (W + 1)
    dp[0] = 0

    # --- DP ---
    for x in range(W + 1):
        if dp[x] == float('inf'):
            continue

        for tile in short_imgs:
            _, w = tile.shape
            nx = min(x + w, W)  # truncate at end
            region = long_img[:, x:nx]
            tile_crop = tile[:, :region.shape[1]]
            c = np.count_nonzero(region != tile_crop)

            if dp[x] + c < dp[nx]:
                dp[nx] = dp[x] + c
                choice[nx] = tile_crop
                prev[nx] = x

    # --- reconstruct solution ---
    seq: list[np.ndarray] = []

    x = W
    while x > 0:
        seq.insert(0, choice[x])
        x = prev[x]

    return seq, dp[W]
