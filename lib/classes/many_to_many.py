class Article:
    # class variable to store all Article instances
    all = []

    def __init__(self, author, magazine, title):
        self.author = author
        self.magazine = magazine
    # validate title
        if not isinstance(title, str):
            raise Exception("Title must be a string")
        if not (5 <= len(title) <= 50):
            raise Exception("Title must be 5–50 characters")
    # ensure title is immutable after first assignment
        if hasattr(self, "_title"):
            raise Exception("Title cannot be changed")
    # add this article to the global list
        self._title = title
        Article.all.append(self)

    @property
    def title(self):
         # returns article title
        return self._title

    @property
    def author(self):
        # returns author who wrote the article
        return self._author

    @author.setter
    def author(self, value):
        # ensures author is an Author instance
        if not isinstance(value, Author):
            raise Exception("Author must be an Author instance")
        self._author = value

    @property
    def magazine(self):
        # returns yhe magazine where the article was published
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        # ensures magazine is a Magazine instance
        if not isinstance(value, Magazine):
            raise Exception("Magazine must be a Magazine instance")
        self._magazine = value


class Author:
    def __init__(self, name):
        # author name must be a string 
        if not isinstance(name, str):
            raise Exception("Name must be a string")
        # author name must not be empty
        if len(name) < 1:
            raise Exception("Name must not be empty")

        self._name = name

    @property
    def name(self):
        return self._name

    def articles(self):
        # returns all articles written by this author
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        # returns all magazines this author has written for
        return list({a.magazine for a in self.articles()})

    def add_article(self, magazine, title):
        # creates and returns a new article written by this author for the given magazine with the given title
        return Article(self, magazine, title)

    def topic_areas(self):
        # returns a list of unique categories of magazines this author has written for
        mags = self.magazines()
        if not mags:
            # if the author has not written for any magazines,return None
            return None
        return list({m.category for m in mags})


class Magazine:
    all = []

    def __init__(self, name, category):
        """validations:
        - namemust be a string between 2 and 16 characters
        - category must be a non-empty string"""
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise Exception("Invalid magazine name")
        if not isinstance(category, str) or len(category) < 1:
            raise Exception("Invalid category")

        self._name = name
        self._category = category
        # add this magazine to the global list
        Magazine.all.append(self)

    @property
    def name(self):
        # returns magazine name
        return self._name

    @name.setter
    def name(self, value):
        # allows changing the magazine name with validation
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise Exception("Invalid magazine name")
        self._name = value

    @property
    def category(self):
        # returns magazine category
        return self._category

    @category.setter
    def category(self, value):
        # allows changing the magazine category with validation
        if not isinstance(value, str) or len(value) < 1:
            raise Exception("Invalid category")
        self._category = value

    def articles(self):
        # returns all articles published in this magazine
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        # returns all unique authors who have written for this magazine
        return list({a.author for a in self.articles()})

    def article_titles(self):
        # returns a list of titles of all articles published in this magazine
        arts = self.articles()
        if not arts:
            return None
        return [a.title for a in arts]

    def contributing_authors(self):
        # returns a list of authors who have written more than 2 articles for this magazine
        counts = {}
        # count articles per author
        for article in self.articles():
            counts[article.author] = counts.get(article.author, 0) + 1

        # filter authors with more than 2 articles
        result = [author for author, count in counts.items() if count > 2]

        return result if result else None

    @classmethod
    def top_publisher(cls):
        # returns the magazine with the highest number of articles published
        if not Article.all:
            return None

        return max(cls.all, key=lambda m: len(m.articles()))
