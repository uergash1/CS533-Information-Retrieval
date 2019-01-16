Problem statement
=================

Write a program that reads a document and outputs all the index terms that occur in it in lexicographic order.

The program should have one command parameter <file name>.txt (for the input file)

The document is a simple HTML file.
----------------------------------- 

1. Extract only terms between tags. Tags should be ignored. There will be no fixed pattern of tags, so make sure your code can handle all tags.

2. All index terms will be lower case.

3. Do not index the following stop words: and, a, the, an, by, from, for, hence, of, the, with, in, within, who, when, where, why, how, whom, have, had, has, not, for, but, do, does, done. 

4. Do not index a single character followed by space.

5. Use hyphen as an end of token. So the word data-base will be stored as two terms data and base. Unfortunately the date 1970-80 will become two numbers 1970 and 80.

6. Get rid of single and double quotes (“, ‘) or parentheses (( ,  [) when they are the first characters of a token.

7. Get rid of single and double quotes (“, ‘) or parentheses (( ,  [) when they are the last characters of the token.

8. A comma, a period, question mark, colon, semicolon, or an exclamation mark followed by space should not be included in a token (leave them in the token if they are not followed by a space).

9. Do index numbers (3,1111 will be stored as a single index term).

10. Delete all apostrophes in a token. So car’s, and cars’, will be changed to cars and then stemmed to car.

11. Do the following minimal stemming that deals with plurals and third person:

a. if word ends in “ies” but not “eies” or “aies” then “ies”->“y”; (skies becomes sky, dies become dy)
b. else in “es” but not “aes”, “ees” or “oes” then “es”->e; (retrieves becomes retrieve)
c. else in “s” but not “us” or “ss”   then “s”->NULL (doors becomes door, success stay success) endif

12. Your program should be able to handle any extra space or blank lines in the document.
