class Article:
    """Represents an Article linking an Author and a Magazine.

    Attributes:
        all (list): class-level list of all Article instances created.
    """
    all = []

    def __init__(self, author, magazine, title):
        """Create a new Article and link it to author and magazine.

        Validates `title` length (5..50). On success the new Article is
        appended to `Article.all` and also added to the private
        `_articles` lists on both the author and magazine objects. The
        linking is a side-effect expected by the tests.

        Args:
            author (Author): the article's author instance.
            magazine (Magazine): the magazine instance this article belongs to.
            title (str): article title (5-50 characters).

        Raises:
            ValueError: if title fails validation.
        """
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters")
        self._title = title
        self._author = author
        self._magazine = magazine
        Article.all.append(self)

        # Ensure owner objects have an _articles list and register this article
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
        # Titles are immutable after creation in this model.
        raise Exception("Title cannot be changed after instantiation")

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        # Allow changing the article's author while keeping relationships
        # consistent: remove from the previous author's list and append
        # to the new author's list.
        if not isinstance(value, Author):
            raise ValueError("Author must be an instance of Author")
        if self._author and self in self._author._articles:
            self._author._articles.remove(self)
        self._author = value
        if not hasattr(value, '_articles'):
            value._articles = []
        value._articles.append(self)

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        # Similar to author setter: preserve bidirectional links when
        # changing the magazine for this article.
        if not isinstance(value, Magazine):
            raise ValueError("Magazine must be an instance of Magazine")
        if self._magazine and self in self._magazine._articles:
            self._magazine._articles.remove(self)
        self._magazine = value
        if not hasattr(value, '_articles'):
            value._articles = []
        value._articles.append(self)
        
class Author:
    """Simple Author model storing a name and articles list.

    The Author keeps a private `_articles` list populated when new
    Article instances are created or when an Article's author is updated.
    """
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
        """Return a list of Article instances written by this author.

        Returns an empty list when the author has no articles.
        """
        return self._articles

    def magazines(self):
        """Return unique Magazine instances the author has written for.

        Uses a set comprehension to remove duplicates and returns a list.
        """
        return list(set(article.magazine for article in self._articles))

    def add_article(self, magazine, title):
        """Create and return a new Article authored by this Author.

        This is a convenience wrapper around Article(...). The Article
        constructor will validate the title and automatically register the
        article on both the author and magazine.
        """
        article = Article(self, magazine, title)
        return article

    def topic_areas(self):
        """Return unique categories (strings) of magazines the author writes for.

        Returns None when the author has no articles to mirror the tests'
        expectations for empty results.
        """
        if not self._articles:
            return None
        return list(set(article.magazine.category for article in self._articles))

class Magazine:
    """Simple Magazine model storing name, category and its articles.

    The class-level `all` list tracks every Magazine instance created.
    """
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
        """Return list of Article instances published in this Magazine."""
        return self._articles

    def contributors(self):
        """Return unique authors who have written for this magazine."""
        return list(set(article.author for article in self._articles))

    def article_titles(self):
        """Return list of article titles or None when no articles exist.

        Tests expect None for empty results, so we mirror that behavior.
        """
        titles = [article.title for article in self._articles]
        return titles if titles else None

    def contributing_authors(self):
        """Return authors who have contributed more than 2 articles.

        Returns None when no authors meet the threshold.
        """
        author_counts = {}
        for article in self._articles:
            author = article.author
            author_counts[author] = author_counts.get(author, 0) + 1
        contributing = [author for author, count in author_counts.items() if count > 2]
        return contributing if contributing else None

    @classmethod
    def top_publisher(cls):
        """Return the Magazine with the most articles or None if none exist.

        Uses a simple max key on the length of _articles and returns None
        when there are no magazines with articles.
        """
        if not cls.all:
            return None
        return max(cls.all, key=lambda mag: len(mag._articles)) if any(len(mag._articles) > 0 for mag in cls.all) else None
