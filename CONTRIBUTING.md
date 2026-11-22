# Contributing to codeuz

Thanks for helping. These notes cover every repository in the organization that does not have its own contributing guide.

## Found a mistake?

Open an issue in the repository the page belongs to and paste the page's address. Typos, wrong output, broken links and unclear explanations are all worth reporting. Most pages also have an edit link at the bottom that opens the file on GitHub.

## Sending a change

1. Fork the repository and make your change on a branch.
2. Run the site locally to check it. Each repository's README says how.
3. Open a pull request against `main`. CI builds the site and runs the code examples, and it has to pass.

Keep each pull request to one topic. Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/) with a capitalized description, for example `fix: Correct loop example output`.

Most pages come in English and Uzbek. If you change only one language, say so in the pull request so the other one can be updated too.

## Writing Uzbek lessons

Use the Uzbek edition of Python Foundations as the reference for spelling, terms, and tone. Its lessons on lists, dictionaries, sets, and recursion show how to introduce a concept through a small example and explain what the code does. Use the same term when a later course revisits the concept. [Python Foundations in Uzbek](https://codeuz-edu.github.io/python-tutorials/uz/)

Write with **ö**, **ğ**, **ş**, and **ç**. Use **ʼ** (U+02BC) where words such as **maʼlumot** and **taʼsir** need a tutuq sign. Keep Python identifiers and library names as written in the source. Keep expected output in step with any changes to code or sample text.

| English | Uzbek |
| --- | --- |
| list, array | röyxat, massiv |
| dictionary, set | luğat, töplam |
| key, value, element | kalit, qiymat, element |
| string, tuple | satr, kortej |
| class, object, attribute, reference | klass, obyekt, atribut, havola |
| loop, call stack | sikl, çaqiruvlar steki |
| hash, hashing, hashable | xeş, xeşlaş, xeşlanadigan |
| cache, caching | keş, keşlaş |
| sort, search | saralaş, qidiriş |
| base case, recursive case | bazaviy holat, rekursiv holat |
| running time, memory use | bajariliş vaqti, xotira sarfi |

Use **Nimalarni örganasiz** for learning goals, **Maşq** or **Maşqlar** for practice, **Yeçim** for solutions, and **Xulosa** for recaps. In the browser editor, use **Işga tuşiriş**, **Tekşiriş**, and **Natija**. Call the playground **Sinov maydonçasi**.

Review the Uzbek and English pages side by side. Check that examples, edge cases, and assumptions still agree, including whether a time bound is average, amortized, or worst case. Fix a factual mistake in both editions and run the example checks. Between courses, link readers to the same language when that edition exists.
