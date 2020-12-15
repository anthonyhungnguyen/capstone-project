from extracting import extract
from checking_features import checking_features
from trainning1 import train
from utils.LogFCI import setup_logger

if __name__ == "__main__":

    # print("[Training] 1. extract_features()...")
    # extract()

    # print("[Training] 2. checking_features()...")
    # checking_features()

    print("[Training] 3. train()...")
    train()

    print("[Training] Done")
    exit()