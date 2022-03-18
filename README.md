MDA Lint
========

*MDA Lint is only a prototype!*

MDA Lint is a linter for MDAnalysis and for programs using MDAnalysis. It
detects the use of MDAnalysis's API, makes sure they are applied appropriately,
and offers suggestions to fix and improved their usage. The linter also awards
badges when it recognises good practices advocated by MDAnalysis.

## Usage

```bash
mdalint /path/to/library/root
```

At the end of a run, the program lists the badges that were awarded as well as
errors and warnings that were detected.

## Badges

### AnalysisBase

The tested program implements at least one analysis using the [`AnalysisBase`
API](https://docs.mdanalysis.org/stable/documentation_pages/analysis/base.html).
This API allows to implement multi-frame analyses in a way that is consistent.
In most cases, it allows analyses to benefit from improvements to MDAnalysis
without modification.

The badge is assigned when at least one class inherit from `AnalysisBase` and
implements a `_single_frame` method.

#### Errors

An error is issued when:

* a class inherit from `AnalysisBase` but does not
  implements the `_single_frame` method. 
* the `run` method is overwritten and does not have the `start`, `stop`,
  `step`, and `verbose` arguments.

#### Warnings

A warning is issued when:

* the `run` method is overwritten.
* the `_prepare`, `_single_frame`, or `_conclude` method take unexpected
  arguments.
* neither the `_single_frame` nor the `_conclude` method assign values in the
  `results` attribute.

### Reader

### Parser

### Writer

### Topology attribute

### Selection keyword
