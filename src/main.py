from frameworks.scvs.scvs import SCVS


def main():
    scvs = SCVS()
    guidelines = scvs.guidelines()
    for guideline in guidelines:
        print(guideline)


if __name__ == "__main__":
    main()
