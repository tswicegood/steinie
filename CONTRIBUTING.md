# Contributing to Steinie

So you wanna contribute?!  Awesome! :+1:

There are a couple of ways you can contribute to the development.  Not all of
which require you to code!


## Reporting Issues

I'm trying my best to make sure there aren't issues with all of code I release,
but occasionally bugs (:bug:) make it through and are released.  Here's a
checklist of things to do:

* [ ] Make sure you're on the latest version of `steinie`.  You can do that
  by running `pip update steinie`.
* [ ] If you're adventurous, you can try running the latest development version
  by running `pip install https://github.com/tswicegood/steinie/tarball/develop`.

If updating Steinie doesn't work for you, the next thing to d
[open a report][].  Here are a few things to make sure you include to help us
out the most:

* [ ] Explain what you expect to happen and what actually happened.
* [ ] Add the steps you used to reproduce the error.
* [ ] Include the code you ran and the output if there is any.  The error
  message is useful, but often information that's displayed before that can
  point me in the right direction.


## Contribute Code

The easiest thing to do is contribute a feature or fix a bug that you've found.
If you want to contribute but don't know where to start, check out our
(hopefully) small list of [open bugs][].  If you want to take a stab at adding
something, check out the list of [open enhancement requests][].

Once you know what you're going to add, there's a few things you can do to help
us figure out how to process your code:

* [Create a fork](https://github.com/tswicegood/steinie/fork)
* Create a branch with your change off of `develop`.  Follow these naming
  conventions for naming your branches:
  * `feature/{{ feature name }}` <-- new features
  * `fix/{{ issue number or general bug description }}` <-- fixes to the code
  * `refactor/{{ refactor name / description }}` <-- general cleanup /
      refactoring
* Commit your changes to your branch.  Changes with extensive unit tests are
  given priority because they simplify the process of verifying the code.
* Open a pull request against the `develop` branch
* :tada: profit!

I might not always get right back to you and your PR right away, but I'll try to
do it as quickly as possible.  If you haven't heard anything after a few days to
a week, please comment again to make sure notices are sent back out.


## Coding Guidelines

The rest of this document is aimed at people developing and releasing Steinie.


### Coding Style

* Please run all of your code through [flake8][] (yes, it's more strict than
  straight [pep8][], but it helps ensure a consistent visual style for our
  code).
* Please include tests for all new code and bugfixes.  The tests are run using
  [pytest][] so you can use things like [parameterized tests][] and such.
* Please [mark any tests][] that are slow with the `@pytest.mark.slow`
  decorator so they can be skipped when needed.


### Releasing Steinie

Steinie follows [SemVer][] with one specific change: pre-release versions are
denoted without using a hyphen.  For example, a development version of Steinie
might be `2.1alpha.0`.  Anything released with the `alpha` must be treated as
not-final code.

* The `develop` branch should always have a version number that is +1 minor
  version ahead of what is in `master`.  For example, if the latest code in
  `master` is `v2.0.2`, the `develop` branch should be `v2.1alpha.0`.


#### Merging Feature Releases to `master`

If you're ready to release, open a PR to ensure that `develop` has everything
that it needs for this release, including any updates to change logs and such.
Do not merge Steinie directly via GitHub's interface.  Instead, follow these
steps from your working tree:

* `git fetch origin`
* `git checkout master`
* `git merge --no-ff --no-commit origin/develop`
* Modify the `setup.py` and (eventually) `conda.recipe/meta.yaml` to remove the
  `alpha` from the minor version.
* `git commit` the changes.  Ensure that the subject line includes the version
  number at the end of the message.  You may also wish to include a descriptive
  sentence explaining the main feature(s) of the release.
* `git tag vX.Y.Z`
* `git push origin master --tags`
* After binstar build has successfully built the new version, make sure that all
  builds are added to the `main` channel of tswicegood.

> Author's Note: It would be great to automate this entirely into a tool that
> would build a release for you!


#### Handling Bugfix Releases

You should create a new branch called `vX.Y.Z-prep` from the tag and increment
the bugfix version number (`Z` in this example) by one and add `alpha`.  For
example, if the latest release is `v2.0.2`, you would create a branch called
`v2.0.3alpha` and the first commit should be the changes to `setup.py` and
(eventually) `conda.recipe/meta.yaml`.

Please open a pull request for this fix, but do not merge via GitHub.  Instead,
follow the outline above to handle the bugfix release.  Once merged, make sure
to merge `master` into `develop` and push that branch as well so the bugfix is
included in future versions.


[binstar build]: http://docs.binstar.org/build_cli.html
[tswicegood/c/dev]: https://conda.binstar.org/tswicegood/c/dev
[develop branch]: https://github.com/tswicegood/steinie/tree/develop
[flake8]: http://flake8.readthedocs.org/
[gist]: https://gist.github.com/
[mark any tests]: http://pytest.org/latest/example/markers.html
[open a report]: https://github.com/tswicegood/steinie/issues/new
[open bugs]: https://github.com/tswicegood/steinie/issues?q=is%3Aopen+is%3Aissue+label%3Abug
[open enhancement requests]: https://github.com/tswicegood/steinie/issues?q=is%3Aopen+is%3Aissue+label%3Aenhancement
[parameterized tests]: http://pytest.org/latest/parametrize.html#parametrize
[pep8]: https://www.python.org/dev/peps/pep-0008/
[pytest]: http://pytest.org/latest/
[SemVer]: http://semver.org/
