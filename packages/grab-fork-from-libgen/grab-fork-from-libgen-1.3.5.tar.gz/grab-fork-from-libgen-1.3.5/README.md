# grab-fork-from-libgen
A fork of grab-convert-from-libgen, which is an easy API/wrapper for searching and downloading books from Libgen.

## Before Installing

**If you want to download books, be sure that you have installed Calibre and have added the necessary `ebook-convert` command to your path!**

[calibre](https://calibre-ebook.com/) is "a powerful and easy to use e-book manager". It's also free, open-source, and super easy to use.

You can install an calibre executable, through MacOS Homebrew, compile from source... pick your poison. They only thing you need to be sure of 
is the command `ebook-convert` is in your PATH.

If you choose not to do so, you can still use this library for searching on LibraryGenesis and scraping metadata.

## Install

Install by 

```
pip install grab-fork-from-libgen
```

### Migrating
If you already have `grab-convert-from-libgen` installed, run this:\
(not required)
```
pip uninstall grab-convert-from-libgen
```



## Fork Overview
### The following changes are made in this fork:
You can now get a book's cover. (from 3lib or LibraryRocks)  
You can now get a book's direct download links. (from LibraryLol)  
You can now get a book's description (if it has one) (also from LibraryLol).  
You can now get pagination info (Check how many pages and if there's a next page in your search.)  
Fixed "page" query in Fiction search.  
Some small fixes for edge cases.

All of these functions need the original file's md5 and topic.  
(Which are provided by default for every result entry in this version).

All these features are **OPT-IN**.  
This means your code won't break when migrating to this fork, and you may use the new functions how you want to.

You can read the documentation for the new methods below.  
This fork was made because some things may not comply with the original's author idea for the library.  
It's also made by a beginner, and while i've tried my best to use DRY, typehints, etc. Some things can still be improved.

Of course, this would not be possible without [Willmeyers](https://github.com/willmeyers/grab-convert-from-libgen) work.

## Quickstart

The example below shows to grab the first book returned from a search and save it to your current working directory as a pdf.

```python
from grab_fork_from_libgen import LibgenSearch

res = LibgenSearch('sci-tech', q='test')

res.first(convert_to='pdf')
```

This is an example the gets and downloads a book that matches a given title.

```python
from grab_fork_from_libgen import LibgenSearch

res = LibgenSearch('fiction', q='test')

res.get(title='a title', save_to='.')
```

You must specify a `topic` when creating a search instance. Choices are `fiction` or `sci-tech`.

## Documentation

Only search parameters marked as required are needed when searching.

### Libgen Non-fiction/Sci-tech
#### Search Parameters

`q`: The search query (required)

`sort`: Sort results. Choices are `def` (default), `id`, `title`, `author`, `publisher`, `year`

`sortmode`: Ascending or decending. Choices are `ASC` or `DESC`

`column`: The column to search against. Choices are `def` (default), `title`, `author`, `publisher`, `year`, `series`, `ISBN`, `Language`, or `md5`.

`phrase`: Search with mask (word*). Choices are `0` or `1`.

`res`: Results per page. Choices are `25`, `50`, or `100`.

`page`: Page number.

### Libgen Fiction
#### Search Parameters

`q`: The search query (required)

`criteria`: The column to search against. Choices are `title`, `authors`, or `series`.

`language`: Language code

`format`: File format

`wildcard`: Wildcarded words (word*). Set to `1`.

`page`: Page number

### LibgenSearch
#### get_results

`get_results(self, pagination: Optional[bool]) -> OrderedDict`

Caches and returns results based on the search parameters the `LibgenSearch` objects was initialized with. 
Takes one optional boolean argument.  
If it's **True**: Returns a dict, with two values, the first one being:
```
pagination = {
    "total_pages": either `int` or `None`
    "has_next_page": either `True` or `False`
}
```
And the second one being an ordered dict, which is your search results:
```
results = {
    0: "first_book_info"
    1: "second_book_info"
    ...
}
```
If the user sets pagination to **False** or doesn't provide any value, this OrderedDict is the only result returned.

You can easily convert this dict to an ordinary dict instead:
```
results = OrderedDict()
results = dict(results)
```
This will remove the index numbers before each book info.

Results are ordered in the same order as they would be displayed on libgen itself with the book's id serving as the key.

**Notice**: Using pagination will download Chrominium to your home folder on your first run. e.g.: "~/.pyppeteer/".
This only happens once. This happens because LibraryGenesis pagination uses javascript, which is not rendedered by default in the HTML.

It's important to pay attention to this if you use services (like Heroku Free Tier) with limited storage space.


#### first

`first(save_to: str = None, convert_to: str = None) -> Dict`

Returns the first book (as a dictionary) from the cached or obtained results.

#### get

`get(save_to: str = None, convert_to: str = None, **filters) -> Dict`

Returns the first book (as a dictionary) from the cached or obtained results that match the given filter parameters.


### Metadata
This class holds the methods responsible for metadata scraping.

#### Quickstart:
```python
# First, import the Metadata class from grab_fork_from_libgen.
from grab_fork_from_libgen import LibgenSearch, Metadata

# ...
# pagination=True means you opt-in for pagination info.
my_results = LibgenSearch.get_results(pagination=True)


# Get the values from your search results
search_results = my_results["results"]

# Get the info from the first entry in the results.
md5 = search_results[0]["md5"]
topic = search_results[0]["topic"]

# Instantiate a new Metadata class.
# Please read the timeout documentation on the official requests library docs.
meta = Metadata(md5, topic, timeout=(9, 18))

# And use the respective methods.
cover = meta.get_cover()
d_links_and_desc = meta.get_metadata()

```
### Metadata
The `Metadata` class takes three arguments, one being optional:\

`md5` = An `string`, a code used to identify the file on LibraryGenesis and others databases.

`topic` = An `string`, the topic of the file on LibraryGenesis' database. Either `fiction` or `sci-tech`.

`timeout (optional)` = Either `int`, `tuple` or `None`. Defaults to `None`, which equals to infinite timeout.\

Please read more about using tuples in the official `requests` 
[docs](https://docs.python-requests.org/en/latest/user/advanced/#timeouts).

It's good practice to always provide a timeout value. As both the cover and download links providers can be down or
slow at any given moment.\
If they take too long, your code will hang.

#### Metadata - Methods
`get_cover` returns an `string`, which is the direct link to that file's cover image. If no cover is found, returns a
"No Cover" image used in LibraryRocks.

`get_metadata` returns a `tuple`, the first value being a `dict` of all the direct download links of the file, and the
second value being the file's description.   

Throws if no download link is found.
If no description is found, returns `None` on the second value instead.

Please do note that none of these methods are rate-limited. If you abuse them, you will get blocked.\
From personal experience, `1500ms-2000ms` between each call is probably safe.
