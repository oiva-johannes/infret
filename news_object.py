class NewsArticle:
    __articles = []

    def __init__(self, text, link, header, provider):
        self.__text = text
        self.__link = link
        self.__header = header
        self.__provider = provider
        self.__articles.append(self)
    
    def __str__(self) -> str:
        return f"\nText: {self.__text}\nLink: {self.__link}\nHeader size: {self.__header}\n"
                
    @staticmethod
    def show():
        for article in NewsArticle.__articles:
            print(article)
