class Article:
    all = []

    def __init__(self, author, magazine, title):
        # Validate title
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters")
        
        self._title = title
        self._author = author
        self._magazine = magazine
        Article.all.append(self)

        # Register article with author and magazine
        if not hasattr(author, '_articles'):
            author._articles = []
        author._articles.append(self)

        if not hasattr(magazine, '_articles'):
            magazine._articles = []
        magazine._articles.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        raise Exception("Title cannot be changed after instantiation")

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise ValueError("Author must be an instance of Author")
        
        # Remove from old author's list
        if self._author and self in self._author._articles:
            self._author._articles.remove(self)
        
        # Add to new author's list
        self._author = value
        if not hasattr(value, '_articles'):
            value._articles = []
        value._articles.append(self)

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            raise ValueError("Magazine must be an instance of Magazine")
        
        # Remove from old magazine's list
        if self._magazine and self in self._magazine._articles:
            self._magazine._articles.remove(self)
        
        # Add to new magazine's list
        self._magazine = value
        if not hasattr(value, '_articles'):
            value._articles = []
        value._articles.append(self)


class Author:
    def __init__(self, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string")
        
        self._name = name
        self._articles = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise Exception("Name cannot be changed after instantiation")

    def articles(self):
        return self._articles

    def magazines(self):
        magazines = []
        for article in self._articles:
            if article.magazine not in magazines:
                magazines.append(article.magazine)
        return magazines

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        if not self._articles:
            return None
        
        topics = []
        for article in self._articles:
            category = article.magazine.category
            if category not in topics:
                topics.append(category)
        return topics


class Magazine:
    all = []

    def __init__(self, name, category):
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string")
        
        self._name = name
        self._category = category
        self._articles = []
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string")
        self._category = value

    def articles(self):
        return self._articles

    def contributors(self):
        authors = []
        for article in self._articles:
            if article.author not in authors:
                authors.append(article.author)
        return authors

    def article_titles(self):
        titles = [article.title for article in self._articles]
        return titles if titles else None

    def contributing_authors(self):
        author_counts = {}
        for article in self._articles:
            author = article.author
            author_counts[author] = author_counts.get(author, 0) + 1
        
        contributing = []
        for author, count in author_counts.items():
            if count > 2:
                contributing.append(author)
        
        return contributing if contributing else None

    @classmethod
    def top_publisher(cls):
        if not cls.all:
            return None
        
        # Find magazine with most articles
        top = None
        for magazine in cls.all:
            if len(magazine._articles) > 0:
                if top is None or len(magazine._articles) > len(top._articles):
                    top = magazine
        
        return top