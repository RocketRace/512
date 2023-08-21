# [Round 6](https://cg.esolangs.gay/6/): Find a Fibonacci sum

[*Submitted entry*](https://cg.esolangs.gay/6/#4)

*Relevant files:* `Copy_of_sponge_2_copy_FINAL.docx.py`

This is one of my most cursed entries. The whole entry is built around the `# coding: unicode-escape`
declaration at the beginning of the file. This makes it possible to reference unicode codepoints using
octal (`\12`), hex (`\x7f`) or unicode (`\u2345`) escapes. This is, at first glance, not that weird.
Not so! A quirk with this encoding is that it assumes the file is encoded as latin-1. This is, of course,
a pretty valid assumption given that `unicode-escape` is meant to provide a platform-agnostic way to include
unicode characters inside your source code using only ASCII. However, most tools today use UTF-8 by default!
This includes text editors and, of course, the preview box on `cg.esolangs.gay`.

The code also abuses the fact that Python's identifiers can be any unicode character, so long as it fits into the
Consortium-provided identifier character classes. There are bytes >= 128 in the Latin-1 codepage that have that
property! Therefore, it's possible to create code that looks malformed, weird or otherwise cursed when viewed
as UTF-8, while fairly reasonable if still wild. (You can try for yourself by reopening it with the right encoding.)
Indeed, as utf-8 most of this code would immediately raise a `SyntaxError`! 

The code makes heavy use of this trick in multiple places, sowing as much chaos as I could possibly manage. 
I looked around for all the codepoints that were "interesting" enough to include small bits around. I think it's 
worthwhile to read through the source; there's a lot of details within. 

Oh, and of course. The final 6 megabytes of the code are dedicated to pixel art renditions of Sans Undertale. Apologies
to your text editor.
