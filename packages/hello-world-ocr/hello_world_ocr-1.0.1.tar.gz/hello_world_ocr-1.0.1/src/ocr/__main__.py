from ocr import scan

def main():
    image = "article.png"
    text = scan(image)
    print(text)

if __name__ == "__main__":
    main()
