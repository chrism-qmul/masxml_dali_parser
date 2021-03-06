# MASXML-DALI Parser

## Description

Quick and dirty convenience wrappers around lxml etree for easier parsing.

The XML is quite straightforward, so this parser doesn't do much apart from:
- un-flatten the relationships between the various types
- provide a convenient DSL-like interface for querying
- translate between IDs and offsets (+ relative offsets to parent nodes)

All elements can be used as normal lxml etree.

## Install

```
pip install git+git://github.com/chrism-qmul/masxml_dali_parser.git
```

or in requirements.txt as:
```
git+git://github.com/chrism-qmul/masxml_dali_parser.git@0.0.2#egg=masxml-dali-parser
```

## Example
Fetch the first sentence, its tokens, its markables (+ heads),
get back the relative offsets of those markables, and display the text.

```python
import masxml_dali_parser 

fh = open("data/DALI-LEARN/Read_Easy_English/A_Back_To_School-masxml.xml", 'rb')
xml_string = fh.read()
parser = masxml_dali_parser.Parser(xml_string)

sentence = parser.sentences()[1]
print([word.text for word in sentence.words()])
for markable in sentence.markables():
  print((markable.relative_offsets(sentence), markable.getparent().relative_offsets(sentence), [word.text for word in markable.words()]))
```

## Example
Fetch the mentions from the first paragraph and get their named entities:

```python
import masxml_dali_parser

fh = open("data/DALI-LEARN/Read_Easy_English/A_Back_To_School-masxml.xml", 'rb')
xml_string = fh.read()
parser = masxml_dali_parser.Parser(xml_string)

paragraph = parser.paragraphs()[0]
print(paragraph.original_text())
for markable in paragraph.markables():
  print([word.text for word in markable.words()])
  print([ner.get("nerType") for ner in markable.ner()])
  print("***")
```
