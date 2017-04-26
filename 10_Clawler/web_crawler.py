import os
import sys
import time
import bs4
import requests

def get_html_string(url):
    """
        Content:
            HTML取得
        Param:
            url: HTMLを取得するURL
    """
    decoded_html = ""

    # HTMLを取得
    try:
        r = requests.get(url)
        html = r.text
    except:
        return decoded_html

    decoded_html = html

    return decoded_html

def get_resource(html, extensions):
    """
        Content:
            リソース取得
        Param
            html:       HTML
            extensions: 拡張子のリスト
    """

    resource_list = []

    soup = bs4.BeautifulSoup(html)
    for a_tag in soup.find_all("a"):
        href_str = a_tag.get("href")
        try:
            (path, ext) = os.path.splitext(href_str)
            if ext in extensions:
                resource_list.append(href_str)
        except:
            pass

    resource_list = sorted(set(resource_list), key=resource_list.index)
    for resource in resource_list:
        try:
            print("download ---> [%s]" % os.path.basename(resource))
            r = requests.get(resource)
            f = open("./data/"+os.path.basename(resource), "wb")
            f.write(r.content)
        except Exception as e:
            print(e)
            print("download failed ... [%s]" % os.path.basename(resource))
        finally:
            time.sleep(3)


def crawling(url, extensions):
    """
        Content:
            クローリング
        Param:
            url:        クローリングするURL
            extensions: 取得するリソースの拡張子(list)
    """

    # 指定したURLのHTMLを取得
    html = get_html_string(url)
    if len(html) < 1:
        print("HTMLが取得できませんでした。")
        print("URLを確認してください。")
        sys.exit(1)

    # リソース取得
    get_resource(html, extensions)


def check_args():
    """
        Content:
            起動引数確認
    """
    if len(sys.argv) == 3:
        return True
    else:
        return False


def print_usage():
    print("Usage: %s URL Extensions" % __file__)
    print("URLにはクロールしたいウェブサイトのアドレスを指定してください。")
    print("Extensionsにはクロールしたときに取得するファイルの拡張子を指定してください。")
    print("Extensionsはカンマ区切りで複数指定できます。")


def main():
    """
        Content:
            main
    """
    # 引数確認
    if check_args() is False:
        print_usage()
        sys.exit(1)

    url = sys.argv[1]
    extensions = sys.argv[2].split(",")

    # クロール開始
    crawling(url, extensions)


if __name__ == "__main__":
    main()
