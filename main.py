import pixiv
import danbooru
import utils

def main():
    print("Enter 1 to get resources from Danbooru. \nEnter 2 to get resources from Pixiv.")
    num_ask = input("Enter: ")
    try:
        num_ask = int(num_ask)
        if num_ask < 1 or num_ask > 2:
            print("Enter a valid number.")
            return
    except:
        print("Enter a number.")
        return
    print("Enter the path of file holding the image IDs.")
    print("If the path contains more than one ID, it must have it like this:\nID\nID\nID")
    file_ask:str = input("Enter file name/path: ")
    try:
        with open(file_ask) as _:
            pass
    except:
        print("File does not exist!")
        return
    utils.make_outer_img_dir()
    if num_ask == 2:
        pixiv.Pixiv(file_ask)
    else:
        danbooru.Danbooru(file_ask)
if __name__ == "__main__":
    main()