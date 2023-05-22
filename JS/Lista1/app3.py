import wikipedia

temat = input("Podaj nazwę artykułu na wikipedii (po angielsku): ")

strona = wikipedia.page(temat)

print(strona.summary)


print(f"Link do strony: {strona.url}")
