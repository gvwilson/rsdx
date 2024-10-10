---
title: "Introduction"
tagline: "An overview of where we're going and why."
abstract: >
    The best way to learn design is to study examples,
    and the best programs to use as examples
    are ones like those you want to create.
    These lessons therefore build small versions
    of tools that research software engineers build and use every day
    to show how experienced software designers think.
syllabus:
-   Assume you know how to program.
-   Want to learn how to design pieces of software that are reliable and reusable.
-   "Best way is through examples: principles don't make sense unless you know how to translate them into specifics."
---

The best way to learn design in any field
is to study examples [%b Schon1984 Petre2016 %],
and the most approachable examples are based on
problems that learners are already familiar with.
These lessons therefore solve scaled-down versions
of programs that researchers build every day
to show how experienced software designers think.
Along the way,
they introduce some fundamental ideas
that many self-taught programmers haven't encountered.
We hope these lessons will help you design better software yourself
and help you pass on what you know to others.

## Audience {: #intro-audience}

This learner persona [%b Wilson2019 %] describes who this book is for:

> *Ning has a master's degree in genomics.
> She knows enough Python to analyze data from her experiments,
> but wants to tackle bigger problems,
> have more confidence that she's getting the right answers,
> and write code that other people can use.
> These lessons will show her how to design, build, and test large programs
> in less time and with less pain.*
> {: .continue}

Like Ning, you should be able to:
{: .continue}

-   Write Python programs using lists, loops, conditionals, dictionaries, and functions
    and puzzle your way through Python programs that use classes and exceptions.
    ([The Carpentries lesson on Python][carpentries_python] covers everything you will need.)

-   Run Unix shell commands like `ls`, `mkdir`, `grep`, and `find`,
    use wildcards to match filenames,
    and write `for` loops to process multiple files.
    ([The Carpentries lesson on the shell][carpentries_shell] covers everything you will need.)

-   Use [Git][git] to save and share files.
    ([The Carpentries lesson on Git][carpentries_shell] covers everything you will need.)

-   Read and write a little bit of HTML.

This material will also help another persona:

> *Yim teaches an introduction to data science for biologists.
> They would like to teach a more advanced course
> to people who have mastered the basics,
> but doesn't have the time to build a curriculum themself
> and isn't really sure what they would include.
> This book will give them material they can use immediately
> and starting points for course projects.*
> {: .continue}

## The Big Ideas {: #intro-ideas}

Our approach to design is based on three big ideas.
First,
as the number of components in a system grows,
the complexity of the system increases rapidly
([%f intro-complexity %]).
However,
the number of things we can hold in working memory at any time
is fixed and fairly small [%b Hermans2021 %].
If we want to build large programs that we can understand,
we therefore need to construct them out of pieces
that interact in a small number of ways.
Figuring out what those pieces and interactions should be
is the core of what we call "design".

[% figure
   slug="intro-complexity"
   img="complexity.svg"
   alt="Complexity and size"
   caption="How complexity grows with size."
%]

Second,
"making sense" depends on who we are.
When we use a low-level language,
we incur the [%g cognitive_load "cognitive load" %]
of assembling micro-steps into something more meaningful.
When we use a high-level language,
on the other hand,
we incur a similar load translating functions of functions
into actual operations on actual data.

More experienced programmers are more capable at both ends of the curve,
but that's not the only thing that changes.
If a novice's comprehension curve looks like the lower one in [%f intro-comprehension %],
then an expert's looks like the upper one.
Experts don't just understand more at all levels of abstraction;
their *preferred* level has also shifted
so they find \\( \sqrt{x^2 + y^2} \\) easier to read
than the Medieval equivalent
"the side of the square whose area is the sum of the areas of the two squares
whose sides are given by the first part and the second part".
This curve means that for any given task,
the code that is quickest for a novice to comprehend
will almost certainly be different from the code that
an expert can understand most quickly.

[% figure
   slug="intro-comprehension"
   img="comprehension.svg"
   alt="Comprehension curves"
   caption="Novice and expert comprehension curves."
%]

Our third big idea is testing research applications is hard
because we often don't know what the right answer actually is.
(If we did,
we would already have published and moved on.)
However,
that doesn't mean such applications can't be tested:
if we think about how we're going to check the code as we design it,
we can make it as trustworthy as a physical experiment.

## Formatting {: #intro-layout}

We display Python source code like this:

[% inc "python_sample.py" %]

and Unix shell commands like this:
{: .continue}

[% inc "shell_sample.sh" %]

Data files and program output are shown like this:
{: .continue}

[% inc "data_sample.yml" %]

[% inc "output_sample.out" %]

We use `...` to show where lines have been omitted,
and occasionally break lines in unnatural ways to make them fit on the page.
Where we do this,
we end all but the last line with a single backslash `\`.
Finally,
we show glossary entries in **bold text**
and write functions as `function_name` rather than `function_name()`.
The latter is more common,
but the empty parentheses makes it hard to tell
whether we're talking about the function itself
or a call to the function with no parameters.

## Usage {: #intro-use}

The source for this book is available in <a href="[% config repo %]">our Git repository</a>
and all of it can be read on <a href="[% config site %]">our website</a>.
All of the written material in this book
is licensed under the [Creative Commons - Attribution - NonCommercial 4.0 International license][cc_by_nc]
(CC-BY-NC-4.0),
while the software is covered by the [Hippocratic License][hippocratic_license].
The first license allows you to use and remix this material for noncommercial purposes,
as-is or in adapted form,
provided you cite its original source;
if you want to sell copies or make money from this material in any other way,
you must <a href="mailto:[% config author.email %]">contact us</a> and obtain permission first.
The second license allows you to use and remix the software on this site
provided you do not violate international agreements governing human rights;
please see [%x license %] for details.

If you would like to improve what we have,
add new material,
or ask questions,
please <a href="[% config repo %]">file an issue</a>
or <a href="[% config author.email %]">email us</a>.
All contributors are required to abide by our Code of Conduct
([%x conduct %]).

## Acknowledgments {: #intro-acknowledgments}

Like [%b Wilson2022 %] and [%b Wilson2022 %],
this book was inspired by [%b Kamin1990 Kernighan1979 Kernighan1981 Kernighan1983 Kernighan1988 Oram2007 Wirth1976 %] and by:

-   [*The Architecture of Open Source Applications*][aosa] series
    [%b Brown2011 Brown2012 Armstrong2013 Brown2016 %];
-   the posts and [zines][evans_zines] created by [Julia Evans][evans_julia];
    and
-   everyone who helped write [%b Irving2021 %]
    or ever contributed to a [Carpentries][carpentries] lesson.

[% fixme "add thanks" %]

I am also grateful to Shashi Kumar for help with LaTeX,
and to the creators of
[Glosario][glosario],
[GNU Make][gnu_make],
[ark][ark],
[LaTeX][latex],
[pip][pip],
[Python][python],
[Ruff][ruff],
[WAVE][webaim_wave],
and many other open source tools:
if we all give a little,
we all get a lot.

All royalties from this book will go to the [Red Door Family Shelter][red_door] in Toronto.

## Exercises {: #intro-exercises}

[% fixme "fill in exercises for introduction" %]
