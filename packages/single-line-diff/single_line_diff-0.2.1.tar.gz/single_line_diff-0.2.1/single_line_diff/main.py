
import doctest

def getLongestMatchingSubstring(line1: str, line2: str, minMatchSize : int = 1):
	'''
	Doesn't do anything clever about ties.

	>>> getLongestMatchingSubstring("a", "b")
	''
	>>> getLongestMatchingSubstring("abc", "abc")
	'abc'
	>>> getLongestMatchingSubstring("abcd", "abc")
	'abc'
	>>> getLongestMatchingSubstring("abc", "abcd")
	'abc'
	>>> getLongestMatchingSubstring("bcd", "abcd")
	'bcd'
	>>> getLongestMatchingSubstring("abcde", "bcd")
	'bcd'
	>>> getLongestMatchingSubstring("bcd", "abcde")
	'bcd'

	# It should match abc due to optimization but the behaviour isn't really specified
	>>> getLongestMatchingSubstring("abc_xyz", "abc-xyz")
	'abc'

	# These tests check that we don't get any off by 1 errors
	>>> getLongestMatchingSubstring("a|ab|abc", "abc")
	'abc'
	>>> getLongestMatchingSubstring("abc", "a|ab|abc")
	'abc'
	>>> getLongestMatchingSubstring("abc", "a|abc|ab")
	'abc'
	>>> getLongestMatchingSubstring("a|abc|ab", "abc")
	'abc'
	>>> getLongestMatchingSubstring("abc", "a|abc|")
	'abc'
	>>> getLongestMatchingSubstring("a|abc|", "abc")
	'abc'

	# Min match size
	>>> getLongestMatchingSubstring("a", "a", 2)
	''
	>>> getLongestMatchingSubstring("ab", "ab", 2)
	'ab'
	'''
	currentBestMatch = ""
	line1Length = len(line1)
	for start in range(line1Length):
		for end in range(start + len(currentBestMatch) + minMatchSize, line1Length + 1):
			if line1[start:end] in line2:
				currentBestMatch = line1[start:end]
	return(currentBestMatch)

def diffRaw(line1 : str, line2 : str, minMatchSize : int = 1, matchCharacter : str = "•"):
	'''
	The main recursive function.

	# Non-recursive tests
	>>> diffRaw("", "")
	('', '', '')
	>>> diffRaw("a", "b")
	('a', 'b', '^')
	>>> diffRaw("aa", "b")
	('aa', 'b•', '^^')
	>>> diffRaw("a", "a")
	('a', 'a', ' ')

	# Recursive tests
	>>> diffRaw("abc", "xbz")
	('abc', 'xbz', '^ ^')
	>>> diffRaw("abcdef", "12ab34df56")
	('••abc•def••', '12ab34d•f56', '^^  ^^ ^ ^^')

	# Visual output:
	••abc•def••
	12ab34d•f56
	^^  ^^ ^ ^^
	'''
	largestMatch = getLongestMatchingSubstring(line1, line2, minMatchSize)
	if largestMatch == "":
		maxLength = max(len(line1), len(line2))
		return(line1.ljust(maxLength, matchCharacter), line2.ljust(maxLength, matchCharacter), maxLength * "^")
	else:
		line1Index = line1.index(largestMatch)
		line2Index = line2.index(largestMatch)
		largestMatchLength = len(largestMatch)
		
		left = diffRaw(line1[:line1Index], line2[:line2Index], minMatchSize, matchCharacter)
		right = diffRaw(line1[line1Index + largestMatchLength:], line2[line2Index + largestMatchLength:], minMatchSize, matchCharacter)

		return (left[0] + largestMatch + right[0], left[1] + largestMatch + right[1], left[2] + len(largestMatch) * " " + right[2])

def diff(line1 : str, line2 : str, minMatchSize : int = 1, matchCharacter : str = "•"):
	r'''
	>>> diff("A simple recursive single line diffing algorithm", "This recursive algorithm is awesome for diffing single lines")
	'A •simple recursive••••••••••••••••••••••••••••••••• single line diffing algorithm\nThis••••• recursive algorithm is awesome for diffing single lines•••••••••••••••••\n^^^ ^^^^^          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^            ^^^^^^^^^^^^^^^^^^\n'
	
	# Visual output:
	A •simple recursive••••••••••••••••••••••••••••••••• single line diffing algorithm
	This••••• recursive algorithm is awesome for diffing single lines•••••••••••••••••
	^^^ ^^^^^          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^            ^^^^^^^^^^^^^^^^^^

	# Min match size
	>>> diff("I called but no one answered.", "I called, but no one answered.")
	'I called• but no one answered.\nI called, but no one answered.\n        ^                     \n'
	>>> diff("I called but no one answered.", "I called, but no one answered.", 2)
	'I called• but no one answered.\nI called, but no one answered.\n        ^                     \n'
	>>> diff("What is your strategy?", "Tell us about your strategy.")
	'Wh••••••a•••t is your strategy?\nTell us about••• your strategy.\n^^^^^^^^ ^^^ ^^^              ^\n'
	>>> diff("What is your strategy?", "Tell us about your strategy.", 3)
	'What is•••••• your strategy?\nTell us about your strategy.\n^^^^^^^^^^^^^              ^\n'

	# First one results in this:
	Wh••••••a•••t is your strategy?
	Tell us about••• your strategy.
	^^^^^^^^ ^^^ ^^^              ^

	# Second one results in this
	What is•••••• your strategy?
	Tell us about your strategy.
	^^^^^^^^^^^^^              ^
	'''
	raw = diffRaw(line1, line2, minMatchSize, matchCharacter)
	return raw[0] + "\n" + raw[1] + "\n" + raw[2] + "\n"

if __name__ == "__main__":
	doctest.testmod()
