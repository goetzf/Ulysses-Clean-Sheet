# python3.3
# clean_sheet.py

# Version 1.0.1 2014-05-11 at 21:05 EDT
# Changes: 2014-05-11 More pure xml ET parsing.
# Finally discovered the element.tail attribute :)
# Either Clean Blank Lines or RegEx find & repl. Not both in the same run

# MIT (c) 2014 RoyRogers56

## Clean blank lines in Ulysses sheets:
# One blank line after each paragraph, except lists, quotes and code;
# Strips blank line after heading 3-6
# Strips double spaces.

## RegEx find & replace:
# Add two lines at top of sheet in UL codeblock:
# '' find:regex-pattern
# '' repl:repl-pattern
# See: https://docs.python.org/3.3/howto/regex.html
# Attributes (in link, image, and video) and Attachments are left untouched

# Use Hazel to trigger script, for smooth laundry service :)

import subprocess
import sys
import xml.etree.ElementTree as ET
import re

input_file = ""

if len(sys.argv) > 1:
    if sys.argv[1] != "":
        input_file = sys.argv[1]

if input_file == "":
    input_file = "test.ulysses"
    # print("*** No input file!")
    # quit()


def write_file(filename, file_content):
    f = open(filename, "w", encoding='utf-8')
    f.write(file_content)
    f.close()


# Globals:
use_regex = False
re_from = ""
re_to = ""


def replace(elem, text=False, tail=False):
    if text and elem.text:
        # elem.text: is element's inner text
        if use_regex:
            elem.text = re.sub(re_from, re_to, elem.text)
        else:
            # Clean double spaces:
            elem.text = re.sub(r" +", r" ", elem.text)
    if tail and elem.tail:
        # elem.tail: is text nodes following an element's closing tag.
        if use_regex:
            elem.tail = re.sub(re_from, re_to, elem.tail)
        else:
            # Clean double spaces:
            elem.tail = re.sub(r" +", r" ", elem.tail)


def regex_parse_par(p):
    global use_regex

    try:
        for elem in p.iter():
        # Iterates trough all elements and subelements of paragraph tree
        # No need for recursive calls :)
            if elem.tag == "p":
                replace(elem, text=True)
            elif elem.tag == "tag":
                continue
            elif elem.tag in ("tags", "attribute"):
                replace(elem, tail=True)
            else:
                replace(elem, text=True, tail=True)
        return None
    except Exception as e:
        use_regex = False
        print(e)
        msg = '<p><tags><tag kind="comment">%% </tag></tags>Error in RegEx: '\
              + '<element kind="code" startTag="`">"' + re_from + '", "' + re_to + '" : ' + str(e)\
              + '</element></p>\n'
        return ET.XML(msg)


def check_for_regex(p):
    global use_regex
    global re_from
    global re_to

    par = ET.tostring(p, "unicode", "xml")
    match = re.search(r'<p><tags><tag kind="codeblock">\'\' ?</tag></tags> *find:(.+)</p>', par)
    if match:
        re_from = match.group(1)
        return True
    match = re.search(r'<p><tags><tag kind="codeblock">\'\' ?</tag></tags> *repl:(.+)</p>', par)
    if re_from != "" and match:
        re_to = match.group(1)
        use_regex = True
        print("RegEx from:", re_from)
        print("RegEx to  :", re_to)
        return True

    return False


#*** Main program:

xml_file = input_file + "/Content.xml"
xml_doc = ET.parse(xml_file)

xml_new_body = ET.Element("string")
xml_new_body.set("xml:space", "preserve")

p_blank = ET.Element("p")

add_blank = False
next_blank = False
p_num = 0

xml_body = xml_doc.find("string")
for p in xml_body.iterfind("p"):
    p_num += 1
    if p_num <= 2 and check_for_regex(p):
        # Reads first two lines and chack for regex find: and repl:
        # then skips these lines if found
        continue

    if not use_regex:
        if add_blank:
            xml_new_body.append(p_blank)
            add_blank = False

        if not (p or p.text):
            # Blank lines
            if add_blank:
                xml_new_body.append(p_blank)
            add_blank = False
            continue

        kind = None
        tag = p.find("tags/tag")
        if tag is not None:
            kind = tag.get("kind")

        if kind in ("orderedList", "unorderedList", "codeblock", "blockquote", "comment"):
            # No blank line after list par and blockquote, except last.
            add_blank = False
            next_blank = True
        elif kind in ("heading1", "heading2"):
            # Blank line after heading1-2
            if next_blank:
                xml_new_body.append(p_blank)
                next_blank = False
            add_blank = True
        elif kind in ("heading3", "heading4", "heading5", "heading6"):
            # No blank line after heading3-6
            if next_blank:
                xml_new_body.append(p_blank)
                next_blank = False
            add_blank = False
        else:
            if next_blank:
                xml_new_body.append(p_blank)
                next_blank = False
            add_blank = True
    #end_if not use_regex

    # Stripping double blanks or RegEx replace:
    err_msg = regex_parse_par(p)
    if err_msg:
        xml_new_body.append(err_msg)

    # Building xml_new_body, by adding a paragraph for each iteration,
    # except when "continue" is used above:
    xml_new_body.append(p)
#end_for p in xml_body.iterfind("p")

xml_doc.getroot().remove(xml_body)
xml_doc.getroot().insert(1, xml_new_body)

xml_doc.write("debug.xml")

xml_doc.write(xml_file)
subprocess.call(['open', input_file])
print("Ulysses file processed:", input_file)
